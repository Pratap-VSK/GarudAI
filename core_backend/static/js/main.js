document.addEventListener('DOMContentLoaded', () => {
    
    const map = L.map('map', { attributionControl: false }).setView([20.5937, 78.9629], 5);
    
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19
    }).addTo(map);
    
    let userMarker = null;
    let currentComplaintData = null; 

    const submitBtn = document.getElementById('submitBtn');
    const statusMsg = document.getElementById('statusMsg');

    submitBtn.addEventListener('click', () => {
        const desc = document.getElementById('issueDesc').value.trim();

        if (!desc) { alert("Please enter a detailed description of the civic issue."); return; }
        if (!navigator.geolocation) { alert("Geolocation is not supported by your browser."); return; }

        submitBtn.disabled = true;
        statusMsg.innerText = "Acquiring precise satellite GPS coordinates...";

        const options = {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        };

        navigator.geolocation.getCurrentPosition(async (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;

            map.flyTo([lat, lon], 17, { animate: true, duration: 1.5 });
            if (userMarker) { map.removeLayer(userMarker); }
            
            userMarker = L.marker([lat, lon], { draggable: true }).addTo(map)
                .bindPopup("<b>Exact Location Locked</b><br>Drag pin if needed.")
                .openPopup();

            userMarker.on('dragend', function (event) {
                const markerPos = event.target.getLatLng();
                currentComplaintData.lat = markerPos.lat;
                currentComplaintData.lon = markerPos.lng;
            });

            statusMsg.innerText = "Connecting to GarudAI Microservice...";

            try {
                const response = await fetch('/api/submit/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ lat: lat, lon: lon, description: desc })
                });

                const result = await response.json();

                if (result.status === "success") {
                    statusMsg.innerText = "";
                    submitBtn.innerText = "Draft Generated (Verify Pin on Map)";
                    
                    document.getElementById('locDisplay').innerText = result.location || "Coordinates Verified";
                    document.getElementById('deptDisplay').innerText = result.department;
                    document.getElementById('emailDisplay').innerText = result.email;
                    document.getElementById('letterDisplay').innerText = result.letter;
                    
                    currentComplaintData = {
                        description: desc,
                        lat: lat,
                        lon: lon,
                        location: result.location,
                        department: result.department,
                        email: result.email,
                        letter: result.letter
                    };
                    
                    document.getElementById('resultBox').classList.remove('hidden');
                    document.getElementById('resultBox').scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    statusMsg.innerText = "Error: " + result.message;
                    submitBtn.disabled = false;
                }
            } catch (err) {
                statusMsg.innerText = "Connection failed to AI server.";
                submitBtn.disabled = false;
            }
        }, (err) => {
            statusMsg.innerText = "Location permission denied or GPS timeout. Allow GPS access.";
            submitBtn.disabled = false;
        }, options);
    });

    const confirmSendBtn = document.getElementById('confirmSendBtn');
    const resetBtn = document.getElementById('resetBtn');

    if (resetBtn) {
        resetBtn.addEventListener('click', () => { 
            window.location.reload(); 
        });
    }

    if (confirmSendBtn) {
        confirmSendBtn.addEventListener('click', async function() {
            if (!currentComplaintData) return;

            this.innerHTML = "Filing to Authority...";
            this.disabled = true;

            try {
                const response = await fetch('/api/confirm/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentComplaintData)
                });
                
                const resData = await response.json();

                if (resData.status === "success") {
                    this.innerHTML = "Complaint Filed Successfully ✓";
                    this.style.backgroundColor = "#138808"; 
                    this.style.borderColor = "#138808";
                    this.style.color = "#fff";
                    alert(`Success! Complaint filed for location: ${resData.saved_location}`);
                    
                    setTimeout(() => {
                        window.location.href = "/my-reports/";
                    }, 2000);
                } else {
                    alert("Error saving complaint to database.");
                    this.disabled = false;
                    this.innerHTML = "File Complaint";
                }
            } catch (err) {
                alert("Network error while filing complaint.");
                this.disabled = false;
                this.innerHTML = "File Complaint";
            }
        });
    }
});