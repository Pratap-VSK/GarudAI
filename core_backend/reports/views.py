from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
import requests
import json
from .models import Incident, CitizenProfile

def landing(request):
    """Renders the main landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def register_view(request):
    """Handles User Registration and creates CitizenProfile."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        pincode = request.POST.get('pincode')
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullname)
        
        CitizenProfile.objects.create(
            user=user,
            phone=phone,
            age=age,
            pincode=pincode,
            city=location
        )
        
        messages.success(request, "GarudAI Account created successfully! Please login.")
        return redirect('login')
        
    return render(request, 'register.html')

def login_view(request):
    """Handles Citizen Login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
            
    return render(request, 'login.html')

def logout_view(request):
    """Logs out the user and clears session."""
    logout(request)
    return redirect('landing')

@login_required(login_url='/login/')
def dashboard(request):
    """Fetches user-specific database records for the dashboard."""
    complaints = Incident.objects.filter(user=request.user)
    
    context = {
        'total_requests': complaints.count(),
        'pending_requests': complaints.filter(status='Pending').count(),
        'resolved_requests': complaints.filter(status='Resolved').count(),
        'user_complaints': complaints  # Order is handled by Meta class in models.py
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def index(request):
    """Renders the Live Escalation Terminal (Map + Form)."""
    return render(request, 'index.html')

@csrf_exempt
@login_required(login_url='/login/')
def submit_incident(request):
    """Sends GPS/Description to FastAPI, and saves the AI response to the Database."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            lat = body.get('lat', 0.0)
            lon = body.get('lon', 0.0)
            desc = body.get('description', '')
            
            fastapi_url = "http://127.0.0.1:8001/process-incident"
            res = requests.post(fastapi_url, json=body)
            
            if res.status_code == 200:
                api_response = res.json()
                
                if not isinstance(api_response, dict):
                    api_response = {}
                    
                ai_data = api_response.get("result", {})
                if isinstance(ai_data, str):
                    try:
                        ai_data = json.loads(ai_data)
                    except:
                        ai_data = {}
                        
                department = ai_data.get("department", "Municipal Corporation")
                authority_email = ai_data.get("authority_email", "admin@local.gov")
                drafted_letter = ai_data.get("drafted_letter", "Error generating letter.")
                location_str = api_response.get("location", "Unknown Location")

                Incident.objects.create(
                    user=request.user,         
                    description=desc,
                    latitude=lat,
                    longitude=lon,
                    location_city=location_str,
                    department=department,
                    authority_email=authority_email,
                    drafted_letter=drafted_letter,
                    status='Pending'            
                )

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