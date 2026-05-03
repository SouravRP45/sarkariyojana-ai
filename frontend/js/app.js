// Global state
window.appState = {
    userProfile: null,
    schemes: [],
    currentView: 'hero' // hero, profile, dashboard
};

// Navigation
function navigateTo(viewId) {
    document.querySelectorAll('section').forEach(sec => sec.classList.remove('active'));
    document.getElementById(`${viewId}-section`).classList.add('active');
    window.appState.currentView = viewId;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Basic navigation
    document.getElementById('btn-start').addEventListener('click', () => {
        navigateTo('profile');
        initProfileForm();
    });

    document.getElementById('chat-fab').addEventListener('click', toggleChat);
    document.getElementById('close-chat').addEventListener('click', toggleChat);
    
    // Chat setup
    initChat();
});
