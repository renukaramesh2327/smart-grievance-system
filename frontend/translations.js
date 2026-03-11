// Translation System for Smart Grievance System
// Supports 12 Indian Languages

const translations = {
    en: {
        // Common
        'app_name': 'Smart Grievance System',
        'welcome': 'Welcome',
        'logout': 'Logout',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'view': 'View',
        'update': 'Update',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'loading': 'Loading...',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        
        // Auth
        'login': 'Login',
        'register': 'Register',
        'email': 'Email',
        'password': 'Password',
        'name': 'Name',
        'phone': 'Phone Number',
        'login_title': 'Login to Your Account',
        'register_title': 'Create New Account',
        'forgot_password': 'Forgot Password?',
        'dont_have_account': "Don't have an account?",
        'already_have_account': 'Already have an account?',
        
        // Dashboard
        'dashboard': 'Dashboard',
        'my_grievances': 'My Grievances',
        'submit_grievance': 'Submit Grievance',
        'track_grievance': 'Track Grievance',
        'profile': 'Profile',
        
        // Grievance
        'complaint_text': 'Describe your complaint',
        'location': 'Location',
        'department': 'Department',
        'status': 'Status',
        'submitted_on': 'Submitted On',
        'grievance_id': 'Grievance ID',
        'complaint_details': 'Complaint Details',
        
        // Status
        'received': 'Received',
        'assigned': 'Assigned to Department',
        'in_progress': 'Under Progress',
        'investigation': 'Investigation',
        'reviewed': 'Reviewed',
        'resolved': 'Resolved',
        'closed': 'Closed',
        
        // Officer
        'officer_dashboard': 'Officer Dashboard',
        'department_grievances': 'Department Grievances',
        'update_status': 'Update Status',
        'add_comment': 'Add Comment',
        
        // Admin
        'admin_dashboard': 'Admin Dashboard',
        'all_officers': 'All Officers',
        'create_officer': 'Create Officer',
        'analytics': 'Analytics',
        'total_grievances': 'Total Grievances',
        
        // Language
        'change_language': 'Change Language',
        'select_language': 'Select Language'
    },
    
    hi: {
        // Common
        'app_name': 'स्मार्ट शिकायत प्रणाली',
        'welcome': 'स्वागत है',
        'logout': 'लॉग आउट',
        'submit': 'जमा करें',
        'cancel': 'रद्द करें',
        'save': 'सहेजें',
        'edit': 'संपादित करें',
        'delete': 'हटाएं',
        'view': 'देखें',
        'update': 'अपडेट करें',
        'back': 'वापस',
        'next': 'अगला',
        'previous': 'पिछला',
        'loading': 'लोड हो रहा है...',
        'success': 'सफलता',
        'error': 'त्रुटि',
        'warning': 'चेतावनी',
        
        // Auth
        'login': 'लॉगिन',
        'register': 'पंजीकरण',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'name': 'नाम',
        'phone': 'फोन नंबर',
        'login_title': 'अपने खाते में लॉगिन करें',
        'register_title': 'नया खाता बनाएं',
        'forgot_password': 'पासवर्ड भूल गए?',
        'dont_have_account': 'खाता नहीं है?',
        'already_have_account': 'पहले से खाता है?',
        
        // Dashboard
        'dashboard': 'डैशबोर्ड',
        'my_grievances': 'मेरी शिकायतें',
        'submit_grievance': 'शिकायत दर्ज करें',
        'track_grievance': 'शिकायत ट्रैक करें',
        'profile': 'प्रोफ़ाइल',
        
        // Grievance
        'complaint_text': 'अपनी शिकायत का विवरण दें',
        'location': 'स्थान',
        'department': 'विभाग',
        'status': 'स्थिति',
        'submitted_on': 'जमा किया गया',
        'grievance_id': 'शिकायत आईडी',
        'complaint_details': 'शिकायत विवरण',
        
        // Status
        'received': 'प्राप्त',
        'assigned': 'विभाग को सौंपा गया',
        'in_progress': 'प्रगति में',
        'investigation': 'जांच',
        'reviewed': 'समीक्षा की गई',
        'resolved': 'हल हो गया',
        'closed': 'बंद',
        
        // Language
        'change_language': 'भाषा बदलें',
        'select_language': 'भाषा चुनें'
    },
    
    ta: {
        // Common
        'app_name': 'ஸ்மார்ட் குறைதீர்ப்பு அமைப்பு',
        'welcome': 'வரவேற்கிறோம்',
        'logout': 'வெளியேறு',
        'submit': 'சமர்ப்பிக்கவும்',
        'cancel': 'ரத்து செய்',
        'save': 'சேமி',
        'edit': 'திருத்து',
        'delete': 'நீக்கு',
        'view': 'பார்க்க',
        'update': 'புதுப்பிக்கவும்',
        'back': 'பின்',
        'next': 'அடுத்து',
        'previous': 'முந்தைய',
        'loading': 'ஏற்றுகிறது...',
        'success': 'வெற்றி',
        'error': 'பிழை',
        'warning': 'எச்சரிக்கை',
        
        // Auth
        'login': 'உள்நுழைய',
        'register': 'பதிவு செய்க',
        'email': 'மின்னஞ்சல்',
        'password': 'கடவுச்சொல்',
        'name': 'பெயர்',
        'phone': 'தொலைபேசி எண்',
        'login_title': 'உங்கள் கணக்கில் உள்நுழைக',
        'register_title': 'புதிய கணக்கை உருவாக்கவும்',
        
        // Dashboard
        'dashboard': 'டாஷ்போர்டு',
        'my_grievances': 'எனது குறைகள்',
        'submit_grievance': 'குறை சமர்ப்பிக்கவும்',
        'track_grievance': 'குறையைக் கண்காணிக்கவும்',
        'profile': 'சுயவிவரம்',
        
        // Grievance
        'complaint_text': 'உங்கள் புகாரை விவரிக்கவும்',
        'location': 'இடம்',
        'department': 'துறை',
        'status': 'நிலை',
        'submitted_on': 'சமர்ப்பிக்கப்பட்டது',
        'grievance_id': 'குறை ஐடி',
        
        // Language
        'change_language': 'மொழியை மாற்று',
        'select_language': 'மொழியைத் தேர்ந்தெடுக்கவும்'
    },
    
    te: {
        // Common
        'app_name': 'స్మార్ట్ ఫిర్యాదు వ్యవస్థ',
        'welcome': 'స్వాగతం',
        'logout': 'లాగౌట్',
        'submit': 'సమర్పించండి',
        'cancel': 'రద్దు చేయి',
        'save': 'సేవ్ చేయి',
        'edit': 'సవరించు',
        'view': 'చూడండి',
        'update': 'నవీకరించు',
        'back': 'వెనుకకు',
        
        // Auth
        'login': 'లాగిన్',
        'register': 'నమోదు',
        'email': 'ఇమెయిల్',
        'password': 'పాస్‌వర్డ్',
        'name': 'పేరు',
        'phone': 'ఫోన్ నంబర్',
        
        // Dashboard
        'dashboard': 'డాష్‌బోర్డ్',
        'my_grievances': 'నా ఫిర్యాదులు',
        'submit_grievance': 'ఫిర్యాదు సమర్పించండి',
        'profile': 'ప్రొఫైల్',
        
        // Language
        'change_language': 'భాషను మార్చండి',
        'select_language': 'భాషను ఎంచుకోండి'
    },
    
    bn: {
        // Common
        'app_name': 'স্মার্ট অভিযোগ সিস্টেম',
        'welcome': 'স্বাগতম',
        'logout': 'লগআউট',
        'submit': 'জমা দিন',
        'cancel': 'বাতিল',
        'save': 'সংরক্ষণ',
        'edit': 'সম্পাদনা',
        'view': 'দেখুন',
        'update': 'আপডেট',
        'back': 'পিছনে',
        
        // Auth
        'login': 'লগইন',
        'register': 'নিবন্ধন',
        'email': 'ইমেইল',
        'password': 'পাসওয়ার্ড',
        'name': 'নাম',
        'phone': 'ফোন নম্বর',
        
        // Dashboard
        'dashboard': 'ড্যাশবোর্ড',
        'my_grievances': 'আমার অভিযোগ',
        'submit_grievance': 'অভিযোগ জমা দিন',
        'profile': 'প্রোফাইল',
        
        // Language
        'change_language': 'ভাষা পরিবর্তন করুন',
        'select_language': 'ভাষা নির্বাচন করুন'
    },
    
    mr: {
        // Common
        'app_name': 'स्मार्ट तक्रार प्रणाली',
        'welcome': 'स्वागत आहे',
        'logout': 'लॉगआउट',
        'submit': 'सबमिट करा',
        'cancel': 'रद्द करा',
        'save': 'जतन करा',
        'edit': 'संपादित करा',
        'view': 'पहा',
        'update': 'अपडेट करा',
        
        // Auth
        'login': 'लॉगिन',
        'register': 'नोंदणी',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'name': 'नाव',
        'phone': 'फोन नंबर',
        
        // Dashboard
        'dashboard': 'डॅशबोर्ड',
        'my_grievances': 'माझ्या तक्रारी',
        'submit_grievance': 'तक्रार सबमिट करा',
        'profile': 'प्रोफाइल',
        
        // Language
        'change_language': 'भाषा बदला',
        'select_language': 'भाषा निवडा'
    },
    
    gu: {
        // Common
        'app_name': 'સ્માર્ટ ફરિયાદ સિસ્ટમ',
        'welcome': 'સ્વાગત છે',
        'logout': 'લૉગઆઉટ',
        'submit': 'સબમિટ કરો',
        'cancel': 'રદ કરો',
        'save': 'સાચવો',
        'edit': 'સંપાદિત કરો',
        'view': 'જુઓ',
        'update': 'અપડેટ કરો',
        
        // Auth
        'login': 'લૉગિન',
        'register': 'નોંધણી',
        'email': 'ઈમેલ',
        'password': 'પાસવર્ડ',
        'name': 'નામ',
        'phone': 'ફોન નંબર',
        
        // Dashboard
        'dashboard': 'ડેશબોર્ડ',
        'my_grievances': 'મારી ફરિયાદો',
        'submit_grievance': 'ફરિયાદ સબમિટ કરો',
        'profile': 'પ્રોફાઇલ',
        
        // Language
        'change_language': 'ભાષા બદલો',
        'select_language': 'ભાષા પસંદ કરો'
    },
    
    kn: {
        // Common
        'app_name': 'ಸ್ಮಾರ್ಟ್ ದೂರು ವ್ಯವಸ್ಥೆ',
        'welcome': 'ಸ್ವಾಗತ',
        'logout': 'ಲಾಗ್ಔಟ್',
        'submit': 'ಸಲ್ಲಿಸಿ',
        'cancel': 'ರದ್ದುಮಾಡಿ',
        'save': 'ಉಳಿಸಿ',
        'edit': 'ಸಂಪಾದಿಸಿ',
        'view': 'ವೀಕ್ಷಿಸಿ',
        'update': 'ನವೀಕರಿಸಿ',
        
        // Auth
        'login': 'ಲಾಗಿನ್',
        'register': 'ನೋಂದಣಿ',
        'email': 'ಇಮೇಲ್',
        'password': 'ಪಾಸ್‌ವರ್ಡ್',
        'name': 'ಹೆಸರು',
        'phone': 'ಫೋನ್ ಸಂಖ್ಯೆ',
        
        // Dashboard
        'dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'my_grievances': 'ನನ್ನ ದೂರುಗಳು',
        'submit_grievance': 'ದೂರು ಸಲ್ಲಿಸಿ',
        'profile': 'ಪ್ರೊಫೈಲ್',
        
        // Language
        'change_language': 'ಭಾಷೆ ಬದಲಿಸಿ',
        'select_language': 'ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ'
    },
    
    ml: {
        // Common
        'app_name': 'സ്മാർട്ട് പരാതി സംവിധാനം',
        'welcome': 'സ്വാഗതം',
        'logout': 'ലോഗൗട്ട്',
        'submit': 'സമർപ്പിക്കുക',
        'cancel': 'റദ്ദാക്കുക',
        'save': 'സംരക്ഷിക്കുക',
        'edit': 'എഡിറ്റ് ചെയ്യുക',
        'view': 'കാണുക',
        'update': 'അപ്ഡേറ്റ് ചെയ്യുക',
        
        // Auth
        'login': 'ലോഗിൻ',
        'register': 'രജിസ്റ്റർ',
        'email': 'ഇമെയിൽ',
        'password': 'പാസ്‌വേഡ്',
        'name': 'പേര്',
        'phone': 'ഫോൺ നമ്പർ',
        
        // Dashboard
        'dashboard': 'ഡാഷ്‌ബോർഡ്',
        'my_grievances': 'എന്റെ പരാതികൾ',
        'submit_grievance': 'പരാതി സമർപ്പിക്കുക',
        'profile': 'പ്രൊഫൈൽ',
        
        // Language
        'change_language': 'ഭാഷ മാറ്റുക',
        'select_language': 'ഭാഷ തിരഞ്ഞെടുക്കുക'
    },
    
    pa: {
        // Common
        'app_name': 'ਸਮਾਰਟ ਸ਼ਿਕਾਇਤ ਪ੍ਰਣਾਲੀ',
        'welcome': 'ਸੁਆਗਤ ਹੈ',
        'logout': 'ਲਾਗਆਉਟ',
        'submit': 'ਜਮ੍ਹਾਂ ਕਰੋ',
        'cancel': 'ਰੱਦ ਕਰੋ',
        'save': 'ਸੁਰੱਖਿਅਤ ਕਰੋ',
        'edit': 'ਸੰਪਾਦਿਤ ਕਰੋ',
        'view': 'ਦੇਖੋ',
        'update': 'ਅੱਪਡੇਟ ਕਰੋ',
        
        // Auth
        'login': 'ਲਾਗਇਨ',
        'register': 'ਰਜਿਸਟਰ',
        'email': 'ਈਮੇਲ',
        'password': 'ਪਾਸਵਰਡ',
        'name': 'ਨਾਮ',
        'phone': 'ਫ਼ੋਨ ਨੰਬਰ',
        
        // Dashboard
        'dashboard': 'ਡੈਸ਼ਬੋਰਡ',
        'my_grievances': 'ਮੇਰੀਆਂ ਸ਼ਿਕਾਇਤਾਂ',
        'submit_grievance': 'ਸ਼ਿਕਾਇਤ ਜਮ੍ਹਾਂ ਕਰੋ',
        'profile': 'ਪ੍ਰੋਫਾਈਲ',
        
        // Language
        'change_language': 'ਭਾਸ਼ਾ ਬਦਲੋ',
        'select_language': 'ਭਾਸ਼ਾ ਚੁਣੋ'
    },
    
    or: {
        // Common
        'app_name': 'ସ୍ମାର୍ଟ ଅଭିଯୋଗ ବ୍ୟବସ୍ଥା',
        'welcome': 'ସ୍ୱାଗତ',
        'logout': 'ଲଗଆଉଟ୍',
        'submit': 'ଦାଖଲ କରନ୍ତୁ',
        'cancel': 'ବାତିଲ କରନ୍ତୁ',
        'save': 'ସଞ୍ଚୟ କରନ୍ତୁ',
        'edit': 'ସମ୍ପାଦନା କରନ୍ତୁ',
        'view': 'ଦେଖନ୍ତୁ',
        'update': 'ଅପଡେଟ୍ କରନ୍ତୁ',
        
        // Auth
        'login': 'ଲଗଇନ୍',
        'register': 'ପଞ୍ଜୀକରଣ',
        'email': 'ଇମେଲ୍',
        'password': 'ପାସୱାର୍ଡ',
        'name': 'ନାମ',
        'phone': 'ଫୋନ୍ ନମ୍ବର',
        
        // Dashboard
        'dashboard': 'ଡ୍ୟାସବୋର୍ଡ',
        'my_grievances': 'ମୋର ଅଭିଯୋଗ',
        'submit_grievance': 'ଅଭିଯୋଗ ଦାଖଲ କରନ୍ତୁ',
        'profile': 'ପ୍ରୋଫାଇଲ୍',
        
        // Language
        'change_language': 'ଭାଷା ପରିବର୍ତ୍ତନ କରନ୍ତୁ',
        'select_language': 'ଭାଷା ଚୟନ କରନ୍ତୁ'
    },
    
    ur: {
        // Common
        'app_name': 'سمارٹ شکایت نظام',
        'welcome': 'خوش آمدید',
        'logout': 'لاگ آؤٹ',
        'submit': 'جمع کرائیں',
        'cancel': 'منسوخ کریں',
        'save': 'محفوظ کریں',
        'edit': 'ترمیم کریں',
        'view': 'دیکھیں',
        'update': 'اپ ڈیٹ کریں',
        
        // Auth
        'login': 'لاگ ان',
        'register': 'رجسٹر',
        'email': 'ای میل',
        'password': 'پاس ورڈ',
        'name': 'نام',
        'phone': 'فون نمبر',
        
        // Dashboard
        'dashboard': 'ڈیش بورڈ',
        'my_grievances': 'میری شکایات',
        'submit_grievance': 'شکایت جمع کرائیں',
        'profile': 'پروفائل',
        
        // Language
        'change_language': 'زبان تبدیل کریں',
        'select_language': 'زبان منتخب کریں'
    }
};

