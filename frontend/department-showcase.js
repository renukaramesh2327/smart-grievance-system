/**
 * Department Showcase System
 * Rotates daily to give equal respect to all departments
 */

const departments = [
    { name: 'Water Supply', icon: '💧', color: '#0077be', day: 0 },
    { name: 'Electricity', icon: '⚡', color: '#f39c12', day: 1 },
    { name: 'Sanitation', icon: '🧹', color: '#27ae60', day: 2 },
    { name: 'Roads & Infrastructure', icon: '🛣️', color: '#34495e', day: 3 },
    { name: 'Healthcare', icon: '🏥', color: '#e74c3c', day: 4 },
    { name: 'Education', icon: '📚', color: '#3498db', day: 5 },
    { name: 'Public Transport', icon: '🚌', color: '#9b59b6', day: 6 },
    { name: 'Housing', icon: '🏘️', color: '#e67e22', day: 7 },
    { name: 'Police', icon: '👮', color: '#2c3e50', day: 8 },
    { name: 'Fire Services', icon: '🚒', color: '#c0392b', day: 9 },
    { name: 'Agriculture', icon: '🌾', color: '#16a085', day: 10 },
    { name: 'Environment', icon: '🌳', color: '#27ae60', day: 11 },
    { name: 'Revenue', icon: '💰', color: '#8e44ad', day: 12 },
    { name: 'Social Welfare', icon: '🤝', color: '#e91e63', day: 13 },
    { name: 'Panchayat Raj', icon: '🏛️', color: '#ff9800', day: 14 },
    { name: 'Urban Development', icon: '🏗️', color: '#607d8b', day: 15 },
    { name: 'Tourism', icon: '🗿', color: '#00bcd4', day: 16 }
];

/**
 * Get department of the day based on current date
 * Rotates through all departments to give equal representation
 */
function getDepartmentOfDay() {
    const today = new Date();
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
    const deptIndex = dayOfYear % departments.length;
    return departments[deptIndex];
}

/**
 * Initialize department showcase
 */
function initDepartmentShowcase() {
    // Add department showcase banner
    const banner = document.createElement('div');
    banner.className = 'department-showcase';
    document.body.appendChild(banner);
    
    // Add floating department icons
    const iconsContainer = document.createElement('div');
    iconsContainer.className = 'department-icons-bg';
    
    // Add 10 random department icons
    for (let i = 0; i < 10; i++) {
        const randomDept = departments[Math.floor(Math.random() * departments.length)];
        const icon = document.createElement('div');
        icon.className = 'dept-icon';
        icon.textContent = randomDept.icon;
        icon.style.color = randomDept.color;
        iconsContainer.appendChild(icon);
    }
    
    document.body.appendChild(iconsContainer);
    
    // Add department of the day badge
    const deptOfDay = getDepartmentOfDay();
    const badge = document.createElement('div');
    badge.className = 'dept-of-day';
    badge.style.borderLeftColor = deptOfDay.color;
    badge.innerHTML = `
        <div class="dept-of-day-icon" style="color: ${deptOfDay.color};">
            ${deptOfDay.icon}
        </div>
        <div class="dept-of-day-text">
            <div class="dept-of-day-label">Department of the Day</div>
            <div class="dept-of-day-name" style="color: ${deptOfDay.color};">
                ${deptOfDay.name}
            </div>
        </div>
    `;
    
    document.body.appendChild(badge);
    
    // Add tooltip on hover
    badge.title = `Today we honor the ${deptOfDay.name} department for their dedicated service to our community.`;
}

/**
 * Add department-themed styling to sector cards
 */
