/**
 * Simple Page Translator
 * Translates common text on the page
 */

// Common translations for all pages
const commonTranslations = {
    en: {
        'Smart Grievance System': 'Smart Grievance System',
        'Logout': 'Logout',
        'Profile': 'Profile',
        'Dashboard': 'Dashboard',
        'Submit Grievance': 'Submit Grievance',
        'My Grievances': 'My Grievances',
        'Track Grievance': 'Track Grievance',
        'Login': 'Login',
        'Register': 'Register',
        'Email': 'Email',
        'Password': 'Password',
        'Submit': 'Submit',
        'Update': 'Update',
        'Cancel': 'Cancel',
        'Save': 'Save',
        'Back': 'Back',
        'View': 'View',
        'Status': 'Status',
        'Department': 'Department',
        'Location': 'Location',
        'Date': 'Date',
        'Action': 'Action',
        'Actions': 'Actions',
        'Complaint': 'Complaint',
        'Description': 'Description',
        'Submitted On': 'Submitted On',
        'Last Updated': 'Last Updated'
    },
    hi: {
        'Smart Grievance System': 'स्मार्ट शिकायत प्रणाली',
        'Logout': 'लॉग आउट',
        'Profile': 'प्रोफ़ाइल',
        'Dashboard': 'डैशबोर्ड',
        'Submit Grievance': 'शिकायत दर्ज करें',
        'My Grievances': 'मेरी शिकायतें',
        'Track Grievance': 'शिकायत ट्रैक करें',
        'Login': 'लॉगिन',
        'Register': 'पंजीकरण',
        'Email': 'ईमेल',
        'Password': 'पासवर्ड',
        'Submit': 'जमा करें',
        'Update': 'अपडेट',
        'Cancel': 'रद्द करें',
        'Save': 'सहेजें',
        'Back': 'वापस',
        'View': 'देखें',
        'Status': 'स्थिति',
        'Department': 'विभाग',
        'Location': 'स्थान',
        'Date': 'तारीख',
        'Action': 'कार्रवाई',
        'Actions': 'कार्रवाई',
        'Complaint': 'शिकायत',
        'Description': 'विवरण',
        'Submitted On': 'जमा किया गया',
        'Last Updated': 'अंतिम अपडेट'
    },
    ta: {
        'Smart Grievance System': 'ஸ்மார்ட் குறைதீர்ப்பு அமைப்பு',
        'Logout': 'வெளியேறு',
        'Profile': 'சுயவிவரம்',
        'Dashboard': 'டாஷ்போர்டு',
        'Submit Grievance': 'குறை சமர்ப்பிக்கவும்',
        'My Grievances': 'எனது குறைகள்',
        'Track Grievance': 'குறையைக் கண்காணிக்கவும்',
        'Login': 'உள்நுழைய',
        'Register': 'பதிவு செய்யவும்',
        'Email': 'மின்னஞ்சல்',
        'Password': 'கடவுச்சொல்',
        'Submit': 'சமர்ப்பிக்கவும்',
        'Update': 'புதுப்பிக்கவும்',
        'Cancel': 'ரத்து செய்யவும்',
        'Save': 'சேமிக்கவும்',
        'Back': 'பின்',
        'View': 'பார்க்கவும்',
        'Status': 'நிலை',
        'Department': 'துறை',
        'Location': 'இடம்',
        'Date': 'தேதி',
        'Action': 'நடவடிக்கை',
        'Actions': 'நடவடிக்கைகள்',
        'Complaint': 'குறை',
        'Description': 'விவரம்',
        'Submitted On': 'சமர்ப்பிக்கப்பட்டது',
        'Last Updated': 'கடைசியாக புதுப்பிக்கப்பட்டது'
    },
    te: {
        'Smart Grievance System': 'స్మార్ట్ ఫిర్యాదు వ్యవస్థ',
        'Logout': 'లాగ్అవుట్',
        'Profile': 'ప్రొఫైల్',
        'Dashboard': 'డాష్‌బోర్డ్',
        'Submit Grievance': 'ఫిర్యాదు సమర్పించండి',
        'My Grievances': 'నా ఫిర్యాదులు',
        'Track Grievance': 'ఫిర్యాదును ట్రాక్ చేయండి',
        'Login': 'లాగిన్',
        'Register': 'నమోదు',
        'Email': 'ఇమెయిల్',
        'Password': 'పాస్‌వర్డ్',
        'Submit': 'సమర్పించండి',
        'Update': 'నవీకరించండి',
        'Cancel': 'రద్దు చేయండి',
        'Save': 'సేవ్ చేయండి',
        'Back': 'వెనుకకు',
        'View': 'చూడండి',
        'Status': 'స్థితి',
        'Department': 'విభాగం',
        'Location': 'స్థానం',
        'Date': 'తేదీ',
        'Action': 'చర్య',
        'Actions': 'చర్యలు',
        'Complaint': 'ఫిర్యాదు',
        'Description': 'వివరణ',
        'Submitted On': 'సమర్పించబడింది',
        'Last Updated': 'చివరిగా నవీకరించబడింది'
    }
};

// Translate page content
function translatePage(langCode) {
    if (!commonTranslations[langCode]) {
        console.warn('Translation not available for:', langCode);
        return;
    }
    
    const translations = commonTranslations[langCode];
    
    // Translate all text nodes
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode: function(node) {
                // Skip script and style tags
                if (node.parentElement.tagName === 'SCRIPT' || 
                    node.parentElement.tagName === 'STYLE') {
                    return NodeFilter.FILTER_REJECT;
                }
                // Only process non-empty text nodes
                if (node.textContent.trim().length > 0) {
                    return NodeFilter.FILTER_ACCEPT;
                }
                return NodeFilter.FILTER_REJECT;
            }
        }
    );
    
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    // Translate each text node
    textNodes.forEach(textNode => {
        const originalText = textNode.textContent.trim();
        if (translations[originalText]) {
            textNode.textContent = textNode.textContent.replace(originalText, translations[originalText]);
        }
    });
    
    // Translate placeholders
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(element => {
        const placeholder = element.placeholder;
        if (translations[placeholder]) {
            element.placeholder = translations[placeholder];
        }
    });
    
    // Translate button text
    document.querySelectorAll('button').forEach(button => {
        const text = button.textContent.trim();
        if (translations[text]) {
            button.textContent = translations[text];
        }
    });
    
    // Update page language attribute
    document.documentElement.setAttribute('lang', langCode);
    
    console.log('Page translated to:', langCode);
}

// Listen for language changes
window.addEventListener('languageChanged', (event) => {
    const langCode = event.detail.language;
    translatePage(langCode);
});

// Apply translation on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        if (currentLang !== 'en') {
            translatePage(currentLang);
        }
    });
} else {
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    if (currentLang !== 'en') {
        translatePage(currentLang);
    }
}
