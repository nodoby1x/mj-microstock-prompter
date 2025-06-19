import streamlit as st
from controller import PrompterGenerator
from dotenv import load_dotenv
import os
import time
import pandas as pd
from typing import List
from microstock_optimizer import optimizer

load_dotenv()

def GeminiPage():
    st.title("Single Prompt Generator")
    st.markdown("Generate individual Midjourney prompts using AI")
    
    # Load custom CSS
    try:
        with open("style.css", "r") as file:
            content = file.read()
        custom_css = f"<style>{content}</style>"
        st.markdown(custom_css, unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    # API Configuration
    st.sidebar.header("Settings")
    
    provider = st.sidebar.selectbox("AI Provider", ["gemini", "openai"], key="single_provider")
    
    # Get API key from environment or user input
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
        key="single_api_key"
    )
    
    model = st.sidebar.selectbox("Model", model_options, key="single_model")
    
    # Generation settings
    num_prompts = st.sidebar.slider("Prompts per Round", min_value=1, max_value=10, value=1, key="single_num_prompts")
    round_count = st.sidebar.slider("Number of Rounds", min_value=1, max_value=20, value=1, key="single_rounds")
    rest_time = st.sidebar.slider("Round Interval (seconds)", min_value=5, max_value=30, value=15, key="single_rest")
    
    # Main interface
    st.subheader("📝 Microstock-Optimized Prompt Configuration")
    
    # Row 1: Main inputs
    row1_col1, row1_col2 = st.columns(2)
    main_base = row1_col1.text_input("Main Subject *", "", help="The primary subject or concept for your image", placeholder="e.g., professional businesswoman")
    image_style = row1_col2.text_input("Image Style", "Photography", help="Photography, Digital Art, Illustration, etc.")
    
    # Real-time optimization analysis
    if main_base:
        with st.expander("📊 Microstock Optimization Analysis", expanded=False):
            analysis = optimizer.analyze_prompt_potential(main_base, "", "")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                score_color = "🟢" if analysis['marketability_score'] >= 70 else "🟡" if analysis['marketability_score'] >= 40 else "🔴"
                st.metric("Marketability Score", f"{analysis['marketability_score']}/100 {score_color}")
            with col2:
                st.metric("Detected Category", analysis['category'].title())
            with col3:
                st.metric("Commercial Potential", "High" if analysis['marketability_score'] >= 70 else "Medium" if analysis['marketability_score'] >= 40 else "Low")
            
            if analysis['suggestions']:
                st.subheader("💡 Optimization Suggestions")
                for suggestion in analysis['suggestions'][:3]:
                    st.info(f"💡 {suggestion}")
            
            if analysis['trending_alternatives']:
                st.subheader("🔥 Trending Alternatives")
                for i, alt in enumerate(analysis['trending_alternatives'][:3]):
                    st.success(f"✨ {alt}")
            
            if analysis['missing_elements']:
                st.subheader("⚠️ Missing High-Value Elements")
                for element in analysis['missing_elements']:
                    st.warning(f"Consider adding: {element}")
    
    # Row 2: Details
    image_details = st.text_input("Image Details", "", help="Specific details about the image", placeholder="e.g., holding laptop, professional attire")
    
    # Row 3: Additional elements
    row3_col1, row3_col2 = st.columns(2)
    elements = row3_col1.text_input("Elements", "", help="Specific objects or elements to include", placeholder="e.g., modern office, natural lighting")
    aspect = row3_col2.selectbox("Aspect Ratio", ["16:9", "1:1", "4:3", "9:16", "3:2"], help="Image aspect ratio for different platforms")
    
    # Row 4: Mood and style
    row4_col1, row4_col2, row4_col3 = st.columns(3)
    theme = row4_col1.text_input("Theme", "", help="Overall theme or concept", placeholder="e.g., Success, Innovation")
    emotional = row4_col2.text_input("Emotional Tone", "", help="Happy, confident, professional, etc.", placeholder="e.g., Confident, Professional")
    color_palette = row4_col3.text_input("Color Palette", "", help="Modern, professional color schemes", placeholder="e.g., Corporate blues, Warm naturals")
    
    # Microstock-optimized Midjourney configuration
    st.subheader("🎯 Microstock-Optimized MJ Configuration")
    
    # Preset configurations for different uses
    preset_configs = {
        "High-Quality Business": f"--ar {aspect} --q 2 --stylize 100 --chaos 10",
        "Commercial Photography": f"--ar {aspect} --q 2 --stylize 50 --chaos 20",
        "Lifestyle/Editorial": f"--ar {aspect} --q 2 --stylize 200 --chaos 30",
        "Custom": f"--ar {aspect} --q 2 --chaos 50"
    }
    
    preset_choice = st.selectbox("Microstock Preset", list(preset_configs.keys()), help="Optimized settings for different microstock uses")
    
    if preset_choice == "Custom":
        config_mj = st.text_input(
            "Custom MJ Parameters", 
            preset_configs[preset_choice],
            help="Midjourney-specific parameters optimized for microstock"
        )
    else:
        config_mj = preset_configs[preset_choice]
        st.code(config_mj, language="bash")
        st.info(f"Using {preset_choice} preset - optimized for commercial microstock use")
    
    # Microstock enhancement suggestions
    with st.expander("🎯 Microstock Success Tips", expanded=False):
        category = "business"  # Default
        if main_base:
            analysis = optimizer.analyze_prompt_potential(main_base, theme or "", elements or "")
            category = analysis['category']
        
        bestselling_examples = optimizer.get_bestselling_prompts(category)
        st.subheader(f"🏆 Top-Selling {category.title()} Prompts")
        for example in bestselling_examples[:3]:
            st.success(f"✨ {example}")
        
        st.subheader("📈 Quick Wins for Higher Sales")
        quick_wins = [
            "Add 'diverse' or 'multicultural' for broader appeal",
            "Include 'professional' for business market",
            "Specify 'modern' or 'contemporary' styling",
            "Add 'studio lighting' for quality indication",
            "Include negative space for text overlay"
        ]
        for win in quick_wins:
            st.info(f"💰 {win}")
    
    # Initialize session state
    if "prompts" not in st.session_state:
        st.session_state.prompts = []
    if "generation_stats" not in st.session_state:
        st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎨 Generate Microstock Prompts", key="generate_single", type="primary"):
            generate_prompts(api_key, provider, model, main_base, image_style, image_details,
                           theme, elements, emotional, color_palette, aspect, config_mj,
                           num_prompts, round_count, rest_time)
    
    with col2:
        if st.button("Clear All", key="clear_all"):
            st.session_state.prompts.clear()
            st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}
            st.rerun()
    
    with col3:
        if st.button("Export TXT", key="export_single_txt"):
            export_prompts_txt()
    
    # Display generation statistics
    if st.session_state.generation_stats["total"] > 0:
        stats = st.session_state.generation_stats
        st.metric(
            "Generation Stats", 
            f"{stats['successful']}/{stats['total']}",
            f"{stats['failed']} failed" if stats['failed'] > 0 else "All successful"
        )
    
    # Display generated prompts
    display_generated_prompts()
    
    # Additional microstock resources
    with st.expander("📚 Microstock Marketing Resources", expanded=False):
        st.subheader("📈 Top Microstock Keywords by Category")
        
        categories = ["Business", "Technology", "Lifestyle", "Healthcare", "Education", "Finance"]
        selected_cat = st.selectbox("View keywords for:", categories)
        
        keyword_sets = {
            "Business": ["professional", "teamwork", "leadership", "success", "corporate", "meeting", "handshake", "growth"],
            "Technology": ["innovation", "digital", "AI", "smart", "connected", "future", "tech", "mobile"],
            "Lifestyle": ["wellness", "balance", "happiness", "family", "home", "comfort", "health", "joy"],
            "Healthcare": ["medical", "care", "wellness", "health", "treatment", "prevention", "diagnosis"],
            "Education": ["learning", "knowledge", "study", "skill", "training", "development", "academic"],
            "Finance": ["investment", "savings", "planning", "wealth", "security", "banking", "financial"]
        }
        
        if selected_cat in keyword_sets:
            keywords = keyword_sets[selected_cat]
            st.success(f"🎯 High-value {selected_cat.lower()} keywords: {', '.join(keywords)}")
        
        st.subheader("💡 Microstock Success Formula")
        st.info("📊 **Subject** + **Professional/Diverse** + **Modern/Contemporary** + **Commercial Context** = **Higher Sales**")
        
        st.subheader("🚫 What to Avoid")
        avoid_items = [
            "Trademarks or brand logos", "Seasonal content (unless specific)", "Overly specific locations",
            "Poor lighting or composition", "Outdated technology or fashion", "Text or readable content"
        ]
        for item in avoid_items:
            st.warning(f"❌ {item}")

