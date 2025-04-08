document.addEventListener("DOMContentLoaded", function() {
    function updateDeviceType() {
        const deviceType = window.innerWidth <= 768 ? "mobile" : "desktop";
        const deviceTypeStore = document.querySelector('[data-dash-id="device-type"]');
        if (deviceTypeStore) {
            deviceTypeStore.setAttribute("data", deviceType);
        }
    }
    updateDeviceType();
    window.addEventListener("resize", updateDeviceType);  // Update on window resize
});