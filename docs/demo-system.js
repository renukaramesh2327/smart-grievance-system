// =====================================================
// ENHANCED SMART GRIEVANCE SYSTEM
// =====================================================

const DEMO_MODE = true;

// Hierarchical User Structure
const DEMO_USERS = [
    { 
        id: 1,
        email: 'admin@grievance.gov', 
        password: 'admin123', 
        role: 'ADMIN', 
        name: 'System Administrator',
        phone: '9999999999',
        dob: '1985-05-15',
        gender: 'Male',
        address: 'Government Office, New Delhi',
        aadhaar: '****-****-4567',
        canEditAll: true,
        hierarchyLevel: 0
    },
    { 
        id: 2,
        email: 'electricity.head@grievance.gov', 
        password: 'head123', 
        role: 'DEPARTMENT_HEAD', 
        name: 'Electricity Dept Head', 
        department: 'Electricity',
        phone: '9876543210',
        dob: '1980-03-20',
        gender: 'Male',
        address: 'Electricity Board, Sector 5',
        aadhaar: '****-****-1234',
        location: 'Delhi',
        hierarchyLevel: 1
    },
    { 
        id: 3,
        email: 'electricity.officer@grievance.gov', 
        password: 'officer123', 
        role: 'OFFICER', 
        name: 'Field Officer - Electricity', 
        department: 'Electricity',
        reportsTo: 2,
        phone: '9876543211',
        dob: '1990-07-10',
        gender: 'Female',
        address: 'Field Office, Zone A',
        aadhaar: '****-****-5678',
        location: 'Delhi North',
        hierarchyLevel: 2
    },
    { 
        id: 4,
        email: 'electricity.worker@grievance.gov', 
        password: 'worker123', 
        role: 'FIELD_WORKER', 
        name: 'Lineman - Electricity', 
        department: 'Electricity',
        reportsTo: 3,
        phone: '9876543212',
        dob: '1995-11-25',
        gender: 'Male',
        address: 'Staff Quarters, Sector 12',
        aadhaar: '****-****-9012',
        location: 'Delhi North',
        hierarchyLevel: 3
    },
    { 
        id: 5,
        email: 'citizen@example.com', 
        password: 'citizen123', 
        role: 'CITIZEN', 
        name: 'Ramesh Kumar',
        phone: '9123456789',
        dob: '1992-08-15',
        gender: 'Male',
        address: '123, Green Park, Delhi',
        aadhaar: '',
        hierarchyLevel: 4
    }
];