function enhanceSectorCards() {
    const sectorMapping = {
        'Water Supply': 'water-supply',
        'Electricity': 'electricity',
        'Sanitation': 'sanitation',
        'Roads': 'roads',
        'Healthcare': 'healthcare',
        'Education': 'education',
        'Transport': 'transport',
        'Housing': 'housing',
        'Police': 'police',
        'Fire': 'fire',
        'Agriculture': 'agriculture',
        'Environment': 'environment',
        'Revenue': 'revenue',
        'Social Welfare': 'social-welfare',
        'Panchayat': 'panchayat',
        'Urban Development': 'urban-dev',
        'Tourism': 'tourism'
    };
    
    // Wait for DOM to be ready
    setTimeout(() => {
        document.querySelectorAll('.sector-card').forEach(card => {
            const title = card.querySelector('h3')?.textContent;
            if (title) {
                for (const [key, value] of Object.entries(sectorMapping)) {
                    if (title.includes(key)) {
                        card.setAttribute('data-dept', value);
                        break;
                    }
                }
            }
        });
    }, 100);
}

/**
 * Create department appreciation message
 */
function createAppreciationMessage() {
    const deptOfDay = getDepartmentOfDay();
    const messages = {
        'Water Supply': 'Ensuring clean water reaches every home 💧',
        'Electricity': 'Powering our nation, lighting our future ⚡',
        'Sanitation': 'Keeping our cities clean and healthy 🧹',
        'Roads & Infrastructure': 'Building pathways to progress 🛣️',
        'Healthcare': 'Caring for the health of our nation 🏥',
        'Education': 'Nurturing minds, building futures 📚',
        'Public Transport': 'Connecting communities, enabling mobility 🚌',
        'Housing': 'Creating homes, building dreams 🏘️',
        'Police': 'Protecting and serving with honor 👮',
        'Fire Services': 'Brave hearts, saving lives 🚒',
        'Agriculture': 'Feeding the nation, sustaining life 🌾',
        'Environment': 'Protecting nature for future generations 🌳',
        'Revenue': 'Managing resources for public welfare 💰',
        'Social Welfare': 'Empowering communities, supporting lives 🤝',
        'Panchayat Raj': 'Grassroots governance, people\'s power 🏛️',
        'Urban Development': 'Building smart, sustainable cities 🏗️',
        'Tourism': 'Showcasing India\'s rich heritage 🗿'
    };
    
    return messages[deptOfDay.name] || 'Serving the nation with dedication';
}

/**
 * Add appreciation banner (optional)
 */
function addAppreciationBanner() {
    const deptOfDay = getDepartmentOfDay();
    const message = createAppreciationMessage();
    
    // Only add to main pages (index, track, etc.)
    if (window.location.pathname.includes('index.html') || 
        window.location.pathname.includes('track.html')) {
        
        const banner = document.createElement('div');
        banner.style.cssText = `
            background: linear-gradient(135deg, ${deptOfDay.color}15 0%, ${deptOfDay.color}05 100%);
            border-left: 4px solid ${deptOfDay.color};
            padding: 12px 20px;
            margin: 20px auto;
            max-width: 1200px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        `;
        
        banner.innerHTML = `
            <div style="font-size: 2rem;">${deptOfDay.icon}</div>
            <div style="flex: 1;">
                <div style="font-size: 0.75rem; color: #6B7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Honoring Today
                </div>
                <div style="font-size: 1rem; font-weight: 700; color: ${deptOfDay.color}; margin-top: 2px;">
                    ${deptOfDay.name}
                </div>
                <div style="font-size: 0.875rem; color: #4B5563; margin-top: 4px;">
                    ${message}
                </div>
            </div>
        `;
        
        // Insert after header
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(banner, container.firstChild);
        }
    }
}

/**
 * Get all departments for display
 */
function getAllDepartments() {
    return departments;
}

/**
 * Initialize on page load
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initDepartmentShowcase();
        enhanceSectorCards();
        addAppreciationBanner();
    });
} else {
    initDepartmentShowcase();
    enhanceSectorCards();
    addAppreciationBanner();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        departments,
        getDepartmentOfDay,
        getAllDepartments,
        createAppreciationMessage
    };
}
