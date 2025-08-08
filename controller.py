import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any
from enum import Enum
from microstock_templates import get_microstock_enhancements, build_microstock_prompt_enhancement, INDUSTRY_KEYWORDS
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"

class PrompterGenerator:
    """
    Enhanced prompt generator supporting multiple AI providers
    """
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-pro", provider: str = "gemini"):
        if not api_key:
            raise ValueError("Error: Please provide an API key")
        
        self.api_key = api_key
        self.model_name = model_name
        self.provider = AIProvider(provider.lower())
        
        try:
            if self.provider == AIProvider.GEMINI:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(model_name=self.model_name)
            elif self.provider == AIProvider.OPENAI:
                openai.api_key = self.api_key
                self.client = openai.OpenAI(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider.value} client: {e}")
            raise
    
    def prompt_generator(self, main_base: str, image_style: str = "Photography", 
                        theme: Optional[str] = None, elements: Optional[str] = None, 
                        emotional: Optional[str] = None, color: Optional[str] = None, 
                        image_detail: Optional[str] = None, aspect: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate optimized Midjourney prompts for microstock images
        """
        if not main_base.strip():
            raise ValueError("Main base cannot be empty")
        
        try:
            create_prompt = self._build_prompt(main_base, image_style, theme, elements, 
                                             emotional, color, image_detail, aspect)
            
            if self.provider == AIProvider.GEMINI:
                response = self.model.generate_content(create_prompt)
                return {"text": response.text, "provider": "gemini"}
            elif self.provider == AIProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at creating Midjourney prompts for microstock photography."},
                        {"role": "user", "content": create_prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                return {"text": response.choices[0].message.content, "provider": "openai"}
        except (openai.APIError, openai.RateLimitError, openai.AuthenticationError) as e:
            logger.error(f"OpenAI API error: {e}")
            raise ValueError(f"OpenAI API error: {e}") from e
        except Exception as e:
            logger.error(f"Error generating prompt with {self.provider.value}: {e}")
            raise ValueError(f"An unexpected error occurred: {e}") from e
    
    def _build_prompt(self, main_base: str, image_style: str, theme: Optional[str], 
                     elements: Optional[str], emotional: Optional[str], color: Optional[str], 
                     image_detail: Optional[str], aspect: Optional[str]) -> str:
        """
        Build highly optimized microstock prompt with maximum commercial appeal
        """
        # Detect category for targeted optimization
        category = self._detect_category(main_base, theme, elements)
        microstock_data = get_microstock_enhancements(category)
        
        # Build core commercial prompt
        create_prompt = (
            f"Create a BESTSELLING microstock {image_style} prompt that will generate HIGH SALES. "
            f"This image must be PERFECT for commercial buyers in {category} industry.\n\n"
            f"CORE SUBJECT: {main_base}\n"
            f"TARGET MARKET: {category.title()} professionals, marketers, content creators\n"
            f"COMMERCIAL CATEGORY: {category}\n\n"
            f"MANDATORY MICROSTOCK SUCCESS FACTORS:\n"
            f"• TRENDING KEYWORDS: Include {', '.join(microstock_data['keywords'][:5])}\n"
            f"• BUYER APPEAL: High commercial value, widely usable, premium quality\n"
            f"• DIVERSITY: Include diverse, inclusive representation (age, ethnicity, gender)\n"
            f"• PROFESSIONAL QUALITY: Studio lighting, perfect composition, sharp focus\n"
            f"• CLEAN DESIGN: No text, logos, brands, or copyrighted material\n"
            f"• MODERN STYLE: Contemporary, trending, not outdated\n"
            f"• VERSATILE USE: Perfect for websites, ads, presentations, social media\n\n"
        )
        
        # Add category-specific optimization
        create_prompt += f"INDUSTRY-SPECIFIC REQUIREMENTS for {category.upper()}:\n"
        create_prompt += f"• SCENARIOS: {', '.join(microstock_data['scenarios'][:3])}\n"
        create_prompt += f"• LIGHTING: {microstock_data['lighting']}\n"
        create_prompt += f"• COMPOSITION: {microstock_data['composition']}\n\n"
        
        # Add user-specific details with commercial optimization
        if theme:
            create_prompt += f"THEME ENHANCEMENT: {theme} (make it commercially trending and buyer-focused)\n"
        if elements:
            create_prompt += f"KEY ELEMENTS: {elements} (ensure they're modern, professional, and market-ready)\n"
        if emotional:
            create_prompt += f"EMOTIONAL APPEAL: {emotional} (positive, aspirational, business-appropriate)\n"
        if color:
            create_prompt += f"COLOR STRATEGY: {color} (trending, professional, brand-safe palette)\n"
        if image_detail:
            create_prompt += f"PREMIUM DETAILS: {image_detail} (high-end, commercial-grade specifics)\n"
        if aspect:
            create_prompt += f"FORMAT OPTIMIZATION: {aspect} ratio (perfect for digital and print marketing)\n\n"
        
        # Final commercial optimization instructions
        create_prompt += (
            f"SALES OPTIMIZATION CHECKLIST:\n"
            f"• Use TOP SELLING keywords: {', '.join(random.sample(INDUSTRY_KEYWORDS.get(category, []), min(3, len(INDUSTRY_KEYWORDS.get(category, [])))))}\n"
            f"• Target HIGH-DEMAND buyer searches\n"
            f"• Ensure MAXIMUM commercial usability\n"
            f"• Create PREMIUM quality worthy of top-tier licensing\n"
            f"• Include negative space for text overlay where appropriate\n"
            f"• Focus on EVERGREEN content that sells year-round\n"
            f"• Make it ADVERTISING-READY and BRAND-SAFE\n\n"
            f"OUTPUT: Generate a concise, powerful Midjourney prompt that creates a "
            f"BESTSELLING microstock image with maximum commercial appeal and buyer demand."
        )
        
        return create_prompt
    
    def flux_prompt_generator(self, main_base: str, image_style: str = "Photography", 
                            theme: Optional[str] = None, elements: Optional[str] = None, 
                            emotional: Optional[str] = None, color: Optional[str] = None, 
                            image_detail: Optional[str] = None, lighting: Optional[str] = None,
                            composition: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate optimized FLUX1.dev prompts for microstock images (NO Midjourney parameters)
        """
        if not main_base.strip():
            raise ValueError("Main base cannot be empty")
        
        try:
            create_prompt = self._build_flux_prompt(main_base, image_style, theme, elements, 
                                                  emotional, color, image_detail, lighting, composition)
            
            if self.provider == AIProvider.GEMINI:
                response = self.model.generate_content(create_prompt)
                return {"text": response.text, "provider": "gemini"}
            elif self.provider == AIProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at creating FLUX1.dev Stable Diffusion prompts for microstock photography. NEVER include Midjourney parameters like --ar, --v, --zoom, --style, --chaos, etc."},
                        {"role": "user", "content": create_prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                return {"text": response.choices[0].message.content, "provider": "openai"}
        except (openai.APIError, openai.RateLimitError, openai.AuthenticationError) as e:
            logger.error(f"OpenAI API error: {e}")
            raise ValueError(f"OpenAI API error: {e}") from e
        except Exception as e:
            logger.error(f"Error generating FLUX prompt with {self.provider.value}: {e}")
            raise ValueError(f"An unexpected error occurred: {e}") from e
    
    def _build_flux_prompt(self, main_base: str, image_style: str, theme: Optional[str], 
                          elements: Optional[str], emotional: Optional[str], color: Optional[str], 
                          image_detail: Optional[str], lighting: Optional[str], composition: Optional[str]) -> str:
        """
        Build FLUX1.dev-specific prompt without Midjourney parameters
        """
        # Detect category for targeted optimization
        category = self._detect_category(main_base, theme, elements)
        microstock_data = get_microstock_enhancements(category)
        
        # Build FLUX-specific commercial prompt
        create_prompt = (
            f"Create a BESTSELLING microstock {image_style} prompt for FLUX1.dev Stable Diffusion that will generate HIGH SALES. "
            f"This image must be PERFECT for commercial buyers in {category} industry.\n\n"
            f"IMPORTANT: Generate ONLY a descriptive prompt text. DO NOT include any Midjourney parameters like --ar, --v, --zoom, --style, --chaos, --seed, etc.\n\n"
            f"CORE SUBJECT: {main_base}\n"
            f"TARGET MARKET: {category.title()} professionals, marketers, content creators\n"
            f"COMMERCIAL CATEGORY: {category}\n\n"
            f"MANDATORY FLUX1.dev MICROSTOCK SUCCESS FACTORS:\n"
            f"• TRENDING KEYWORDS: Include {', '.join(microstock_data['keywords'][:5])}\n"
            f"• BUYER APPEAL: High commercial value, widely usable, premium quality\n"
            f"• DIVERSITY: Include diverse, inclusive representation (age, ethnicity, gender)\n"
f"• PROFESSIONAL QUALITY: Studio lighting, perfect composition, sharp focus\n"
            f"• FLUX QUALITY TERMS: photorealistic, detailed, sharp focus, high resolution\n"
            f"• CLEAN DESIGN: No text, logos, brands, or copyrighted material\n"
            f"• MODERN STYLE: Contemporary, trending, not outdated\n"
            f"• VERSATILE USE: Perfect for websites, ads, presentations, social media\n\n"
        )
        
        # Add category-specific optimization
        create_prompt += f"INDUSTRY-SPECIFIC REQUIREMENTS for {category.upper()}:\n"
        create_prompt += f"• SCENARIOS: {', '.join(microstock_data['scenarios'][:3])}\n"
        if lighting:
            create_prompt += f"• LIGHTING: {lighting}\n"
        else:
            create_prompt += f"• LIGHTING: {microstock_data['lighting']}\n"
        if composition:
            create_prompt += f"• COMPOSITION: {composition}\n"
        else:
            create_prompt += f"• COMPOSITION: {microstock_data['composition']}\n\n"
        
        # Add user-specific details
        if theme:
            create_prompt += f"THEME ENHANCEMENT: {theme} (make it commercially trending and buyer-focused)\n"
        if elements:
            create_prompt += f"KEY ELEMENTS: {elements} (ensure they're modern, professional, and market-ready)\n"
        if emotional:
            create_prompt += f"EMOTIONAL APPEAL: {emotional} (positive, aspirational, business-appropriate)\n"
        if color:
            create_prompt += f"COLOR STRATEGY: {color} (trending, professional, brand-safe palette)\n"
        if image_detail:
            create_prompt += f"PREMIUM DETAILS: {image_detail} (high-end, commercial-grade specifics)\n\n"
        
        # Final FLUX optimization instructions
        create_prompt += (
            f"FLUX1.dev OPTIMIZATION CHECKLIST:\n"
            f"• Use TOP SELLING keywords: {', '.join(random.sample(INDUSTRY_KEYWORDS.get(category, []), min(3, len(INDUSTRY_KEYWORDS.get(category, [])))))}\n"
            f"• Target HIGH-DEMAND buyer searches\n"
            f"• Ensure MAXIMUM commercial usability\n"
            f"• Create PREMIUM quality worthy of top-tier licensing\n"
            f"• Include FLUX quality terms: photorealistic, detailed, sharp focus, high resolution\n"
            f"• Focus on EVERGREEN content that sells year-round\n"
            f"• Make it ADVERTISING-READY and BRAND-SAFE\n\n"
            f"OUTPUT: Generate a concise, descriptive FLUX1.dev prompt (NO Midjourney parameters like --ar, --v, --zoom) that creates a "
            f"BESTSELLING microstock image with maximum commercial appeal and buyer demand. "
            f"The prompt should be clean descriptive text only, suitable for Stable Diffusion FLUX1.dev model."
        )
        
        return create_prompt
    
    def imagen_prompt_generator(self, main_base: str, image_style: str = "Photography", 
                               theme: Optional[str] = None, elements: Optional[str] = None, 
                               emotional: Optional[str] = None, color: Optional[str] = None, 
                               image_detail: Optional[str] = None, lighting: Optional[str] = None,
                               composition: Optional[str] = None, setting: Optional[str] = None,
                               mood: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate optimized Google Imagen 4 prompts for microstock images
        """
        if not main_base.strip():
            raise ValueError("Main base cannot be empty")
        
        try:
            # Directly build the prompt without an extra AI call
            create_prompt = self._build_imagen_prompt(
                main_base, image_style, theme, elements, emotional, color, 
                image_detail, lighting, composition, setting, mood
            )
            
            return {"text": create_prompt, "provider": "system"}
            
        except Exception as e:
            logger.error(f"Error generating Imagen prompt: {e}")
            raise ValueError(f"An unexpected error occurred while generating the Imagen prompt: {e}") from e
    
    def _build_imagen_prompt(self, main_base: str, image_style: str, theme: Optional[str], 
                            elements: Optional[str], emotional: Optional[str], color: Optional[str], 
                            image_detail: Optional[str], lighting: Optional[str], composition: Optional[str],
                            setting: Optional[str], mood: Optional[str]) -> str:
        """
        Build Google Imagen 4-specific prompt based on a precise template.
        """
        # Detect category for targeted optimization
        category = self._detect_category(main_base, theme, elements)
        microstock_data = get_microstock_enhancements(category)
        
        # Define template components, using defaults from microstock_data if not provided
        primary_subject = main_base
        environment = setting or (microstock_data['scenarios'][0] if microstock_data['scenarios'] else 'professional business environment')
        compositional_style = composition or microstock_data['composition']
        key_detail = theme or ""
        lighting_desc = lighting or microstock_data['lighting']
        mood_atmosphere = mood or emotional or "optimistic and professional"
        color_palette = color or "neutral tones with corporate accent colors"
        
        # Construct the prompt using a precise f-string template
        prompt = (
            f"A photorealistic, high-resolution {image_style.lower()} of {primary_subject} "
            f"in a {environment}. The composition should be {compositional_style}, with a focus on {key_detail}. "
            f"The lighting is {lighting_desc}. The overall mood is {mood_atmosphere}. "
            f"The color palette consists of {color_palette}."
        )
        
        # Add extra details if provided
        if elements:
            prompt += f" Additional elements include: {elements}."
        if image_detail:
            prompt += f" Premium details to include: {image_detail}."
            
        # Add commercial keywords for better searchability
        commercial_keywords = ", ".join(random.sample(INDUSTRY_KEYWORDS.get(category, []), min(3, len(INDUSTRY_KEYWORDS.get(category, [])))))
        prompt += f" Keywords for commercial success: {commercial_keywords}, high-resolution, detailed, professional."
        
        return prompt
    
    def _detect_category(self, main_base: str, theme: Optional[str], elements: Optional[str]) -> str:
        """
        Detect the most relevant microstock category based on input
        """
        text_to_analyze = f"{main_base} {theme or ''} {elements or ''}".lower()
        
        category_scores = {}
        for category, keywords in INDUSTRY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text_to_analyze)
            category_scores[category] = score
        
        # Return category with highest score, default to 'business'
        return max(category_scores, key=category_scores.get) if any(category_scores.values()) else 'business'

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if API_KEY:
        try:
            generator = PrompterGenerator(api_key=API_KEY, model_name="gemini-1.5-pro", provider="gemini")
            result = generator.prompt_generator(
                main_base="A dog cycling a bicycle",
                image_style="Photography",
                theme="Wonderful Day",
                elements="Road, Tree",
                emotional="Happy",
                color="Cool Pastel",
                image_detail="dog wearing sunglasses",
                aspect="16:9"
            )
            print(f"Generated prompt ({result['provider']}): {result['text']}")
        except Exception as e:
            logger.error(f"Error: {e}")
    else:
        logger.error("No API key found in environment variables")