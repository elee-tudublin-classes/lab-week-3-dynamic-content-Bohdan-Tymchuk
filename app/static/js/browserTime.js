// browserTime.js
function updateClientTime() {
    const clientTimeSpan = document.getElementById('clientTime');
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    clientTimeSpan.textContent = timeString;
}

// Update the time every second
setInterval(updateClientTime, 1000);

// Set the initial client time on page load
updateClientTime();
