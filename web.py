import streamlit as sl
from controller import PrompterGenerator
from dotenv import load_dotenv
import os
import time

load_dotenv()

sl.set_page_config(page_title="MJ Prompter")

def main():

    with open("style.css", "r") as file:
        content = file.read()
    custom_css = f"<style>{content}</style>"
    sl.markdown(custom_css, unsafe_allow_html=True)

    sl.title("MJ Prompter For Microstock")
    sl.sidebar.header("Settings")

    api_key_env = os.getenv("GEMINI_API_KEY")
    api_key = sl.sidebar.text_input("Gemini API Key", value=api_key_env if api_key_env else "", type="password")
    
    num_prompts = sl.sidebar.slider("Prompts per Round", min_value=1, max_value=10, value=1)
    round_count = sl.sidebar.slider("Number of Rounds", min_value=1, max_value=20, value=1)
    rest_time = sl.sidebar.slider("Round Interval", min_value=5, max_value=30, value=15)

    row1_col1, row1_col2 = sl.columns(2)
    main_base = row1_col1.text_input("Main Base", "")
    image_style = row1_col2.text_input("Image Style", "Photography")

    image_details = sl.text_input("Image Details", "")
    config_mj = sl.text_input("Config", "--ar 16:9 --q 2 --chaos 50 --p 2qnqoze")

    row3_col1, row3_col2 = sl.columns(2)
    elements = row3_col1.text_input("Elements", "")
    aspect = row3_col2.text_input("Aspect", "16:9")

    row4_col1, row4_col2, row4_col3 = sl.columns(3)
    theme = row4_col1.text_input("Theme", "")
    emotional = row4_col2.text_input("Emotional", "")
    color_palette = row4_col3.text_input("Color Palette", "")

    if "prompts" not in sl.session_state:
        sl.session_state.prompts = []
    
    if sl.sidebar.button("Generate Prompts", key='generate-button'):
    # Validate API key
        if api_key.strip() == "":
            sl.error("Please enter your Gemini API Key.")
        elif main_base == "":
            sl.error("Please fill the main base idea to create prompt.")
        else:
            try:
                # Clear previous prompts
                sl.session_state.prompts.clear()

                # Generate prompts for multiple rounds
                for round_num in range(1, round_count + 1):
                    sl.info(f"Starting Round {round_num}...")
                    
                    # Create a new instance of the PrompterGenerator for each round
                    generator = PrompterGenerator(api_key=api_key, model_name="gemini-1.5-flash")

                    # Temporary list for the current round
                    round_prompts = []

                    # Generate the specified number of prompts
                    for i in range(1, num_prompts + 1):
                        try:
                            prompt = generator.prompt_generator(
                                main_base=main_base,
                                image_style=image_style,
                                image_detail=image_details,
                                theme=theme,
                                elements=elements,
                                emotional=emotional,
                                color=color_palette,
                                aspect=aspect,
                            )
                            this_prompt = prompt.text.replace(".", "").strip()
                            complete_prompt = this_prompt + " " + config_mj.strip()
                            round_prompts.append(complete_prompt)
                            time.sleep(3) #delay 3 second each prompt request
                        except Exception as e:
                            sl.error(f"Error generating prompt {i} in Round {round_num}: {str(e)}")
                    
                    # Add current round's prompts to session state
                    sl.session_state.prompts.extend(round_prompts)

                    # Pause before the next round
                    if round_num < round_count:
                        sl.info(f"Resting for {rest_time} seconds before the next round...")
                        time.sleep(rest_time) #delaying each round
            except Exception as e:
                sl.error(f"Error initializing MidjourneyPromptGenerator: {str(e)}")


    if sl.sidebar.button("Export TXT", key='txt-button'):
        if sl.session_state.prompts:
            file_name = f"{'prompts'}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(sl.session_state.prompts))
            sl.sidebar.success(f"Prompts exported to {file_name}")
        else:
            sl.sidebar.error("No prompts to export.")

    # Display the prompts stored in session state
    if sl.session_state.prompts:
        sl.success("Generated Midjourney Prompts: Completed")
        # sl.markdown(f'<div class="prompt-output"><div class="prompt-text">{sl.session_state.prompts}</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