def generate_prompts(api_key: str, provider: str, model: str, main_base: str, image_style: str,
                    image_details: str, theme: str, elements: str, emotional: str, 
                    color_palette: str, aspect: str, config_mj: str, 
                    num_prompts: int, round_count: int, rest_time: int):
    
    # Validation
    if not api_key.strip():
        st.error(f"❌ Please enter your {provider.upper()} API Key to generate microstock-optimized prompts.")
        return
    
    if not main_base.strip():
        st.error("❌ Please fill the main subject to create microstock-optimized prompts.")
        return
    
    try:
        # Clear previous prompts for new generation
        st.session_state.prompts.clear()
        st.session_state.generation_stats = {"total": 0, "successful": 0, "failed": 0}
        
        # Progress tracking
        total_prompts = num_prompts * round_count
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        current_prompt = 0
        
        # Generate prompts for multiple rounds
        for round_num in range(1, round_count + 1):
            status_text.info(f"Starting Round {round_num}/{round_count}...")
            
            # Create a new instance of the PrompterGenerator for each round
            generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
            
            # Generate the specified number of prompts
            for i in range(1, num_prompts + 1):
                try:
                    status_text.info(f"Generating prompt {i}/{num_prompts} in Round {round_num}...")
                    
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
                    time.sleep(3)  # Delay between requests
                    
                except Exception as e:
                    st.error(f"❌ Error generating prompt {i} in Round {round_num}: {str(e)}")
                    st.session_state.generation_stats["failed"] += 1
                
                current_prompt += 1
                progress_bar.progress(current_prompt / total_prompts)
            
            # Pause before the next round
            if round_num < round_count:
                status_text.info(f"Resting for {rest_time} seconds before the next round...")
                time.sleep(rest_time)
        
        st.session_state.generation_stats["total"] = total_prompts
        status_text.success("✅ Microstock optimization complete!")
        
        if st.session_state.generation_stats["successful"] > 0:
            st.balloons()
            st.success("🏆 **Pro Tip**: Each generated prompt has been optimized with commercial keywords, diversity elements, and professional quality indicators for maximum microstock sales potential!")
        
    except Exception as e:
        st.error(f"❌ Error initializing generator: {str(e)}")