// Language Translations
const TRANSLATIONS = {
    en: {
        name: 'English',
        home: 'Home',
        login: 'Login',
        register: 'Register',
        fileComplaint: 'File a Complaint',
        track: 'Track Complaint',
        profile: 'My Profile',
        logout: 'Logout',
        submit: 'Submit',
        cancel: 'Cancel',
        title: 'Title',
        description: 'Description',
        department: 'Department',
        status: 'Status',
        priority: 'Priority',
        uploadImage: 'Upload Image',
        grievanceId: 'Grievance ID',
        searchPlaceholder: 'Enter Grievance ID'
    },
    hi: {
        name: 'हिंदी',
        home: 'होम',
        login: 'लॉगिन',
        register: 'रजिस्टर',
        fileComplaint: 'शिकायत दर्ज करें',
        track: 'शिकायत ट्रैक करें',
        profile: 'मेरी प्रोफ़ाइल',
        logout: 'लॉगआउट',
        submit: 'जमा करें',
        cancel: 'रद्द करें',
        title: 'शीर्षक',
        description: 'विवरण',
        department: 'विभाग',
        status: 'स्थिति',
        priority: 'प्राथमिकता',
        uploadImage: 'छवि अपलोड करें',
        grievanceId: 'शिकायत ID',
        searchPlaceholder: 'शिकायत ID दर्ज करें'
    },
    ta: {
        name: 'தமிழ்',
        home: 'முகப்பு',
        login: 'உள்நுழைவு',
        register: 'பதிவு செய்க',
        fileComplaint: 'புகார் பதிவு செய்க',
        track: 'புகார் கண்காணிப்பு',
        profile: 'என் சுயவிவரம்',
        logout: 'வெளியேறு',
        submit: 'சமர்ப்பிக்கவும்',
        cancel: 'ரத்து செய்',
        title: 'தலைப்பு',
        description: 'விளக்கம்',
        department: 'துறை',
        status: 'நிலை',
        priority: 'முன்னுரிமை',
        uploadImage: 'படத்தை பதிவேற்றவும்',
        grievanceId: 'புகார் எண்',
        searchPlaceholder: 'புகார் எண்ணை உள்ளிடவும்'
    },
    te: {
        name: 'తెలుగు',
        home: 'హోమ్',
        login: 'లాగిన్',
        register: 'రిజిస్టర్',
        fileComplaint: 'ఫిర్యాదు దాఖలు చేయండి',
        track: 'ఫిర్యాదును ట్రాక్ చేయండి',
        profile: 'నా ప్రొఫైల్',
        logout: 'లాగ్అవుట్',
        submit: 'సమర్పించు',
        cancel: 'రద్దు చేయి',
        title: 'శీర్షిక',
        description: 'వివరణ',
        department: 'విభాగం',
        status: 'స్థితి',
        priority: 'ప్రాధాన్యత',
        uploadImage: 'చిత్రాన్ని అప్‌లోడ్ చేయండి',
        grievanceId: 'ఫిర్యాదు ID',
        searchPlaceholder: 'ఫిర్యాదు ID నమోదు చేయండి'
    },
    bn: {
        name: 'বাংলা',
        home: 'হোম',
        login: 'লগইন',
        register: 'নিবন্ধন',
        fileComplaint: 'অভিযোগ দাখিল করুন',
        track: 'অভিযোগ ট্র্যাক করুন',
        profile: 'আমার প্রোফাইল',
        logout: 'লগআউট',
        submit: 'জমা দিন',
        cancel: 'বাতিল',
        title: 'শিরোনাম',
        description: 'বিবরণ',
        department: 'বিভাগ',
        status: 'অবস্থা',
        priority: 'অগ্রাধিকার',
        uploadImage: 'ছবি আপলোড করুন',
        grievanceId: 'অভিযোগ আইডি',
        searchPlaceholder: 'অভিযোগ আইডি লিখুন'
    }
};

// Current Language
let currentLanguage = localStorage.getItem('appLanguage') || 'en';

// Department Keywords (Enhanced)
const DEPARTMENT_KEYWORDS = {
    'Electricity': ['electricity', 'power', 'light', 'pole', 'wire', 'transformer', 'blackout', 'voltage', 'meter', 'bill', 'current', 'supply', 'outage', 'shock'],
    'Water Supply': ['water', 'pipe', 'leak', 'tank', 'supply', 'tap', 'drainage', 'sewage', 'bore', 'pump', 'overflow', 'shortage', 'contamination'],
    'Roads': ['road', 'street', 'pothole', 'highway', 'pavement', 'footpath', 'bridge', 'traffic', 'signal', 'jam', 'accident', 'damage'],
    'Sanitation': ['garbage', 'waste', 'trash', 'cleanliness', 'sweeping', 'dustbin', 'smell', 'dirty', 'drain', 'toilet', 'hygiene'],
    'Public Transport': ['bus', 'metro', 'train', 'station', 'railway', 'transport', 'ticket', 'route', 'delay', 'crowd'],
    'Healthcare': ['hospital', 'doctor', 'medicine', 'health', 'clinic', 'ambulance', 'treatment', 'medical', 'emergency', 'patient'],
    'Education': ['school', 'college', 'teacher', 'student', 'education', 'class', 'exam', 'admission', 'fee', 'infrastructure'],
    'Police': ['police', 'theft', 'crime', 'security', 'law', 'FIR', 'complaint', 'officer', 'safety', 'harassment']
};

// Fraud Detection Keywords
const FRAUD_KEYWORDS = ['fake', 'fraud', 'scam', 'cheat', 'lie', 'false', 'spam', 'test123', 'asdf', 'qwerty', 'dummy', 'abcde', 'testing', 'check', 'trial', '123', 'xyz'];

// Profanity Filter
const PROFANITY_LIST = ['badword1', 'badword2'];

// =====================================================
// LANGUAGE MANAGEMENT
// =====================================================

function setLanguage(lang) {
    if (TRANSLATIONS[lang]) {
        currentLanguage = lang;
        localStorage.setItem('appLanguage', lang);
        return true;
    }
    return false;
}

function getLanguage() {
    return currentLanguage;
}

function translate(key) {
    return TRANSLATIONS[currentLanguage][key] || TRANSLATIONS['en'][key] || key;
}

