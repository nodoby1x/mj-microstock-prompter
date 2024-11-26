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

    def prepare_input(self, prompt):
        return input(prompt).strip()
    
    def prompt_generator(self, main_base, image_style, theme=None, elements=None, emotional=None, color=None, image_detail=None, aspect=None):
        create_prompt = f'The generated image from the prompt is use for selling in Microstock, It must not include specific tradmark, logo, quotation marks, and tradmark logo, tradmark word, output commentary.'
        create_prompt += f'The main idea is {main_base} in {image_style} style.'
        if theme:
            create_prompt += f" Make sure to capture essence of {theme}."
        if elements:
            create_prompt += f" Incorporate elements of {elements}."
        if emotional:
            create_prompt += f" The scene should evoke {emotional}."
        if color:
            create_prompt += f" The color pallate should focus on {color}."
        if image_detail:
            create_prompt += f" Include details like {image_detail} to enchance the overall impact."
        if aspect:
            create_prompt += f"For generated an image in aspect {aspect}."
        
        create_prompt += f"""\n \n Response me only prompt here is an example output:
        A bulldog wearing sunglasses, riding a bicycle with a basket full of flowers, pop art style, vibrant colors, bold outlines, comic book aesthetic, dynamic pose, cityscape background

        """
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