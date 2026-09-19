document.getElementById('submitBtn').addEventListener('click', () => {
    const desc = document.getElementById('issueDesc').value.trim();
    const statusMsg = document.getElementById('statusMsg');

    if (!desc) {
        alert("Please enter a problem description.");
        return;
    }

    if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser.");
        return;
    }

    statusMsg.innerText = "Capturing coordinates and connecting with GarudAI...";

    navigator.geolocation.getCurrentPosition(async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        try {
            const response = await fetch('/api/submit/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat: lat, lon: lon, description: desc })
            });

            const result = await response.json();

            if (result.status === "success") {
                statusMsg.innerText = "Complaint generated successfully!";
                
                document.getElementById('locDisplay').innerText = result.location;
                document.getElementById('deptDisplay').innerText = result.department;
                document.getElementById('emailDisplay').innerText = result.email;
                document.getElementById('letterDisplay').innerText = result.letter;
                
                document.getElementById('resultBox').classList.remove('hidden');
            } else {
                statusMsg.innerText = "Error: " + result.message;
            }
        } catch (err) {
            statusMsg.innerText = "Connection failed to server.";
        }
    }, (err) => {
        statusMsg.innerText = "Location permission denied. Please allow GPS access.";
    });
});