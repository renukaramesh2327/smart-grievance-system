// API Base URL
const API_BASE = window.location.origin + '/api';

// Token management
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function removeUser() {
    localStorage.removeItem('user');
}

// API call helper
async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
    }

    return data;
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Logout
function logout() {
    removeToken();
    removeUser();
    window.location.href = 'login.html';
}

// Check authentication
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Get status badge class
function getStatusBadgeClass(status) {
    const statusMap = {
        'Received': 'badge-received',
        'Assigned to Department': 'badge-assigned',
        'Under Progress': 'badge-progress',
        'Investigation': 'badge-investigation',
        'Reviewed': 'badge-reviewed',
        'Resolved': 'badge-resolved',
        'Closed': 'badge-closed'
    };
    return statusMap[status] || 'badge-received';
}

// Update header with user info
function updateHeader() {
    const user = getUser();
    if (!user) return;

    const userInfoDiv = document.querySelector('.user-info');
    if (userInfoDiv) {
        userInfoDiv.innerHTML = `
            <span>${user.name}</span>
            <span class="badge ${user.role === 'ADMIN' ? 'badge-resolved' : user.role === 'OFFICER' ? 'badge-progress' : 'badge-received'}">${user.role}</span>
        `;
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Add logout button handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    // Update header
    updateHeader();
});
