import streamlit as st
from controller import PrompterGenerator
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MJ Prompter For Microstock",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Load custom CSS
    try:
        with open("style.css", "r") as file:
            content = file.read()
        custom_css = f"<style>{content}</style>"
        st.markdown(custom_css, unsafe_allow_html=True)
    except FileNotFoundError:
        logger.warning("style.css not found, using default styling")

    st.title("🎨 MJ Prompter For Microstock")
    st.markdown("Generate professional Midjourney prompts optimized for microstock photography")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Settings")
    
    # AI Provider selection
    provider = st.sidebar.selectbox(
        "AI Provider", 
        ["gemini", "openai"], 
        help="Choose between Gemini and OpenAI for prompt generation"
    )
    
    # API key configuration
    if provider == "gemini":
        api_key_env = os.getenv("GEMINI_API_KEY")
        model_options = ["gemini-1.5-flash", "gemini-1.5-pro"]
    else:
        api_key_env = os.getenv("OPENAI_API_KEY")
        model_options = ["gpt-3.5-turbo", "gpt-4"]
    
    api_key = st.sidebar.text_input(
        f"{provider.upper()} API Key", 
        value=api_key_env if api_key_env else "", 
        type="password",
        help=f"Enter your {provider.upper()} API key"
    )
    
    model = st.sidebar.selectbox("Model", model_options, help="Select the AI model to use")
    
    # Generation settings
    st.sidebar.subheader("📊 Generation Settings")
    num_prompts = st.sidebar.slider("Prompts per Round", min_value=1, max_value=10, value=1)
    round_count = st.sidebar.slider("Number of Rounds", min_value=1, max_value=20, value=1)
    rest_time = st.sidebar.slider("Round Interval (seconds)", min_value=5, max_value=60, value=15)
    
    # Show total prompts calculation
    total_prompts = num_prompts * round_count
    st.sidebar.info(f"Total prompts to generate: {total_prompts}")
    estimated_time = (total_prompts * 3) + ((round_count - 1) * rest_time)
    st.sidebar.info(f"Estimated time: ~{estimated_time} seconds")

    # Main content area
    st.subheader("📝 Prompt Configuration")
    
    # Row 1: Main inputs
    col1, col2 = st.columns(2)
    with col1:
        main_base = st.text_input(
            "Main Subject *", 
            "", 
            help="The primary subject or concept for your image (required)",
            placeholder="e.g., A professional businesswoman"
        )
    with col2:
        image_style = st.text_input(
            "Image Style", 
            "Photography", 
            help="Photography, Digital Art, Illustration, etc.",
            placeholder="Photography"
        )

    # Row 2: Details and configuration
    image_details = st.text_input(
        "Image Details", 
        "", 
        help="Specific details about the image",
        placeholder="e.g., holding a laptop, smiling confidently"
    )
    
    # Row 3: Additional elements
    col1, col2 = st.columns(2)
    with col1:
        elements = st.text_input(
            "Elements", 
            "", 
            help="Specific objects or elements to include",
            placeholder="e.g., office background, natural lighting"
        )
    with col2:
        aspect = st.selectbox(
            "Aspect Ratio", 
            ["16:9", "1:1", "4:3", "9:16", "3:2"],
            help="Image aspect ratio for different platforms"
        )

    # Row 4: Mood and style
    col1, col2, col3 = st.columns(3)
    with col1:
        theme = st.text_input(
            "Theme", 
            "", 
            help="Overall theme or concept",
            placeholder="e.g., Professional success"
        )
    with col2:
        emotional = st.text_input(
            "Emotional Tone", 
            "", 
            help="Happy, confident, serene, etc.",
            placeholder="e.g., Confident, approachable"
        )
    with col3:
        color_palette = st.text_input(
            "Color Palette", 
            "", 
            help="Warm, cool, monochrome, vibrant, etc.",
            placeholder="e.g., Professional blue tones"
        )

    # Midjourney configuration
    st.subheader("🎯 Midjourney Configuration")
    config_mj = st.text_input(
        "MJ Parameters", 
        f"--ar {aspect} --q 2 --chaos 50",
        help="Midjourney-specific parameters that will be appended to each prompt"
    )

    # Initialize session state
    if "prompts" not in st.session_state:
        st.session_state.prompts = []
    if "generation_stats" not in st.session_state:
        st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}

    # Action buttons
    st.subheader("🚀 Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        generate_button = st.button(
            "🎨 Generate Prompts", 
            key='generate-button',
            type="primary",
            use_container_width=True
        )
    
    with col2:
        clear_button = st.button(
            "🗑️ Clear All", 
            key='clear-button',
            use_container_width=True
        )
    
    with col3:
        export_button = st.button(
            "📄 Export TXT", 
            key="export-txt",
            use_container_width=True
        )
    
    # Handle button actions
    if clear_button:
        st.session_state.prompts.clear()
        st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}
        st.success("All prompts cleared!")
        st.rerun()
    
    if export_button:
        export_prompts()
    
    if generate_button:
        generate_prompts(api_key, provider, model, main_base, image_style, image_details,
                        theme, elements, emotional, color_palette, aspect, config_mj,
                        num_prompts, round_count, rest_time)
    
    # Display generation statistics
    if st.session_state.generation_stats["total"] > 0:
        display_stats()
    
    # Display generated prompts
    display_prompts()