function getAllLanguages() {
    return Object.keys(TRANSLATIONS).map(code => ({
        code: code,
        name: TRANSLATIONS[code].name
    }));
}

// =====================================================
// IMAGE VALIDATION & AI DETECTION
// =====================================================

function validateImage(file) {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (!validTypes.includes(file.type)) {
        return { valid: false, error: 'Invalid image type. Only JPG, PNG, WEBP allowed.' };
    }
    
    if (file.size > maxSize) {
        return { valid: false, error: 'Image too large. Maximum 5MB allowed.' };
    }
    
    return { valid: true };
}

function analyzeImageAI(imageData) {
    // Simulate AI image analysis
    const random = Math.random();
    const categories = ['Infrastructure Damage', 'Water Leakage', 'Electrical Issue', 'Road Damage', 'Garbage Accumulation', 'Public Property Damage'];
    const detected = categories[Math.floor(random * categories.length)];
    
    const isRelevant = random > 0.15; // 85% relevant
    const confidence = Math.round(70 + Math.random() * 30);
    
    return {
        detected: detected,
        confidence: confidence,
        isRelevant: isRelevant,
        tags: [detected.toLowerCase(), 'public', 'infrastructure'],
        verdict: isRelevant ? 'GENUINE' : 'SUSPICIOUS',
        reason: isRelevant ? 'Image appears to show actual infrastructure issue' : 'Image does not show clear evidence of reported issue'
    };
}

// =====================================================
// PROFILE MANAGEMENT
// =====================================================

function getUserProfile(userId) {
    const users = JSON.parse(localStorage.getItem('allUsers') || '[]');
    const demoUser = DEMO_USERS.find(u => u.id === userId);
    const registeredUser = users.find(u => u.id === userId);
    return registeredUser || demoUser;
}

function updateUserProfile(userId, updates, requiresVerification = false) {
    const user = getUser();
    
    // Check permissions
    if (user.role !== 'ADMIN' && user.id !== userId) {
        throw new Error('Permission denied');
    }
    
    // Email/Phone change requires verification (unless admin)
    if (requiresVerification && user.role !== 'ADMIN') {
        if (updates.email || updates.phone) {
            return {
                success: false,
                requiresOTP: true,
                message: 'Email/Phone change requires OTP verification',
                pendingUpdates: updates
            };
        }
    }
    
    // Update user in allUsers
    let users = JSON.parse(localStorage.getItem('allUsers') || '[]');
    const userIndex = users.findIndex(u => u.id === userId);
    
    if (userIndex >= 0) {
        users[userIndex] = { ...users[userIndex], ...updates };
        localStorage.setItem('allUsers', JSON.stringify(users));
        
        if (user.id === userId) {
            setUser(users[userIndex]);
        }
        
        return { success: true, user: users[userIndex] };
    }
    
    // Demo user (not in allUsers) - update session only
    if (user.id === userId) {
        const currentUser = getUser();
        const updated = { ...currentUser, ...updates };
        setUser(updated);
        return { success: true, user: updated };
    }
    
    throw new Error('User not found');
}

function requestOTPForChange(field, value) {
    // Simulate OTP request
    const otp = Math.floor(100000 + Math.random() * 900000);
    localStorage.setItem('pendingOTP', JSON.stringify({
        otp: otp,
        field: field,
        value: value,
        expiresAt: Date.now() + 300000 // 5 minutes
    }));
    
    console.log(`📱 OTP Sent: ${otp} for ${field} change to ${value}`);
    return { success: true, message: 'OTP sent successfully' };
}

function verifyOTP(otp) {
    const pending = JSON.parse(localStorage.getItem('pendingOTP') || '{}');
    
    if (!pending.otp) {
        return { success: false, message: 'No pending verification' };
    }
    
    if (Date.now() > pending.expiresAt) {
        localStorage.removeItem('pendingOTP');
        return { success: false, message: 'OTP expired' };
    }
    
    if (parseInt(otp) === pending.otp) {
        localStorage.removeItem('pendingOTP');
        return { success: true, field: pending.field, value: pending.value };
    }
    
    return { success: false, message: 'Invalid OTP' };
}

// =====================================================
// AI CLASSIFICATION ENGINE
// =====================================================

