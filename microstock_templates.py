"""
Microstock-optimized prompt templates and keywords for maximum commercial appeal
"""

# High-demand microstock categories and keywords
MICROSTOCK_CATEGORIES = {
    "business": {
        "keywords": ["professional", "corporate", "meeting", "presentation", "teamwork", "success", "growth", "strategy", "leadership", "innovation"],
        "scenarios": ["business meeting", "office environment", "handshake", "team collaboration", "professional portrait", "workplace diversity", "success celebration", "strategic planning"],
        "lighting": "professional office lighting, clean modern office, natural window light",
        "composition": "corporate headshot style, professional business environment, modern office setting"
    },
    
    "technology": {
        "keywords": ["digital", "innovation", "smart", "modern", "connected", "AI", "data", "cloud", "mobile", "future"],
        "scenarios": ["person using laptop", "smartphone interaction", "digital interface", "tech startup", "remote work", "digital transformation", "smart home"],
        "lighting": "modern tech lighting, blue screen glow, clean minimalist setup",
        "composition": "tech-focused composition, modern clean background, device interaction"
    },
    
    "lifestyle": {
        "keywords": ["wellness", "balance", "happiness", "family", "health", "fitness", "relaxation", "joy", "home", "comfort"],
        "scenarios": ["family time", "healthy lifestyle", "work-life balance", "morning routine", "home comfort", "wellness activity", "leisure time"],
        "lighting": "natural lifestyle lighting, warm home atmosphere, golden hour",
        "composition": "lifestyle photography style, comfortable home setting, natural poses"
    },
    
    "healthcare": {
        "keywords": ["medical", "health", "wellness", "care", "professional", "treatment", "prevention", "diagnosis", "therapy", "healing"],
        "scenarios": ["medical consultation", "healthcare professional", "wellness checkup", "medical technology", "health assessment", "patient care"],
        "lighting": "clinical professional lighting, clean medical environment, reassuring atmosphere",
        "composition": "medical photography style, professional healthcare setting, trust-building"
    },
    
    "education": {
        "keywords": ["learning", "education", "knowledge", "study", "growth", "development", "skill", "training", "academic", "research"],
        "scenarios": ["student learning", "online education", "skill development", "academic success", "educational technology", "knowledge sharing"],
        "lighting": "educational environment lighting, inspiring learning space, focused study lighting",
        "composition": "educational photography style, learning-focused environment, inspirational"
    },
    
    "finance": {
        "keywords": ["investment", "savings", "planning", "financial", "money", "budget", "growth", "security", "wealth", "banking"],
        "scenarios": ["financial planning", "investment strategy", "savings goal", "financial advisor", "money management", "economic growth"],
        "lighting": "professional financial lighting, trustworthy environment, stable atmosphere",
        "composition": "financial photography style, professional advisory setting, security-focused"
    }
}

# Popular microstock demographics and diversity requirements
INCLUSIVE_DEMOGRAPHICS = {
    "age_groups": ["young adult", "middle-aged", "senior", "millennial", "gen-z", "professional age"],
    "ethnicities": ["diverse", "multicultural", "Asian", "Hispanic", "African American", "Caucasian", "mixed ethnicity"],
    "genders": ["woman", "man", "non-binary", "diverse gender representation"],
    "body_types": ["diverse body types", "inclusive representation", "various sizes"],
    "abilities": ["diverse abilities", "inclusive accessibility", "various capabilities"]
}

# Trending visual styles for microstock
TRENDING_STYLES = {
    "photography": {
        "lighting": ["natural lighting", "studio lighting", "golden hour", "soft window light", "professional headshot lighting"],
        "composition": ["rule of thirds", "negative space", "clean background", "professional framing", "commercial composition"],
        "colors": ["neutral tones", "corporate colors", "minimal palette", "warm naturals", "professional blues"]
    },
    
    "illustration": {
        "styles": ["flat design", "minimalist", "modern vector", "isometric", "clean line art"],
        "colors": ["brand-safe colors", "corporate palette", "trending gradients", "minimal color scheme"],
        "composition": ["scalable design", "icon-friendly", "versatile layout", "clean margins"]
    }
}

# High-value microstock prompt enhancers
COMMERCIAL_ENHANCERS = {
    "quality_descriptors": [
        "high-resolution", "professional quality", "commercial grade", "studio quality",
        "sharp focus", "perfect lighting", "premium photography", "editorial quality"
    ],
    
    "commercial_appeal": [
        "marketable", "business-ready", "brand-safe", "corporate-friendly",
        "advertising-ready", "social media optimized", "web-ready", "print-ready"
    ],
    
    "technical_specs": [
        "sharp details", "perfect exposure", "professional color grading",
        "high dynamic range", "commercial lighting setup", "studio backdrop"
    ],
    
    "usage_optimization": [
        "negative space for text", "horizontal layout", "vertical layout",
        "square format", "banner friendly", "header image ready", "hero image style"
    ]
}

# Microstock-specific negative prompts (what to avoid)
MICROSTOCK_AVOID = [
    "trademarks", "logos", "brand names", "copyrighted material",
    "explicit content", "controversial topics", "political imagery",
    "religious symbols", "low quality", "blurry", "pixelated",
    "amateur lighting", "messy background", "cluttered composition",
    "outdated fashion", "old technology", "seasonal clothing",
    "specific locations", "recognizable landmarks", "faces without model releases"
]

def get_microstock_enhancements(category: str = "business") -> dict:
    """Get microstock-specific enhancements for a category"""
    return {
        "keywords": MICROSTOCK_CATEGORIES.get(category, {}).get("keywords", []),
        "scenarios": MICROSTOCK_CATEGORIES.get(category, {}).get("scenarios", []),
        "lighting": MICROSTOCK_CATEGORIES.get(category, {}).get("lighting", "professional lighting"),
        "composition": MICROSTOCK_CATEGORIES.get(category, {}).get("composition", "professional composition"),
        "quality": COMMERCIAL_ENHANCERS["quality_descriptors"],
        "appeal": COMMERCIAL_ENHANCERS["commercial_appeal"],
        "demographics": INCLUSIVE_DEMOGRAPHICS
    }

def build_microstock_prompt_enhancement(base_prompt: str, category: str = "business") -> str:
    """Add microstock-specific enhancements to a base prompt"""
    enhancements = get_microstock_enhancements(category)
    
    enhancement_text = (
        f" Professional {category} photography, "
        f"high commercial appeal, diverse and inclusive, "
        f"studio quality lighting, clean composition, "
        f"trending microstock style, business-ready, "
        f"perfect for marketing materials, "
        f"SEO-optimized visual content"
    )
    
    return base_prompt + enhancement_text

# Popular microstock search terms for different industries
INDUSTRY_KEYWORDS = {
    "corporate": ["leadership", "teamwork", "professional", "business meeting", "handshake", "success", "growth"],
    "healthcare": ["medical", "wellness", "care", "health", "doctor", "nurse", "treatment", "prevention"],
    "technology": ["innovation", "digital", "AI", "smart", "connected", "future", "automation", "data"],
    "education": ["learning", "knowledge", "study", "skill", "training", "development", "academic"],
    "lifestyle": ["wellness", "balance", "happiness", "family", "home", "comfort", "leisure", "joy"],
    "finance": ["investment", "savings", "planning", "wealth", "security", "banking", "financial"]
}