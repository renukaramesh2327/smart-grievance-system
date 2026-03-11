/**
 * Department Image Requirements Configuration
 * 
 * Defines which departments REQUIRE image evidence for complaints
 * and which departments can accept complaints without images.
 * 
 * Analysis based on complaint type:
 * - Physical/Infrastructure issues → Images REQUIRED
 * - Administrative/Document issues → Images OPTIONAL
 */

const DEPARTMENT_IMAGE_REQUIREMENTS = {
    // ========================================
    // IMAGES REQUIRED (Physical/Visual Issues)
    // ========================================
    
    'Water Supply': {
        requiresImages: true,
        reason: 'Visual proof of leakage, contamination, or supply issues needed',
        examples: ['Leaking pipes', 'Contaminated water', 'No water supply', 'Broken taps']
    },
    
    'Electricity': {
        requiresImages: true,
        reason: 'Visual proof of electrical issues, damaged equipment, or power problems needed',
        examples: ['Broken poles', 'Exposed wires', 'Damaged meters', 'Power outage areas']
    },
    
    'Sanitation & Solid Waste': {
        requiresImages: true,
        reason: 'Visual proof of garbage, waste accumulation, or sanitation issues needed',
        examples: ['Garbage piles', 'Overflowing bins', 'Uncollected waste', 'Littering']
    },
    
    'Sewerage & Drainage': {
        requiresImages: true,
        reason: 'Visual proof of blockages, overflows, or drainage issues needed',
        examples: ['Blocked drains', 'Sewage overflow', 'Manholes', 'Waterlogging']
    },
    
    'Roads & Potholes': {
        requiresImages: true,
        reason: 'Visual proof of road damage, potholes, or infrastructure issues needed',
        examples: ['Potholes', 'Broken roads', 'Cracks', 'Road damage']
    },
    
    'Streetlights': {
        requiresImages: true,
        reason: 'Visual proof of non-functional or damaged streetlights needed',
        examples: ['Broken lights', 'Non-functional poles', 'Dark areas', 'Damaged fixtures']
    },
    
    'Traffic': {
        requiresImages: true,
        reason: 'Visual proof of traffic violations, congestion, or signal issues needed',
        examples: ['Traffic violations', 'Broken signals', 'Congestion', 'Illegal parking']
    },
    
    'Public Health': {
        requiresImages: true,
        reason: 'Visual proof of health hazards, unhygienic conditions, or medical issues needed',
        examples: ['Unhygienic conditions', 'Stagnant water', 'Disease outbreaks', 'Medical waste']
    },
    
    'Food Safety': {
        requiresImages: true,
        reason: 'Visual proof of food contamination, unhygienic practices, or violations needed',
        examples: ['Contaminated food', 'Unhygienic kitchens', 'Expired products', 'Violations']
    },
    
    'Environment': {
        requiresImages: true,
        reason: 'Visual proof of pollution, deforestation, or environmental damage needed',
        examples: ['Pollution', 'Illegal dumping', 'Deforestation', 'Environmental damage']
    },
    
    'Telecom / Network': {
        requiresImages: true,
        reason: 'Visual proof of infrastructure issues, damaged equipment, or network problems needed',
        examples: ['Damaged towers', 'Broken cables', 'Network issues', 'Infrastructure damage']
    },
    
    // ========================================
    // IMAGES OPTIONAL (Administrative/Document Issues)
    // ========================================
    
    'Police': {
        requiresImages: false,
        reason: 'Many police complaints are about incidents without physical evidence (theft, harassment, etc.)',
        examples: ['Theft reports', 'Harassment', 'Missing persons', 'General complaints'],
        note: 'Images helpful but not mandatory for all cases'
    },
    
    'Cyber Crime': {
        requiresImages: false,
        reason: 'Cyber crimes often involve digital evidence (screenshots optional), not physical proof',
        examples: ['Online fraud', 'Hacking', 'Identity theft', 'Cyber harassment'],
        note: 'Screenshots can be uploaded but not mandatory'
    },
    
    'Education': {
        requiresImages: false,
        reason: 'Education complaints often about policies, admissions, or administrative issues',
        examples: ['Admission issues', 'Fee disputes', 'Teaching quality', 'Infrastructure (optional images)'],
        note: 'Images helpful for infrastructure issues but not mandatory for all'
    },
    
    'Land & Revenue': {
        requiresImages: false,
        reason: 'Land and revenue issues are document-based, not visual',
        examples: ['Land disputes', 'Property tax', 'Revenue records', 'Documentation issues'],
        note: 'Document scans can be uploaded but not mandatory'
    },
    
    'Ration Card / PDS': {
        requiresImages: false,
        reason: 'Ration card issues are administrative and document-based',
        examples: ['Card not issued', 'Name corrections', 'Ration not received', 'Shop issues'],
        note: 'Images helpful for shop-related issues but not mandatory'
    },
    
    'RTO / Transport': {
        requiresImages: false,
        reason: 'RTO complaints often about licenses, registrations, and documents',
        examples: ['License issues', 'Vehicle registration', 'RC problems', 'Permit issues'],
        note: 'Images helpful for vehicle-related issues but not mandatory for all'
    }
};

/**
 * Check if a department requires images
 * @param {string} department - Department name
 * @returns {boolean} - True if images are required
 */
function doesDepartmentRequireImages(department) {
    const config = DEPARTMENT_IMAGE_REQUIREMENTS[department];
    return config ? config.requiresImages : true; // Default to required if not configured
}

/**
 * Get image requirement details for a department
 * @param {string} department - Department name
 * @returns {object} - Configuration object with reason and examples
 */
function getDepartmentImageRequirement(department) {
    return DEPARTMENT_IMAGE_REQUIREMENTS[department] || {
        requiresImages: true,
        reason: 'Visual evidence helps in faster resolution',
        examples: ['General complaints']
    };
}

/**
 * Get list of departments that require images
 * @returns {array} - Array of department names
 */
function getDepartmentsRequiringImages() {
    return Object.keys(DEPARTMENT_IMAGE_REQUIREMENTS)
        .filter(dept => DEPARTMENT_IMAGE_REQUIREMENTS[dept].requiresImages);
}

/**
 * Get list of departments where images are optional
 * @returns {array} - Array of department names
 */
function getDepartmentsWithOptionalImages() {
    return Object.keys(DEPARTMENT_IMAGE_REQUIREMENTS)
        .filter(dept => !DEPARTMENT_IMAGE_REQUIREMENTS[dept].requiresImages);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DEPARTMENT_IMAGE_REQUIREMENTS,
        doesDepartmentRequireImages,
        getDepartmentImageRequirement,
        getDepartmentsRequiringImages,
        getDepartmentsWithOptionalImages
    };
}