function classifyDepartmentAI(title, description) {
    const text = (title + ' ' + description).toLowerCase();
    const scores = {};
    
    for (const [dept, keywords] of Object.entries(DEPARTMENT_KEYWORDS)) {
        let score = 0;
        keywords.forEach(keyword => {
            const regex = new RegExp(keyword, 'gi');
            const matches = text.match(regex);
            score += matches ? matches.length * 2 : 0;
        });
        scores[dept] = score;
    }
    
    let maxScore = 0;
    let detectedDept = 'Other';
    for (const [dept, score] of Object.entries(scores)) {
        if (score > maxScore) {
            maxScore = score;
            detectedDept = dept;
        }
    }
    
    return {
        department: detectedDept,
        confidence: maxScore > 0 ? Math.min((maxScore / 8) * 100, 100) : 0,
        scores: scores,
        allScores: scores
    };
}

// =====================================================
// FRAUD DETECTION ENGINE
// =====================================================

function detectFraud(title, description, userHistory) {
    const issues = [];
    const text = (title + ' ' + description).toLowerCase();
    
    FRAUD_KEYWORDS.forEach(keyword => {
        if (text.includes(keyword)) {
            issues.push(`Suspicious keyword: "${keyword}"`);
        }
    });
    
    PROFANITY_LIST.forEach(word => {
        if (text.includes(word)) {
            issues.push('Inappropriate language detected');
        }
    });
    
    if (description.length < 20) {
        issues.push('Description too short (minimum 20 characters)');
    }
    
    if (/(.)\1{5,}/.test(text)) {
        issues.push('Suspicious pattern: repeated characters');
    }
    
    if (/^[a-z]{1,3}$/i.test(title.trim())) {
        issues.push('Title appears to be gibberish');
    }
    
    if (userHistory && userHistory.length > 0) {
        const recentSimilar = userHistory.filter(c => 
            c.title.toLowerCase() === title.toLowerCase() && 
            (Date.now() - new Date(c.createdAt).getTime()) < 3600000
        );
        if (recentSimilar.length > 0) {
            issues.push('Duplicate complaint within 1 hour');
        }
        
        const recent10min = userHistory.filter(c => 
            (Date.now() - new Date(c.createdAt).getTime()) < 600000
        );
        if (recent10min.length >= 5) {
            issues.push('Spam: Too many complaints in 10 minutes');
        }
    }
    
    const fraudScore = Math.min((issues.length / 7) * 100, 100);
    
    return {
        isFraudulent: fraudScore > 30,
        fraudScore: Math.round(fraudScore),
        issues: issues,
        severity: fraudScore > 60 ? 'HIGH' : fraudScore > 30 ? 'MEDIUM' : 'LOW'
    };
}

// =====================================================
// PRIORITY CALCULATION
// =====================================================

function calculatePriority(title, description, department, hasImage) {
    const urgentKeywords = ['emergency', 'urgent', 'danger', 'fire', 'accident', 'leak', 'broken', 'critical', 'severe'];
    const text = (title + ' ' + description).toLowerCase();
    
    let urgencyScore = 0;
    urgentKeywords.forEach(keyword => {
        if (text.includes(keyword)) urgencyScore += 1;
    });
    
    const highPriorityDepts = ['Healthcare', 'Police', 'Electricity'];
    if (highPriorityDepts.includes(department)) urgencyScore += 1;
    
    if (hasImage) urgencyScore += 0.5;
    
    if (urgencyScore >= 2.5) return 'High';
    if (urgencyScore >= 1) return 'Medium';
    return 'Low';
}

// Continue in next message due to length...

// =====================================================
// HIERARCHICAL COMPLAINT MANAGEMENT
// =====================================================

function assignToHierarchy(grievance) {
    // Find department head
    const deptHead = DEMO_USERS.find(u => 
        u.role === 'DEPARTMENT_HEAD' && 
        u.department === grievance.department &&
        u.location === grievance.location
    );
    
    if (deptHead) {
        grievance.assignedTo = deptHead.id;
        grievance.currentHandler = deptHead.id;
        grievance.hierarchyLevel = 1;
    }
    
    return grievance;
}

