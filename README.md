# ✈️ Multimodal Airline Assistant  

An **AI-powered Airline Assistant** that helps users book flights, check baggage allowances, and fetch booking details using **Ollama** for LLM reasoning and **Gradio** for an interactive multimodal UI.  

It supports:  
- 🗣️ **Natural Language Queries** (e.g., *“Find flights from Bangalore to Delhi tomorrow”*)  
- 🖼️ **Vision Q&A** (upload boarding passes, flight tickets, or images for AI-based answers)  
- 🧾 **PNR Lookup** (fetch booking details from PNR codes)  
- 🎒 **Baggage Allowance Queries** (by cabin class, status, domestic/international)  

---

## 🚀 Features  
- 💬 **Conversational AI** with Ollama (chat-based airline assistant)  
- 🛫 **Flight Search** (origin, destination, date, cabin, passengers)  
- 🎟 **PNR Fetch** (lookup booking details)  
- 📦 **Baggage Allowance** (economy, business, frequent flyer tiers)  
- 🖼️ **Vision AI** (analyze flight-related images like boarding passes)  
- 🌐 **Gradio UI** for a seamless chat interface  

---

## 🛠️ Tech Stack  
- **Python** (Backend)  
- **Gradio** (Frontend UI)  
- **Ollama** (Local LLM API)  
- **Requests / JSON** for API calls  
- **Torch + Faster Whisper** (optional for speech)  

---

## Screenshots


## 📂 Project Structure  
```
Airline-Agent/
│── app.py # Main Gradio app
│── ollama_client.py # Wrapper for Ollama API (chat + vision)
│── requirements.txt # Dependencies
│── README.md # Project documentation
```

---

## ⚡ Installation  

1️⃣ Clone the repo  
```bash
git clone https://github.com/your-username/airline-assistant.git
cd airline-assistant
```
2️⃣ Create & activate virtual environment
```
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
4️⃣ Install & run Ollama locally
```
👉 Download Ollama
👉 Run your preferred model (e.g., llama3)
ollama run llama3
```
▶️ Usage

Run the Gradio app:
```
python app.py
```
Open in browser: http://127.0.0.1:7860

---

⚠️ Troubleshooting

404 Ollama error → Make sure Ollama is running (ollama serve)

OMP Error #15 → Add at top of app.py:
```
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
```

Model not found → Pull model first:
```
ollama pull llama3
```

👨‍💻 Author

Dhanush Moolemane 

---
