import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  
os.environ["OMP_NUM_THREADS"] = "1" 


import json
import io
import gradio as gr
from ollama_client import chat_llm, vision_qa
from tools import search_flights, baggage_allowance, fetch_pnr
from faster_whisper import WhisperModel

ASR_MODEL = None  # lazy load on first use for speed

# Tool schema specification
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Finds flight options",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "date": {"type": "string", "description": "YYYY-MM-DD"},
                    "pax": {"type": "integer", "default": 1},
                    "cabin": {"type": "string", "enum": ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS"]}
                },
                "required": ["origin", "destination", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "baggage_allowance",
            "description": "Returns baggage limits",
            "parameters": {
                "type": "object",
                "properties": {
                    "cabin": {"type": "string", "enum": ["ECONOMY", "BUSINESS"], "default": "ECONOMY"},
                    "is_international": {"type": "boolean", "default": False},
                    "status": {"type": "string", "enum": ["NONE", "GOLD", "PLATINUM"], "default": "NONE"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_pnr",
            "description": "Looks up booking details for a PNR",
            "parameters": {
                "type": "object",
                "properties": {"pnr_code": {"type": "string"}},
                "required": ["pnr_code"]
            }
        }
    }
]


def route_tools(tool_name, args):
    if tool_name == "search_flights":
        return search_flights(**args)
    if tool_name == "baggage_allowance":
        return baggage_allowance(**args)
    if tool_name == "fetch_pnr":
        return fetch_pnr(**args)
    return {"error": f"Unknown tool {tool_name}"}


def llm_chat(user_msg, history):
    messages = []
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": user_msg})

    resp = chat_llm(messages, model="llama3.1:8b", tools=TOOLS_SPEC)
    out = resp.get("message", {})
    tool_calls = out.get("tool_calls", []) or []
    assistant_text = out.get("content", "")

    # If the LLM requested tools, run them and feed back results
    if tool_calls:
        tool_results = []
        for call in tool_calls:
            fn = call.get("function", {})
            name = fn.get("name")
            raw_args = fn.get("arguments", "{}")

            # Handle both string and dict cases
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args or "{}")
                except Exception:
                    args = {}
            elif isinstance(raw_args, dict):
                args = raw_args
            else:
                args = {}

            result = route_tools(name, args)
            tool_results.append({"tool_name": name, "result": result})

        # Send a follow-up message with tool results to get final answer
        messages.append({
            "role": "tool",
            "content": json.dumps(tool_results)
        })
        final = chat_llm(messages, model="llama3.1:8b")
        assistant_text = final.get("message", {}).get("content", assistant_text)

    return assistant_text


def vision_chat(image, prompt):
    if image is None:
        return "Please upload a boarding pass/screenshot/image."
    # Convert PIL to bytes
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    resp = vision_qa(buf.getvalue(), prompt or "Extract key details useful for travel.")
    return resp.get("message", {}).get("content", "")


def transcribe(audio):
    global ASR_MODEL
    if audio is None:
        return ""
    if ASR_MODEL is None:
        ASR_MODEL = WhisperModel("small", device="cpu")  
    segments, _ = ASR_MODEL.transcribe(audio, beam_size=1)
    return " ".join([s.text for s in segments]).strip()


async def speak(text):
    import edge_tts
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    wav = "tts.wav"
    await communicate.save(wav)
    return wav


with gr.Blocks(title="Multimodal Airline Assistant") as demo:
    gr.Markdown("# ✈️ Multimodal Airline Assistant")

    with gr.Tab("Chat"):
        chat_history = gr.State([])
        chatbox = gr.Chatbot(height=380)
        user_in = gr.Textbox(
            placeholder="Ask me: Find flights BLR→DEL on 2025-09-12, baggage limit for business class, check PNR AB12CD...",
            lines=2)
        send = gr.Button("Send")

        def on_send(m, h):
            ans = llm_chat(m, h or [])
            h = (h or []) + [(m, ans)]
            return h, "", h

        send.click(on_send, [user_in, chat_history], [chatbox, user_in, chat_history])

    with gr.Tab("Image (Boarding pass / rules)"):
        img = gr.Image(type="pil")
        prompt = gr.Textbox(
            value="Read this image and extract passenger name, PNR, flight, times, terminal/gate, and baggage.", lines=2)
        go = gr.Button("Analyze")
        out = gr.Markdown()
        go.click(vision_chat, [img, prompt], out)

    with gr.Tab("Voice"):
        gr.Markdown("Speak your query, I’ll transcribe and answer.")
        mic = gr.Audio(sources=["microphone"], type="filepath")
        transcribed = gr.Textbox(label="Transcript")
        do_tx = gr.Button("Transcribe")
        do_tx.click(transcribe, mic, transcribed)

        chat_from_voice = gr.Button("Ask Assistant")
        chat_ans = gr.Markdown()
        chat_from_voice.click(lambda t: llm_chat(t, []), transcribed, chat_ans)
demo.queue().launch()