function escalateComplaint(grievanceId, reason) {
    const grievances = getDemoGrievances();
    const grievance = grievances.find(g => g.id === grievanceId);
    
    if (!grievance) throw new Error('Grievance not found');
    
    // Find next level in hierarchy
    const currentHandler = DEMO_USERS.find(u => u.id === grievance.currentHandler);
    if (currentHandler && currentHandler.reportsTo) {
        const supervisor = DEMO_USERS.find(u => u.id === currentHandler.reportsTo);
        if (supervisor) {
            grievance.currentHandler = supervisor.id;
            grievance.hierarchyLevel = supervisor.hierarchyLevel;
            grievance.escalated = true;
            grievance.escalationReason = reason;
            
            grievance.updates.push({
                status: 'Escalated',
                date: new Date().toISOString(),
                comment: `Escalated to ${supervisor.name}. Reason: ${reason}`,
                officer: currentHandler.name,
                level: supervisor.hierarchyLevel
            });
            
            localStorage.setItem('demoGrievances', JSON.stringify(grievances));
            
            addNotification(grievance.userId, {
                type: 'escalation',
                message: `Your complaint ${grievanceId} has been escalated to higher authority`,
                grievanceId: grievanceId
            });
            
            return grievance;
        }
    }
    
    throw new Error('Cannot escalate further');
}

function assignToFieldWorker(grievanceId, workerId) {
    const grievances = getDemoGrievances();
    const grievance = grievances.find(g => g.id === grievanceId);
    
    if (!grievance) throw new Error('Grievance not found');
    
    const worker = DEMO_USERS.find(u => u.id === workerId);
    if (!worker) throw new Error('Worker not found');
    
    grievance.assignedWorker = workerId;
    grievance.currentHandler = workerId;
    
    grievance.updates.push({
        status: 'Assigned to Field Worker',
        date: new Date().toISOString(),
        comment: `Assigned to ${worker.name} for resolution`,
        officer: getUser().name,
        workerId: workerId
    });
    
    localStorage.setItem('demoGrievances', JSON.stringify(grievances));
    
    addNotification(grievance.userId, {
        type: 'assignment',
        message: `Your complaint ${grievanceId} has been assigned to field worker`,
        grievanceId: grievanceId
    });
    
    return grievance;
}

// =====================================================
// CORE SYSTEM FUNCTIONS
// =====================================================

function getDemoGrievances() {
    const stored = localStorage.getItem('demoGrievances');
    if (stored) return JSON.parse(stored);
    
    const demo = [
        {
            id: 'GRV001',
            title: 'Street Light Not Working',
            description: 'Street light near my house has been out for 2 weeks causing safety issues',
            department: 'Electricity',
            location: 'Delhi North',
            status: 'Under Progress',
            priority: 'Medium',
            userId: 5,
            aiDetected: true,
            aiConfidence: 95,
            fraudScore: 0,
            currentHandler: 3,
            hierarchyLevel: 2,
            imageUrl: null,
            createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
            updates: [
                { status: 'Received', date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), comment: 'Complaint received', officer: 'System', level: 0 },
                { status: 'Assigned to Department', date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), comment: 'Assigned to Electricity Dept Head', officer: 'System', level: 1 },
                { status: 'Under Progress', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), comment: 'Field officer assigned, inspection scheduled', officer: 'Field Officer', level: 2 }
            ]
        }
    ];
    
    localStorage.setItem('demoGrievances', JSON.stringify(demo));
    return demo;
}

function getToken() { return localStorage.getItem('token'); }
function setToken(token) { localStorage.setItem('token', token); }
function removeToken() { localStorage.removeItem('token'); }

function getUser() {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    return JSON.parse(userStr);
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function removeUser() {
    localStorage.removeItem('user');
}

function isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true' && getUser() !== null;
}

function logout() {
    removeToken();
    removeUser();
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'login.html';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

function requireRole(allowedRoles) {
    if (!requireAuth()) return false;
    const user = getUser();
    if (!allowedRoles.includes(user.role)) {
        alert('Access denied!');
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function formatDateOnly(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
}

function getStatusBadgeClass(status) {
    const statusMap = {
        'Received': 'badge-received',
        'Assigned to Department': 'badge-assigned',
        'Under Progress': 'badge-progress',
        'Investigation': 'badge-investigation',
        'Escalated': 'badge-escalated',
        'Resolved': 'badge-resolved',
        'Closed': 'badge-closed'
    };
    return statusMap[status] || 'badge-received';
}

function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) {
        console.log(message);
        return;
    }
    const alertClass = `alert-${type}`;
    const alertHTML = `<div class="alert ${alertClass} show">${message}</div>`;
    alertContainer.innerHTML = alertHTML;
    if (duration > 0) {
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.classList.remove('show');
                setTimeout(() => {
                    if (alertContainer.innerHTML.includes(message)) {
                        alertContainer.innerHTML = '';
                    }
                }, 300);
            }
        }, duration);
    }
}