def display_generated_prompts():
    """Display generated prompts in an organized way"""
    if st.session_state.prompts:
        st.subheader("🚀 Generated Microstock-Optimized Prompts")
        st.info("🎯 Each prompt has been optimized for maximum commercial appeal and microstock sales potential!")
        
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
                    st.markdown(f"**Prompt {prompt_data['index']}** *({prompt_data['provider']})* 🎯")
                    
                    # Show the prompt
                    st.text_area(
                        f"Round {round_num} - Prompt {prompt_data['index']}",
                        prompt_data["prompt"],
                        height=120,
                        key=f"prompt_display_{round_num}_{i}",
                        label_visibility="collapsed"
                    )
                    
                    # Quick analysis of the generated prompt
                    prompt_text = prompt_data["prompt"]
                    commercial_keywords = ["professional", "diverse", "business", "modern", "commercial", "high-quality", "studio", "corporate"]
                    found_keywords = [kw for kw in commercial_keywords if kw.lower() in prompt_text.lower()]
                    
                    if found_keywords:
                        st.success(f"🎯 Commercial keywords found: {', '.join(found_keywords)}")
                    else:
                        st.warning("💡 Consider adding commercial keywords for better microstock appeal")
                    
                    # Sales potential indicator
                    if len(found_keywords) >= 3:
                        st.success("📈 HIGH sales potential - excellent commercial optimization!")
                    elif len(found_keywords) >= 1:
                        st.info("📉 MEDIUM sales potential - could use more commercial keywords")
                    else:
                        st.warning("📉 LOW sales potential - needs commercial optimization")
                    
                    if i < len(rounds[round_num]) - 1:
                        st.markdown("---")

def export_prompts_txt():
    """Export prompts to TXT file"""
    if st.session_state.prompts:
        try:
            prompts_text = []
            for prompt_data in st.session_state.prompts:
                prompts_text.append(prompt_data["prompt"])
            
            file_content = "\n\n".join(prompts_text)
            
            st.download_button(
                label="Download Prompts as TXT",
                data=file_content,
                file_name=f"prompts_{int(time.time())}.txt",
                mime="text/plain",
                key="download_txt_single"
            )
            
        except Exception as e:
            st.error(f"❌ Error exporting prompts: {e}")
    else:
        st.error("No prompts to export.")
        st.info("💡 Generate some microstock-optimized prompts first to unlock export features!")

if __name__ == "__main__":
    GeminiPage()