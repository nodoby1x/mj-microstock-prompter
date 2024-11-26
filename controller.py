import google.generativeai as genai
import os
from dotenv import load_dotenv

class PrompterGenerator:
    """
    Prompt generator part
    """
    def __init__(self, api_key=None, model_name="gemini-1.5-flash"):
        
        if api_key:
            self.api_key = api_key
        else:
            raise ValueError("Error: Please fill your Gemini API Key")

        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)
    
    def prompt_generator(self, main_base, image_style, theme=None, elements=None, emotional=None, color=None, image_detail=None, aspect=None):
    # Base instruction with concise phrasing
        # print(main_base, image_style, image_detail)
        create_prompt = (
            f"Create a Midjourney prompt for Generate Microstock-ready image in {image_style} style. Avoid trademarks, logos, text, or brand-specific elements. "
            f"Focus on {main_base}."
        )
        # Conditional additions to keep it compact
        if theme:
            create_prompt += f" Highlight the essence of {theme}."
        if elements:
            create_prompt += f" Include {elements}."
        if emotional:
            create_prompt += f" Evoke a sense of {emotional}."
        if color:
            create_prompt += f" Use a {color} palette."
        if image_detail:
            create_prompt += f" Add details like {image_detail}."
        if aspect:
            create_prompt += f" Render in {aspect} aspect ratio."

        # Example output to ensure clarity for API
        create_prompt += (
            "\n\nExample output:\n"
            "A bulldog wearing sunglasses, riding a bicycle with a basket full of flowers, "
            "pop art style, vibrant colors, bold outlines, comic book aesthetic, dynamic pose, cityscape background."
        )

        response = self.model.generate_content(create_prompt)
        
        return response

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    generator = PrompterGenerator(api_key=API_KEY, model_name="gemini-1.5-flash")
    midjourney_prompt = generator.prompt_generator(main_base="A dog cycling a bicycle",
                                                   image_style="Photography",
                                                   theme="Wonderful Day",
                                                   elements="Road, Tree",
                                                   emotional="Happy",
                                                   color="Cool Pastel",
                                                   image_detail="dog wearing a sunglasses",
                                                   aspect="16:9")
    print(midjourney_prompt.text)