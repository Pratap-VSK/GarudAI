from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IncidentInput(BaseModel):
    lat: float
    lon: float
    description: str

@app.post("/process-incident")
async def process_incident(data: IncidentInput):
    # 1. Reverse Geocoding
    headers_geo = {'User-Agent': 'GarudAI/1.0 (hackathon@test.com)'}
    loc_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={data.lat}&lon={data.lon}"
    loc_res = requests.get(loc_url, headers=headers_geo)
    
    if loc_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Location fetch failed")
        
    loc_data = loc_res.json()
    addr = loc_data.get('address', {})
    ward = addr.get('suburb', addr.get('neighbourhood', 'Local Area'))
    city = addr.get('city', addr.get('town', 'Local City'))
    pincode = addr.get('postcode', 'NA')

    # 2. Prompt Definition
    prompt = f"""
    Issue reported: "{data.description}"
    Location: Ward: {ward}, City: {city}, Pincode: {pincode}

    Identify the responsible local municipal department and draft a formal complaint.
    Return strictly valid JSON with these keys:
    "department", "authority_email", "pincode", "drafted_letter".
    """

    # 3. Call Groq REST API (Using valid Llama3 model)
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers_groq = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"
    }
    payload = {
        "model": "llama3-8b-8192",  # YAHAN MODEL FIX KIYA HAI
        "messages": [
            {"role": "system", "content": "You are GarudAI. Output only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(groq_url, headers=headers_groq, json=payload)
        
        if response.status_code != 200:
            print(f"🚨 Groq API Failed: {response.text}")
            raise Exception("Groq rejected request")

        response_data = response.json()
        cleaned = response_data['choices'][0]['message']['content'].strip()
        
        # Strip Markdown formatting (Llama JSON fix)
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:-3].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:-3].strip()
            
        parsed_ai = json.loads(cleaned)

    except Exception as e:
        print(f"Direct API Error: {e}")
        parsed_ai = {
            "department": "Municipal Corporation",
            "authority_email": "admin@local.gov",
            "pincode": pincode,
            "drafted_letter": "The AI is currently processing heavy load. Please try again."
        }

    return {
        "location": f"{ward}, {city} ({pincode})",
        "result": parsed_ai
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)