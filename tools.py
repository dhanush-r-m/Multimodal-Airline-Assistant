# tools.py
from datetime import datetime, timedelta

def search_flights(origin, destination, date, pax=1, cabin="ECONOMY"):
    # Replace with real GDS/NDC/metasearch later
    base_price = 85 if cabin=="ECONOMY" else 220
    return [
        {"carrier":"AI","flight":"AI 503","dep":f"{date}T07:10","arr":f"{date}T09:55",
         "from":origin,"to":destination,"cabin":cabin,"price":base_price + 30},
        {"carrier":"6E","flight":"6E 2198","dep":f"{date}T12:30","arr":f"{date}T15:05",
         "from":origin,"to":destination,"cabin":cabin,"price":base_price + 45},
    ]

def baggage_allowance(cabin="ECONOMY", is_international=False, status="NONE"):
    base = 15 if not is_international else 23
    if cabin == "BUSINESS": base += 10
    if status in ("GOLD","PLATINUM"): base += 10
    return {"checked_kg": base, "cabin_kg": 7}

def fetch_pnr(pnr_code):
    # Stub—replace with your airline PNR service
    return {
        "pnr": pnr_code,
        "name": "DOE/JOHN",
        "itinerary": [
            {"from":"BLR","to":"DEL","dep":"2025-09-12T07:10","flight":"AI 503","status":"CONFIRMED"}
        ],
        "baggage": baggage_allowance()
    }
