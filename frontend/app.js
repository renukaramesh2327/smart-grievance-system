// API Base URL
const API_BASE = window.location.origin + '/api';

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

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

// API call helper with robust error handling
async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };

    let response;
    try {
        response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
    } catch (err) {
        throw new Error('Network error. Please check your connection and try again.');
    }

    let data;
    try {
        data = await response.json();
    } catch {
        throw new Error('Invalid response from server');
    }

    if (response.status === 401) {
        removeToken();
        removeUser();
        window.location.href = 'login.html';
        throw new Error('Session expired. Please login again.');
    }

    if (!response.ok) {
        const msg = data.message || data.error || 'Something went wrong';
        throw new Error(msg);
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
    if (!status) return 'badge-received';
    const statusMap = {
        'Received': 'badge-received',
        'Assigned to Department': 'badge-assigned',
        'Assigned': 'badge-assigned',
        'Under Progress': 'badge-progress',
        'In Progress': 'badge-progress',
        'Investigation': 'badge-investigation',
        'Reviewed': 'badge-reviewed',
        'Resolved': 'badge-resolved',
        'Closed': 'badge-closed',
        'Rejected': 'badge-closed'
    };
    return statusMap[status] || 'badge-received';
}

// Get home URL based on user role
function getHomeUrl() {
    const user = getUser();
    if (!user) return 'index.html';
    if (user.role === 'ADMIN') return 'admin.html';
    if (user.role === 'OFFICER') return 'officer.html';
    return 'index.html';
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

    // Register Service Worker for PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(() => {});
    }
});
