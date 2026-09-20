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

# ==========================================
# 1. PUBLIC & AUTHENTICATION VIEWS
# ==========================================
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


# ==========================================
# 2. PROTECTED CITIZEN VIEWS
# ==========================================
@login_required(login_url='/login/')
def dashboard(request):
    """Fetches user-specific database records for the dashboard."""
    complaints = Incident.objects.filter(user=request.user)
    context = {
        'total_requests': complaints.count(),
        'pending_requests': complaints.filter(status='Pending').count(),
        'resolved_requests': complaints.filter(status='Resolved').count(),
        'user_complaints': complaints  
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def my_reports(request):
    """Fetches all detailed reports for the logged-in user."""
    complaints = Incident.objects.filter(user=request.user)
    context = {
        'user_complaints': complaints
    }
    return render(request, 'my_reports.html', context)

@login_required(login_url='/login/')
def index(request):
    """Renders the Live Escalation Terminal (Map + Form)."""
    return render(request, 'index.html')


# ==========================================
# 3. API ENDPOINTS (TWO-STEP PROCESS)
# ==========================================
@csrf_exempt
@login_required(login_url='/login/')
def submit_incident(request):
    """STEP 1: Sends data to FastAPI, personalizes letter, NO DB SAVE."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            lat = body.get('lat', 0.0)
            lon = body.get('lon', 0.0)
            desc = body.get('description', '')
            
            citizen = request.user
            full_name = citizen.get_full_name() or citizen.username
            user_email = citizen.email
            user_phone = citizen.profile.phone if hasattr(citizen, 'profile') else "N/A"
            
            # --- URL SETUP ---
            fastapi_url = "https://garudai-production.up.railway.app/process-incident"
            
            # fastapi_url = "http://127.0.0.1:8001/process-incident"
            
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
                
                drafted_letter = drafted_letter.replace("[Your Name]", full_name)
                drafted_letter = drafted_letter.replace("[Contact Number]", user_phone)
                drafted_letter = drafted_letter.replace("[Email Address]", user_email)
                drafted_letter = drafted_letter.replace("[Your Name/Signature]", full_name)

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

@csrf_exempt
@login_required(login_url='/login/')
def confirm_incident(request):
    """STEP 2: Called when user clicks 'File Complaint'. Saves exact location and data to DB."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            lat = body.get('lat', 0.0)
            lon = body.get('lon', 0.0)
            
            location_name = body.get('location', '')
            if not location_name or location_name == "Unknown Location":
                try:
                    geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
                    headers = {'User-Agent': 'GarudAI-CivicPlatform'}
                    geo_res = requests.get(geo_url, headers=headers).json()
                    if 'display_name' in geo_res:
                        address_parts = geo_res['display_name'].split(',')
                        location_name = f"{address_parts[0].strip()}, {address_parts[1].strip()}" if len(address_parts) > 1 else geo_res['display_name']
                except:
                    location_name = f"Lat: {lat:.4f}, Lon: {lon:.4f}"

            Incident.objects.create(
                user=request.user,
                description=body.get('description', ''),
                latitude=lat,
                longitude=lon,
                location_city=location_name,
                department=body.get('department', ''),
                authority_email=body.get('email', ''),
                drafted_letter=body.get('letter', ''),
                status='Pending'
            )
            return JsonResponse({"status": "success", "saved_location": location_name})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)