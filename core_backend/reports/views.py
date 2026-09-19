from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def submit_incident(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            
            fastapi_url = "http://127.0.0.1:8001/process-incident"
            res = requests.post(fastapi_url, json=body)
            
            if res.status_code == 200:
                api_response = res.json()
                
                if not isinstance(api_response, dict):
                    api_response = {}
                    
                ai_data = api_response.get("result")
                if ai_data is None:
                    ai_data = {}
                    
                if isinstance(ai_data, str):
                    try:
                        ai_data = json.loads(ai_data)
                    except:
                        ai_data = {}
                        
                if not isinstance(ai_data, dict):
                    ai_data = {}

                department = ai_data.get("department", "Municipal Corporation")
                authority_email = ai_data.get("authority_email", "admin@local.gov")
                drafted_letter = ai_data.get("drafted_letter", "Error generating letter.")
                location_str = api_response.get("location", "Unknown Location")

                return JsonResponse({
                    "status": "success", 
                    "location": location_str,
                    "department": department,
                    "email": authority_email,
                    "letter": drafted_letter
                })
            else:
                return JsonResponse({"status": "error", "message": "AI Server Error"}, status=503)

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Django Error: {str(e)}"}, status=500)