// Translation helper function
function translate(key, lang = null) {
    const currentLang = lang || localStorage.getItem('selectedLanguage') || localStorage.getItem('preferredLanguage') || 'en';
    return translations[currentLang]?.[key] || translations['en'][key] || key;
}

// Apply translations to page
function applyTranslations() {
    const currentLang = localStorage.getItem('selectedLanguage') || localStorage.getItem('preferredLanguage') || 'en';
    
    // Translate elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        const translation = translate(key, currentLang);
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = translation;
        } else {
            element.textContent = translation;
        }
    });
}

// Language switcher component
function createLanguageSwitcher() {
    const currentLang = localStorage.getItem('preferredLanguage') || 'en';
    const languages = [
        { code: 'en', name: 'English', flag: '🇬🇧' },
        { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
        { code: 'bn', name: 'বাংলা', flag: '🇮🇳' },
        { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
        { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
        { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
        { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' },
        { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' },
        { code: 'ml', name: 'മലയാളം', flag: '🇮🇳' },
        { code: 'pa', name: 'ਪੰਜਾਬੀ', flag: '🇮🇳' },
        { code: 'or', name: 'ଓଡ଼ିଆ', flag: '🇮🇳' },
        { code: 'ur', name: 'اردو', flag: '🇮🇳' }
    ];
    
    const currentLangObj = languages.find(l => l.code === currentLang) || languages[0];
    
    return `
        <div class="language-switcher" style="position: relative; display: inline-block;">
            <button class="language-btn" onclick="toggleLanguageMenu()" style="
                background: white;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 12px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            ">
                <span>${currentLangObj.flag}</span>
                <span>${currentLangObj.name}</span>
                <span style="font-size: 0.7rem;">▼</span>
            </button>
            <div id="languageMenu" class="language-menu" style="
                display: none;
                position: absolute;
                top: 100%;
                right: 0;
                margin-top: 8px;
                background: white;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                z-index: 1000;
                min-width: 200px;
                max-height: 400px;
                overflow-y: auto;
            ">
                ${languages.map(lang => `
                    <div class="language-option" onclick="changeLanguage('${lang.code}')" style="
                        padding: 12px 16px;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        transition: background 0.2s ease;
                        ${lang.code === currentLang ? 'background: rgba(255, 153, 51, 0.1);' : ''}
                    " onmouseover="this.style.background='rgba(255, 153, 51, 0.05)'" onmouseout="this.style.background='${lang.code === currentLang ? 'rgba(255, 153, 51, 0.1)' : 'white'}'">
                        <span style="font-size: 1.5rem;">${lang.flag}</span>
                        <span style="font-weight: ${lang.code === currentLang ? '600' : '400'};">${lang.name}</span>
                        ${lang.code === currentLang ? '<span style="margin-left: auto; color: #FF9933;">✓</span>' : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function toggleLanguageMenu() {
    const menu = document.getElementById('languageMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function changeLanguage(code) {
    localStorage.setItem('preferredLanguage', code);
    window.location.reload();
}

// Close language menu when clicking outside
document.addEventListener('click', (e) => {
    const languageSwitcher = document.querySelector('.language-switcher');
    if (languageSwitcher && !languageSwitcher.contains(e.target)) {
        const menu = document.getElementById('languageMenu');
        if (menu) menu.style.display = 'none';
    }
});

// Auto-apply translations on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTranslations);
} else {
    applyTranslations();
}