function generateId(prefix = 'GRV') {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 1000);
    return `${prefix}${timestamp}${random}`;
}

function getUserGrievances() {
    const user = getUser();
    if (!user) return [];
    const allGrievances = getDemoGrievances();
    if (user.role === 'ADMIN') {
        return allGrievances;
    } else if (user.role === 'DEPARTMENT_HEAD' || user.role === 'OFFICER' || user.role === 'FIELD_WORKER') {
        return allGrievances.filter(g => 
            g.department === user.department && 
            (g.currentHandler === user.id || g.assignedTo === user.id || g.assignedWorker === user.id)
        );
    } else {
        return allGrievances.filter(g => g.userId === user.id);
    }
}

function submitGrievance(grievanceData) {
    const user = getUser();
    if (!user) throw new Error('Please login to submit a grievance');
    
    const userHistory = getUserGrievances();
    
    const aiResult = classifyDepartmentAI(grievanceData.title, grievanceData.description);
    const fraudResult = detectFraud(grievanceData.title, grievanceData.description, userHistory);
    
    if (fraudResult.fraudScore > 60) {
        throw new Error('Complaint blocked: ' + fraudResult.issues.join(', '));
    }
    
    const finalDepartment = aiResult.confidence > 50 ? aiResult.department : grievanceData.department;
    const priority = calculatePriority(grievanceData.title, grievanceData.description, finalDepartment, !!grievanceData.imageUrl);
    
    const allGrievances = getDemoGrievances();
    
    let newGrievance = {
        id: generateId('GRV'),
        ...grievanceData,
        department: finalDepartment,
        userId: user.id,
        status: 'Received',
        priority: priority,
        aiDetected: aiResult.confidence > 50,
        aiConfidence: Math.round(aiResult.confidence),
        fraudScore: fraudResult.fraudScore,
        hierarchyLevel: 0,
        createdAt: new Date().toISOString(),
        updates: [{
            status: 'Received',
            date: new Date().toISOString(),
            comment: `Complaint received. ${aiResult.confidence > 50 ? `AI detected: ${finalDepartment} (${Math.round(aiResult.confidence)}% confidence)` : ''}`,
            officer: 'System',
            level: 0
        }]
    };
    
    newGrievance = assignToHierarchy(newGrievance);
    
    allGrievances.push(newGrievance);
    localStorage.setItem('demoGrievances', JSON.stringify(allGrievances));
    
    addNotification(user.id, {
        type: 'success',
        message: `Complaint ${newGrievance.id} submitted successfully`,
        grievanceId: newGrievance.id
    });
    
    console.log(`📧 Email confirmation sent for ${newGrievance.id}`);
    console.log(`📱 SMS sent to ${user.phone} for complaint ${newGrievance.id}`);
    
    return newGrievance;
}

function updateGrievanceStatus(grievanceId, status, comment, proofImageUrl = null) {
    const allGrievances = getDemoGrievances();
    const grievance = allGrievances.find(g => g.id === grievanceId);
    if (!grievance) throw new Error('Grievance not found');
    
    const user = getUser();
    grievance.status = status;
    grievance.updates.push({
        status: status,
        date: new Date().toISOString(),
        comment: comment || `Status updated to ${status}`,
        officer: user ? user.name : 'Officer',
        level: user ? user.hierarchyLevel : 0,
        proofImageUrl: proofImageUrl
    });
    
    if (status === 'Resolved' || status === 'Closed') {
        grievance.resolvedAt = new Date().toISOString();
    }
    
    localStorage.setItem('demoGrievances', JSON.stringify(allGrievances));
    
    addNotification(grievance.userId, {
        type: 'update',
        message: `Complaint ${grievanceId} status: ${status}`,
        grievanceId: grievanceId
    });
    
    console.log(`📧 Status update email sent for ${grievanceId}`);
    console.log(`📱 SMS sent: Complaint ${grievanceId} - ${status}`);
    
    return grievance;
}

function trackGrievance(grievanceId) {
    const allGrievances = getDemoGrievances();
    return allGrievances.find(g => g.id.toUpperCase() === grievanceId.toUpperCase());
}

