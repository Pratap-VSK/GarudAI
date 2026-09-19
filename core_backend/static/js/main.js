document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Initialize Leaflet Map (Centered to India by default)
    const map = L.map('map', { attributionControl: false }).setView([20.5937, 78.9629], 5);
    
    
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
        maxZoom: 19
    }).addTo(map);

    let userMarker = null;

    // 3. Handle Form Submission & Geolocation
    const submitBtn = document.getElementById('submitBtn');
    const statusMsg = document.getElementById('statusMsg');

    submitBtn.addEventListener('click', () => {
        const desc = document.getElementById('issueDesc').value.trim();

        if (!desc) {
            alert("Please enter a detailed description of the civic issue.");
            return;
        }

        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            return;
        }

        // Update UI state
        submitBtn.disabled = true;
        statusMsg.innerText = "Capturing secure GPS coordinates...";

        // Fetch Location
        navigator.geolocation.getCurrentPosition(async (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;

            // Update Map Visuals instantly
            map.flyTo([lat, lon], 16, { animate: true, duration: 1.5 });
            
            if (userMarker) { map.removeLayer(userMarker); }
            
            userMarker = L.marker([lat, lon]).addTo(map)
                .bindPopup("<b>Target Locked</b><br>Coordinates transmitted.")
                .openPopup();

            statusMsg.innerText = "Connecting to GarudAI Microservice...";

            // Send to Django API
            try {
                const response = await fetch('/api/submit/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ lat: lat, lon: lon, description: desc })
                });

                const result = await response.json();

                if (result.status === "success") {
                    statusMsg.innerText = "";
                    submitBtn.innerText = "Report Generated";
                    
                    // Map Django Backend response to UI
                    document.getElementById('locDisplay').innerText = result.location || "Coordinates Verified";
                    document.getElementById('deptDisplay').innerText = result.department;
                    document.getElementById('emailDisplay').innerText = result.email;
                    document.getElementById('letterDisplay').innerText = result.letter;
                    
                    // Show Result Box
                    document.getElementById('resultBox').classList.remove('hidden');
                    
                    // Scroll result into view on mobile
                    document.getElementById('resultBox').scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    statusMsg.innerText = "Error: " + result.message;
                    submitBtn.disabled = false;
                }
            } catch (err) {
                statusMsg.innerText = "Connection failed to AI server. Check backend.";
                submitBtn.disabled = false;
            }
        }, (err) => {
            // Error handling for GPS block
            statusMsg.innerText = "Location permission denied. GPS access is mandatory.";
            submitBtn.disabled = false;
        });
    });
});