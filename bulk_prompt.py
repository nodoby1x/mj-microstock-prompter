import streamlit as st
from controller import PrompterGenerator
import pandas as pd
import io
import time
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

def BulkPrompt():
    st.title("Bulk Prompt Generator")
    st.markdown("Generate multiple prompts from CSV input or batch configuration")
    
    # API Configuration
    st.subheader("API Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        provider = st.selectbox("AI Provider", ["gemini", "openai"], key="bulk_provider")
        api_key = st.text_input(
            f"{provider.upper()} API Key", 
            value=os.getenv(f"{provider.upper()}_API_KEY", ""),
            type="password",
            key="bulk_api_key"
        )
    
    with col2:
        if provider == "gemini":
            model = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"], key="bulk_model")
        else:
            model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], key="bulk_model")
    
    # Input Method Selection
    st.subheader("Input Method")
    input_method = st.radio("Choose input method:", ["Manual Entry", "CSV Upload"], key="bulk_input_method")
    
    prompts_data = []
    
    if input_method == "Manual Entry":
        prompts_data = handle_manual_entry()
    else:
        prompts_data = handle_csv_upload()
    
    # Generation Settings
    st.subheader("Generation Settings")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delay_between = st.slider("Delay between prompts (seconds)", 1, 10, 3, key="bulk_delay")
    with col2:
        max_retries = st.slider("Max retries per prompt", 1, 5, 2, key="bulk_retries")
    with col3:
        batch_size = st.slider("Batch size", 1, 10, 5, key="bulk_batch_size")
    
    if st.button("Generate Bulk Prompts", key="generate_bulk"):
        if not api_key:
            st.error(f"Please provide {provider.upper()} API key")
            return
        
        if not prompts_data:
            st.error("Please provide input data")
            return
        
        generate_bulk_prompts(prompts_data, provider, api_key, model, delay_between, max_retries, batch_size)

def handle_manual_entry() -> List[Dict]:
    st.subheader("Manual Prompt Configuration")
    
    num_prompts = st.number_input("Number of prompts to generate", min_value=1, max_value=50, value=5, key="manual_count")
    
    prompts_data = []
    
    with st.expander("Configure Base Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            base_style = st.text_input("Default Image Style", "Photography", key="manual_style")
            base_theme = st.text_input("Default Theme", "", key="manual_theme")
            base_emotional = st.text_input("Default Emotional Tone", "", key="manual_emotional")
        with col2:
            base_color = st.text_input("Default Color Palette", "", key="manual_color")
            base_aspect = st.selectbox("Default Aspect Ratio", ["16:9", "1:1", "4:3", "9:16"], key="manual_aspect")
            base_elements = st.text_input("Default Elements", "", key="manual_elements")
    
    st.subheader("Individual Prompt Subjects")
    for i in range(num_prompts):
        with st.expander(f"Prompt {i+1}", expanded=i < 3):
            main_base = st.text_input(f"Main Subject {i+1}", key=f"manual_base_{i}")
            detail = st.text_input(f"Specific Details {i+1}", key=f"manual_detail_{i}")
            
            if main_base:
                prompts_data.append({
                    'main_base': main_base,
                    'image_style': base_style,
                    'theme': base_theme,
                    'elements': base_elements,
                    'emotional': base_emotional,
                    'color': base_color,
                    'image_detail': detail,
                    'aspect': base_aspect
                })
    
    return prompts_data

def handle_csv_upload() -> List[Dict]:
    st.subheader("CSV Upload")
    
    # Show expected format
    with st.expander("Expected CSV Format", expanded=False):
        sample_data = pd.DataFrame({
            'main_base': ['A cat playing', 'Mountain landscape', 'Coffee cup on desk'],
            'image_style': ['Photography', 'Digital Art', 'Photography'],
            'theme': ['Playful', 'Serene', 'Cozy'],
            'elements': ['Yarn ball, sunlight', 'Snow peaks, clouds', 'Steam, books'],
            'emotional': ['Happy', 'Peaceful', 'Warm'],
            'color': ['Warm tones', 'Cool blues', 'Earth tones'],
            'image_detail': ['Soft fur texture', 'Golden hour lighting', 'Ceramic texture'],
            'aspect': ['16:9', '16:9', '1:1']
        })
        st.dataframe(sample_data)
        
        # Download sample CSV
        csv_buffer = io.StringIO()
        sample_data.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Sample CSV",
            data=csv_buffer.getvalue(),
            file_name="sample_prompts.csv",
            mime="text/csv"
        )
    
    uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="csv_upload")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} rows from CSV")
            st.dataframe(df.head())
            
            # Convert DataFrame to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    return []

def generate_bulk_prompts(prompts_data: List[Dict], provider: str, api_key: str, 
                         model: str, delay: int, max_retries: int, batch_size: int):
    try:
        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.empty()
        
        generated_prompts = []
        total_prompts = len(prompts_data)
        
        for i, prompt_config in enumerate(prompts_data):
            status_text.text(f"Generating prompt {i+1}/{total_prompts}...")
            
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    result = generator.prompt_generator(**prompt_config)
                    
                    generated_prompts.append({
                        'index': i+1,
                        'main_base': prompt_config['main_base'],
                        'generated_prompt': result['text'].replace('.', '').strip(),
                        'provider': result['provider'],
                        'status': 'Success'
                    })
                    
                    success = True
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        st.warning(f"Retry {retry_count} for prompt {i+1}: {str(e)}")
                        time.sleep(2)
                    else:
                        generated_prompts.append({
                            'index': i+1,
                            'main_base': prompt_config['main_base'],
                            'generated_prompt': f"Error: {str(e)}",
                            'provider': provider,
                            'status': 'Failed'
                        })
            
            progress_bar.progress((i + 1) / total_prompts)
            
            # Add delay between requests
            if i < total_prompts - 1:
                time.sleep(delay)
        
        # Display results
        status_text.text("Generation complete!")
        
        results_df = pd.DataFrame(generated_prompts)
        st.subheader("Generated Prompts")
        st.dataframe(results_df)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as CSV
            csv_buffer = io.StringIO()
            results_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_buffer.getvalue(),
                file_name=f"generated_prompts_{int(time.time())}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download as TXT (prompts only)
            successful_prompts = results_df[results_df['status'] == 'Success']['generated_prompt'].tolist()
            txt_content = '\n\n'.join(successful_prompts)
            st.download_button(
                label="Download Prompts as TXT",
                data=txt_content,
                file_name=f"prompts_{int(time.time())}.txt",
                mime="text/plain"
            )
        
        # Statistics
        success_count = len(results_df[results_df['status'] == 'Success'])
        st.success(f"Successfully generated {success_count}/{total_prompts} prompts")
        
    except Exception as e:
        st.error(f"Error initializing generator: {e}")

if __name__ == "__main__":
    BulkPrompt()