function getStatistics() {
    const grievances = getDemoGrievances();
    const user = getUser();
    let relevantGrievances = grievances;
    if (user && (user.role === 'OFFICER' || user.role === 'DEPARTMENT_HEAD' || user.role === 'FIELD_WORKER')) {
        relevantGrievances = grievances.filter(g => g.department === user.department);
    } else if (user && user.role === 'CITIZEN') {
        relevantGrievances = grievances.filter(g => g.userId === user.id);
    }
    return {
        total: relevantGrievances.length,
        pending: relevantGrievances.filter(g => !['Resolved', 'Closed'].includes(g.status)).length,
        resolved: relevantGrievances.filter(g => g.status === 'Resolved').length,
        inProgress: relevantGrievances.filter(g => g.status === 'Under Progress').length
    };
}

// Notification System
function getNotifications(userId) {
    const notifications = JSON.parse(localStorage.getItem('notifications') || '{}');
    return notifications[userId] || [];
}

function addNotification(userId, notification) {
    const notifications = JSON.parse(localStorage.getItem('notifications') || '{}');
    if (!notifications[userId]) notifications[userId] = [];
    notifications[userId].unshift({ ...notification, id: Date.now(), timestamp: new Date().toISOString(), read: false });
    notifications[userId] = notifications[userId].slice(0, 50);
    localStorage.setItem('notifications', JSON.stringify(notifications));
}

function markNotificationRead(userId, notificationId) {
    const notifications = JSON.parse(localStorage.getItem('notifications') || '{}');
    if (notifications[userId]) {
        const notif = notifications[userId].find(n => n.id === notificationId);
        if (notif) notif.read = true;
        localStorage.setItem('notifications', JSON.stringify(notifications));
    }
}

function getUnreadCount(userId) {
    const notifications = getNotifications(userId);
    return notifications.filter(n => !n.read).length;
}

// Comment System
function getComments(grievanceId, updateIndex) {
    const key = `comments_${grievanceId}_${updateIndex}`;
    return JSON.parse(localStorage.getItem(key) || '[]');
}

function addComment(grievanceId, updateIndex, comment, userId) {
    const key = `comments_${grievanceId}_${updateIndex}`;
    const comments = getComments(grievanceId, updateIndex);
    const user = getUser();
    
    const newComment = {
        id: Date.now(),
        userId: userId,
        userName: user.name,
        userRole: user.role,
        text: comment,
        timestamp: new Date().toISOString()
    };
    
    comments.push(newComment);
    localStorage.setItem(key, JSON.stringify(comments));
    
    if (user.role !== 'CITIZEN') {
        const grievance = trackGrievance(grievanceId);
        if (grievance) {
            addNotification(grievance.userId, {
                type: 'comment',
                message: `${user.name} replied to your complaint ${grievanceId}`,
                grievanceId: grievanceId,
                comment: comment
            });
            console.log(`📧 Comment email sent for ${grievanceId}`);
        }
    }
    
    return newComment;
}

function getCommentsCount(grievanceId, updateIndex) {
    return getComments(grievanceId, updateIndex).length;
}

// Initialize
function initializePage() {
    const user = getUser();
    if (!user) return;
    const userNameEl = document.getElementById('userName');
    const userRoleEl = document.getElementById('userRole');
    if (userNameEl) userNameEl.textContent = user.name;
    if (userRoleEl) userRoleEl.textContent = user.role;
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePage);
} else {
    initializePage();
}

// Export everything
window.grievanceSystem = {
    isLoggedIn, getUser, setUser, logout, requireAuth, requireRole,
    getUserGrievances, submitGrievance, updateGrievanceStatus, trackGrievance, getStatistics,
    formatDate, formatDateOnly, getStatusBadgeClass, showAlert,
    classifyDepartmentAI, detectFraud, analyzeImageAI, calculatePriority, validateImage,
    getNotifications, addNotification, markNotificationRead, getUnreadCount,
    getComments, addComment, getCommentsCount,
    getUserProfile, updateUserProfile, requestOTPForChange, verifyOTP,
    escalateComplaint, assignToFieldWorker, assignToHierarchy,
    setLanguage, getLanguage, translate, getAllLanguages,
    DEMO_MODE, DEMO_USERS, TRANSLATIONS
};

window.DEMO_USERS = DEMO_USERS;
