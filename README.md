# 🦅 GarudAI 
> **Empowering Citizens for a Clean India, One Neighborhood at a Time.**

![GarudAI Banner](https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-Backend-092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-Microservice-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white) ![Groq](https://img.shields.io/badge/AI-Llama_3-FF9900.svg?style=for-the-badge)

GarudAI is an intelligent, grassroots civic-tech platform designed to transform the **"Clean India"** vision into reality. It bridges the gap between residents and local government by eliminating the bureaucratic friction of reporting local civic issues. 

Using precise GPS-based reverse geocoding and the advanced Llama 3 AI model, GarudAI allows users to simply describe a neighborhood problem in everyday words. The system instantly identifies the exact municipal ward and automatically drafts a formal, legally structured escalation letter directed to the correct local authority. 

---

## ✨ Why GarudAI is Different

* 🧠 **Zero-Knowledge Civic Engine:** No need to navigate complex government portals. Just type what you see, and our AI acts as your personal "Bureaucratic Translator".
* 📍 **Hyper-Local Precision:** Automated reverse-geocoding locks down the exact street and ward, leaving no room for authorities to ignore the issue due to vague location data.
* 🚀 **Enterprise-Grade Architecture:** Built on scalable, decoupled microservices (Django + FastAPI), ensuring the AI generation workloads never slow down the main user dashboard.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3, JavaScript, Leaflet.js (OpenStreetMap)
* **Backend Core:** Django (User Auth, Database Models, Security)
* **AI Microservice:** FastAPI (High-speed REST API)
* **AI Engine:** Groq Cloud API (Llama-3.3-70b-versatile)
* **Database:** SQLite (Local) / PostgreSQL (Production)

---

## 💻 How to Install & Run Locally

Follow these steps to get GarudAI running on your local machine. You will need to run two terminal windows: one for the Django frontend and one for the FastAPI microservice.

### Step 1: Prerequisites
Make sure you have **Python 3.10+** and **Git** installed on your PC. You also need a free API key from [Groq Cloud](https://console.groq.com/).

### Step 2: Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone [https://github.com/yourusername/GarudAI.git](https://github.com/yourusername/GarudAI.git)
cd GarudAI
```
Step 3: Setup Virtual Environment & Dependencies
Create a virtual environment to keep things clean:
```
python -m venv venv
```
Activate the virtual environment:
Windows:
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```
Install all required packages:
```
pip install django fastapi uvicorn requests python-dotenv pydantic
```
Step 4: Configure Environment Variables
In the root of your project (or inside your ai_service folder), create a file named .env and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```
Step 5: Start the FastAPI Microservice (Terminal 1)
Open a terminal, ensure your virtual environment is active, navigate to where your main.py is located, and start the AI engine:
```
cd ai_service
uvicorn main:app --host 127.0.0.1 --port 8080 --reload

(Leave this terminal running in the background).
```
Step 6: Setup Database & Start Django (Terminal 2)
Open a new terminal window, activate the virtual environment again, navigate to your Django backend folder, and run the database migrations:

Bash
```
cd core_backend
python manage.py makemigrations
python manage.py migrate
```
Create an admin account to log into the dashboard:
```
python manage.py createsuperuser
```
Finally, start the Django development server:
```
python manage.py runserver
```

🎉 Step 7: You are Live!
Open your web browser and go to: http://127.0.0.1:8000
Log in with the superuser credentials you just created. Click "Report an Issue", allow location access, type your complaint, and watch GarudAI generate your formal escalation letter instantly!

---

<br>

<div align="center">
  <h2>🔥 <span style="color: #FF5722;">Code. Demand. Transform.</span> 🔥</h2>
  
  <p style="font-size: 18px; font-style: italic; color: #555555; max-width: 800px; margin: 0 auto; line-height: 1.6;">
    "Real change doesn't wait for government approvals. It starts the moment a citizen refuses to walk past the filth on their street. GarudAI isn't just a codebase—it's a digital rebellion against civic apathy. We are bypassing the bureaucracy and putting the power of accountability straight into the hands of the common man."
  </p>

  <h3>
    <span style="color: #009688;">Stop ignoring. Start escalating.</span> 🦅
  </h3>

  <p>
    🤝 <b>Join the GarudAI Movement</b> <br>
    Because a Clean India isn't just a political slogan; it's an engineering problem. And we are here to fix it. <b>Star this repo ⭐</b> and let's upgrade our democracy, one ward at a time! 🚀
  </p>

  <br>

  <p>
    <span style="color: #FF9933;"><b>Engineered with relentless passion for 🇮🇳</b></span> <br><br>
    <b>Vision & Code by</b> <br>
    <span style="color: #2196F3; font-size: 24px; font-weight: 900; letter-spacing: 1px;">-:   S. Pratap Vishwakarma👨🏻‍💻   :-</span> 
  </p>
</div>