def generate_prompts(api_key, provider, model, main_base, image_style, image_details,
                    theme, elements, emotional, color_palette, aspect, config_mj,
                    num_prompts, round_count, rest_time):
    
    # Validation
    if not api_key.strip():
        st.error(f"❌ Please enter your {provider.upper()} API Key.")
        return
    
    if not main_base.strip():
        st.error("❌ Please fill the main subject to create prompt.")
        return
    
    try:
        # Clear previous data
        st.session_state.prompts.clear()
        st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}
        
        # Progress tracking
        total_prompts = num_prompts * round_count
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        current_prompt = 0
        
        # Generate prompts for multiple rounds
        for round_num in range(1, round_count + 1):
            status_text.info(f"🔄 Starting Round {round_num}/{round_count}...")
            
            try:
                # Create generator instance
                generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
                
                # Generate prompts for this round
                for i in range(1, num_prompts + 1):
                    try:
                        status_text.info(f"⚡ Generating prompt {i}/{num_prompts} in Round {round_num}...")
                        
                        result = generator.prompt_generator(
                            main_base=main_base,
                            image_style=image_style,
                            image_detail=image_details,
                            theme=theme,
                            elements=elements,
                            emotional=emotional,
                            color=color_palette,
                            aspect=aspect,
                        )
                        
                        # Clean and format the prompt
                        this_prompt = result["text"].replace(".", "").strip()
                        complete_prompt = f"{this_prompt} {config_mj.strip()}"
                        
                        st.session_state.prompts.append({
                            "prompt": complete_prompt,
                            "round": round_num,
                            "index": i,
                            "provider": result["provider"],
                            "timestamp": time.time()
                        })
                        
                        st.session_state.generation_stats["successful"] += 1
                        time.sleep(3)  # Rate limiting
                        
                    except Exception as e:
                        logger.error(f"Error generating prompt {i} in Round {round_num}: {e}")
                        st.error(f"❌ Error generating prompt {i} in Round {round_num}: {str(e)}")
                        st.session_state.generation_stats["failed"] += 1
                    
                    current_prompt += 1
                    progress_bar.progress(current_prompt / total_prompts)
                
                # Pause before next round
                if round_num < round_count:
                    status_text.info(f"⏳ Resting for {rest_time} seconds before next round...")
                    time.sleep(rest_time)
                    
            except Exception as e:
                logger.error(f"Error in round {round_num}: {e}")
                st.error(f"❌ Error in Round {round_num}: {str(e)}")
        
        st.session_state.generation_stats["total"] = total_prompts
        status_text.success("✅ Generation complete!")
        
    except Exception as e:
        logger.error(f"Error initializing generator: {e}")
        st.error(f"❌ Error initializing generator: {str(e)}")

def display_stats():
    """Display generation statistics"""
    stats = st.session_state.generation_stats
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Prompts", stats["total"])
    with col2:
        st.metric("Successful", stats["successful"], delta=None)
    with col3:
        st.metric("Failed", stats["failed"], delta=None)

def display_prompts():
    """Display generated prompts in an organized way"""
    if st.session_state.prompts:
        st.subheader("📋 Generated Prompts")
        st.success(f"✅ Generated {len(st.session_state.prompts)} prompts successfully!")
        
        # Group prompts by round
        rounds = {}
        for prompt_data in st.session_state.prompts:
            round_num = prompt_data["round"]
            if round_num not in rounds:
                rounds[round_num] = []
            rounds[round_num].append(prompt_data)
        
        # Display prompts by round
        for round_num in sorted(rounds.keys()):
            with st.expander(f"Round {round_num} ({len(rounds[round_num])} prompts)", expanded=True):
                for i, prompt_data in enumerate(rounds[round_num]):
                    st.markdown(f"**Prompt {prompt_data['index']}** *({prompt_data['provider']})*")
                    st.text_area(
                        f"prompt_{round_num}_{i}",
                        prompt_data["prompt"],
                        height=100,
                        key=f"display_prompt_{round_num}_{i}",
                        label_visibility="collapsed"
                    )
                    if i < len(rounds[round_num]) - 1:
                        st.markdown("---")

def export_prompts():
    """Export prompts to TXT file"""
    if st.session_state.prompts:
        try:
            prompts_text = [prompt_data["prompt"] for prompt_data in st.session_state.prompts]
            file_content = "\n\n".join(prompts_text)
            
            # Create download button
            st.download_button(
                label="📥 Download Prompts as TXT",
                data=file_content,
                file_name=f"mj_prompts_{int(time.time())}.txt",
                mime="text/plain",
                key="download_prompts"
            )
            
            st.success(f"✅ Ready to download {len(st.session_state.prompts)} prompts!")
            
        except Exception as e:
            logger.error(f"Error exporting prompts: {e}")
            st.error(f"❌ Error exporting prompts: {e}")
    else:
        st.error("❌ No prompts to export. Generate some prompts first!")

if __name__ == "__main__":
    main()
