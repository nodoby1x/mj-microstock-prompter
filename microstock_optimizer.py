"""
Microstock Optimization Helper - Suggests improvements for better sales potential
"""

import re
from typing import Dict, List, Tuple
from microstock_templates import MICROSTOCK_CATEGORIES, INDUSTRY_KEYWORDS, COMMERCIAL_ENHANCERS

class MicrostockOptimizer:
    """Analyzes and optimizes prompts for maximum microstock sales potential"""
    
    def __init__(self):
        self.trending_subjects = {
            "business": [
                "diverse business team meeting", "professional woman presenting", "handshake deal closing",
                "remote work setup", "startup office environment", "corporate diversity group",
                "business success celebration", "professional video call", "team collaboration",
                "female entrepreneur", "business growth chart", "corporate training session"
            ],
            "technology": [
                "person using AI interface", "smart home technology", "digital transformation",
                "cybersecurity professional", "data analysis dashboard", "cloud computing setup",
                "mobile app development", "tech startup workspace", "IoT device interaction",
                "digital marketing analytics", "virtual reality experience", "5G technology"
            ],
            "lifestyle": [
                "work-life balance", "healthy morning routine", "family quality time",
                "home office wellness", "sustainable living", "mindful meditation",
                "active lifestyle", "cooking healthy meals", "home organization",
                "weekend family activities", "personal growth journey", "wellness practices"
            ],
            "healthcare": [
                "telemedicine consultation", "diverse medical team", "preventive healthcare",
                "mental health support", "fitness and wellness", "medical technology",
                "patient care interaction", "health screening", "wellness checkup",
                "medical research", "healthcare innovation", "patient education"
            ],
            "imagen": [
                "photorealistic business portrait", "high-resolution lifestyle photography", 
                "detailed commercial illustration", "Adobe Stock premium content",
                "professional studio photography", "contemporary business scene",
                "diverse professional portrait", "commercial-grade photography",
                "premium quality lifestyle image", "detailed architectural photography"
            ]
        }
        
        self.high_value_demographics = [
            "diverse professional team", "millennial entrepreneurs", "working parents",
            "remote workers", "small business owners", "healthcare professionals",
            "tech professionals", "creative professionals", "multicultural team",
            "female leaders", "young professionals", "experienced professionals"
        ]
        
        self.sales_boosting_keywords = [
            "professional", "success", "growth", "innovation", "teamwork", "leadership",
            "diversity", "modern", "technology", "health", "wellness", "business",
            "digital", "future", "smart", "sustainable", "efficient", "collaborative",
            "photorealistic", "high-resolution", "detailed", "commercial", "premium"
        ]
    
    def analyze_prompt_potential(self, main_base: str, theme: str = "", elements: str = "") -> Dict:
        """Analyze a prompt's commercial potential and suggest improvements"""
        combined_text = f"{main_base} {theme} {elements}".lower()
        
        # Calculate marketability score
        marketability_score = self._calculate_marketability(combined_text)
        
        # Detect category
        category = self._detect_best_category(combined_text)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(main_base, category, marketability_score)
        
        # Identify missing elements
        missing_elements = self._identify_missing_elements(combined_text)
        
        return {
            "marketability_score": marketability_score,
            "category": category,
            "suggestions": suggestions,
            "missing_elements": missing_elements,
            "trending_alternatives": self._get_trending_alternatives(main_base, category),
            "optimization_tips": self._get_optimization_tips(marketability_score)
        }
    
    def _calculate_marketability(self, text: str) -> int:
        """Calculate marketability score (0-100)"""
        score = 0
        
        # Check for sales-boosting keywords
        keyword_matches = sum(1 for keyword in self.sales_boosting_keywords if keyword in text)
        score += min(keyword_matches * 10, 40)
        
        # Check for demographic diversity indicators
        diversity_indicators = ["diverse", "multicultural", "inclusive", "team", "group"]
        if any(indicator in text for indicator in diversity_indicators):
            score += 20
        
        # Check for professional/business context
        business_indicators = ["professional", "business", "corporate", "office", "work"]
        if any(indicator in text for indicator in business_indicators):
            score += 15
        
        # Check for trending topics
        trending_topics = ["remote", "digital", "sustainable", "wellness", "innovation"]
        if any(topic in text for topic in trending_topics):
            score += 15
        
        # Penalty for potentially problematic content
        problematic = ["seasonal", "specific location", "brand", "logo", "trademark"]
        if any(problem in text for problem in problematic):
            score -= 20
        
        return max(0, min(100, score))
    
    def _detect_best_category(self, text: str) -> str:
        """Detect the best microstock category for the content"""
        category_scores = {}
        
        for category, keywords in INDUSTRY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        return max(category_scores, key=category_scores.get) if any(category_scores.values()) else 'business'
    
    def _generate_suggestions(self, main_base: str, category: str, score: int) -> List[str]:
        """Generate specific suggestions for improvement"""
        suggestions = []
        
        if score < 30:
            suggestions.append("Consider adding 'professional' or 'business' context")
            suggestions.append("Include diverse demographics for broader appeal")
        
        if score < 50:
            suggestions.append(f"Add trending {category} keywords for better discoverability")
            suggestions.append("Specify modern, contemporary styling")
        
        if score < 70:
            suggestions.append("Include emotional appeal (success, growth, innovation)")
            suggestions.append("Add professional lighting and composition details")
        
        # Category-specific suggestions
        if category == 'business':
            suggestions.append("Consider: team collaboration, leadership, or success themes")
        elif category == 'technology':
            suggestions.append("Consider: AI, digital transformation, or innovation themes")
        elif category == 'lifestyle':
            suggestions.append("Consider: work-life balance, wellness, or family themes")
        
        return suggestions
    
    def _identify_missing_elements(self, text: str) -> List[str]:
        """Identify missing elements that could boost sales"""
        missing = []
        
        diversity_terms = ["diverse", "multicultural", "inclusive"]
        if not any(term in text for term in diversity_terms):
            missing.append("Diversity/inclusion elements")
        
        quality_terms = ["professional", "high-quality", "studio"]
        if not any(term in text for term in quality_terms):
            missing.append("Quality/professional indicators")
        
        modern_terms = ["modern", "contemporary", "current", "trending"]
        if not any(term in text for term in modern_terms):
            missing.append("Modern/contemporary styling")
        
        commercial_terms = ["business", "corporate", "commercial", "marketing"]
        if not any(term in text for term in commercial_terms):
            missing.append("Commercial context")
        
        return missing
    
    def _get_trending_alternatives(self, main_base: str, category: str) -> List[str]:
        """Get trending alternatives for the main subject"""
        alternatives = []
        
        if category in self.trending_subjects:
            # Find similar trending subjects
            base_words = main_base.lower().split()
            for subject in self.trending_subjects[category]:
                if any(word in subject.lower() for word in base_words):
                    alternatives.append(subject)
        
        # Add general trending alternatives
        if not alternatives:
            alternatives = self.trending_subjects.get(category, [])[:3]
        
        return alternatives[:5]
    
    def _get_optimization_tips(self, score: int) -> List[str]:
        """Get optimization tips based on score"""
        tips = []
        
        if score < 40:
            tips.extend([
                "Focus on high-demand business and professional themes",
                "Include diverse demographics for broader market appeal",
                "Add trending keywords that buyers actively search for"
            ])
        
        if score < 60:
            tips.extend([
                "Emphasize commercial usability and professional quality",
                "Include modern, contemporary styling elements",
                "Add emotional appeal (success, growth, innovation)"
            ])
        
        if score < 80:
            tips.extend([
                "Specify professional lighting and composition",
                "Include negative space for text overlay",
                "Focus on evergreen content that sells year-round"
            ])
        
        tips.append("Ensure content is brand-safe and free of trademarks")
        tips.append("Target specific buyer personas and use cases")
        
        return tips
    
    def get_bestselling_prompts(self, category: str = "business") -> List[str]:
        """Get example bestselling prompt structures"""
        templates = {
            "business": [
                "Diverse professional team collaborating in modern office, natural lighting, business success",
                "Professional woman presenting to multicultural team, corporate environment, leadership",
                "Handshake deal closing between diverse business partners, success celebration",
                "Remote work setup with professional lighting, work-life balance, modern technology"
            ],
            "technology": [
                "Person interacting with AI interface, futuristic lighting, digital innovation",
                "Diverse tech team working on innovative project, modern startup office",
                "Smart home technology setup, contemporary lifestyle, connected living",
                "Digital transformation concept, professional business technology"
            ],
            "lifestyle": [
                "Work-life balance scene, professional working from home, wellness focus",
                "Diverse family enjoying quality time together, modern home environment",
                "Healthy morning routine, professional lifestyle, wellness and productivity",
                "Sustainable living concept, modern eco-friendly home, green lifestyle"
            ],
            "imagen": [
                "A photorealistic, high-resolution lifestyle photograph of diverse young professionals in modern office. Composition is minimalist with copy space, focus on collaboration. Lighting is soft natural morning light. Mood is optimistic and inspiring. Color palette consists of neutral tones with corporate blue accents.",
                "A high-resolution business photograph of professional woman presenting to multicultural team in contemporary workspace. Composition follows rule of thirds, focus on leadership moment. Lighting is bright studio lighting. Mood is confident and successful. Color palette is corporate blues and modern whites.",
                "A photorealistic still life photograph of healthy meal preparation on marble countertop. Composition is bird's-eye flat lay, focus on fresh ingredients arrangement. Lighting is soft even daylight. Mood is fresh and clean. Color palette consists of natural greens, reds, and whites."
            ]
        }
        
        return templates.get(category, templates["business"])

# Create global optimizer instance
optimizer = MicrostockOptimizer()