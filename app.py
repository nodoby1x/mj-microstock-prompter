from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from controller import PrompterGenerator
from microstock_optimizer import optimizer
from image_metadata_extractor import create_metadata_extractor
import os
import time
import json
import io
import pandas as pd
from typing import List, Dict
from dotenv import load_dotenv
import tempfile
import re
from werkzeug.utils import secure_filename
import zipfile

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/api/config')
def api_config():
    """Provide public configuration to the frontend."""
    return jsonify({
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', '')
    })

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gemini')
def gemini_page():
    return render_template('gemini.html')

@app.route('/flux')
def flux_page():
    return render_template('flux.html')

@app.route('/bulk')
def bulk_page():
    return render_template('bulk.html')

@app.route('/imagen')
def imagen_page():
    return render_template('imagen.html')

@app.route('/metadata')
def metadata_page():
    return render_template('metadata.html')

@app.route('/api/generate_prompts', methods=['POST'])
def generate_prompts():
    try:
        data = request.json
        api_key = data.get('api_key')
        provider = data.get('provider', 'gemini')
        model = data.get('model')
        main_base = data.get('main_base')
        image_style = data.get('image_style', 'Photography')
        image_details = data.get('image_details', '')
        theme = data.get('theme', '')
        elements = data.get('elements', '')
        emotional = data.get('emotional', '')
        color_palette = data.get('color_palette', '')
        aspect = data.get('aspect', '16:9')
        config_mj = data.get('config_mj', '--ar 16:9 --q 2')
        num_prompts = data.get('num_prompts', 1)
        round_count = data.get('round_count', 1)
        
        if not api_key or not main_base:
            return jsonify({'error': 'API key and main subject are required'}), 400
        
        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        generated_prompts = []
        
        for round_num in range(1, round_count + 1):
            for i in range(1, num_prompts + 1):
                try:
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
                    
                    clean_prompt = clean_generated_prompt(result["text"])
                    complete_prompt = f"{clean_prompt} {config_mj.strip()}"
                    metadata = generate_prompt_metadata(clean_prompt, main_base, theme, elements)
                    
                    generated_prompts.append({
                        "prompt": complete_prompt,
                        "title": metadata["title"],
                        "description": metadata["description"], 
                        "keywords": metadata["keywords"],
                        "category": metadata["category"],
                        "round": round_num,
                        "index": i,
                        "provider": result["provider"],
                        "timestamp": time.time()
                    })
                    
                    time.sleep(2)
                    
                except Exception as e:
                    return jsonify({'error': f'Error generating prompt: {str(e)}'}), 500
        
        return jsonify({'prompts': generated_prompts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_flux_prompts', methods=['POST'])
def generate_flux_prompts():
    try:
        data = request.json
        api_key = data.get('api_key')
        provider = data.get('provider', 'gemini')
        model = data.get('model')
        main_subject = data.get('main_subject')
        image_style = data.get('image_style', 'Photography')
        lighting = data.get('lighting', 'natural lighting')
        composition = data.get('composition', 'medium shot')
        details = data.get('details', '')
        quality_tags = data.get('quality_tags', [])
        mood = data.get('mood', '')
        color_scheme = data.get('color_scheme', '')
        negative_prompt = data.get('negative_prompt', 'blurry, low quality, distorted')
        aspect_ratio = data.get('aspect_ratio', '1:1 (Square)')
        inference_steps = data.get('inference_steps', 28)
        num_prompts = data.get('num_prompts', 1)
        round_count = data.get('round_count', 1)
        
        if not api_key or not main_subject:
            return jsonify({'error': 'API key and main subject are required'}), 400
        
        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        generated_prompts = []
        
        for round_num in range(1, round_count + 1):
            for i in range(1, num_prompts + 1):
                try:
                    result = generator.flux_prompt_generator(
                        main_base=main_subject,
                        image_style=image_style,
                        theme=mood,
                        elements=details,
                        emotional=mood,
                        color=color_scheme,
                        image_detail=details,
                        lighting=lighting,
                        composition=composition
                    )
                    
                    # Clean FLUX prompt (should already be clean, but safety check)
                    flux_prompt = clean_flux_prompt(result["text"])
                    
                    # Add quality tags if specified
                    if quality_tags:
                        flux_prompt += f", {', '.join(quality_tags)}"
                    metadata = generate_flux_prompt_metadata(flux_prompt, main_subject, image_style, mood)
                    
                    generated_prompts.append({
                        "prompt": flux_prompt,
                        "negative_prompt": negative_prompt,
                        "title": metadata["title"],
                        "description": metadata["description"], 
                        "keywords": metadata["keywords"],
                        "category": metadata["category"],
                        "aspect_ratio": aspect_ratio,
                        "inference_steps": inference_steps,
                        "round": round_num,
                        "index": i,
                        "provider": result["provider"],
                        "timestamp": time.time()
                    })
                    
                    time.sleep(2)
                    
                except Exception as e:
                    return jsonify({'error': f'Error generating FLUX prompt: {str(e)}'}), 500
        
        return jsonify({'prompts': generated_prompts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_imagen_prompts', methods=['POST'])
def generate_imagen_prompts():
    try:
        data = request.json
        api_key = data.get('api_key')
        provider = data.get('provider', 'gemini')
        model = data.get('model')
        main_subject = data.get('main_subject')
        image_style = data.get('image_style', 'Photography')
        setting = data.get('setting', '')
        composition = data.get('composition', 'rule of thirds')
        lighting = data.get('lighting', 'natural lighting')
        mood = data.get('mood', 'optimistic')
        color_palette = data.get('color_palette', 'neutral tones')
        details = data.get('details', '')
        theme = data.get('theme', '')
        elements = data.get('elements', '')
        negative_prompt = data.get('negative_prompt', 'text, logos, branding, trademarks, identifiable people, ugly, deformed, noisy, blurry, distorted, grainy')
        num_prompts = data.get('num_prompts', 1)
        round_count = data.get('round_count', 1)
        
        if not api_key or not main_subject:
            return jsonify({'error': 'API key and main subject are required'}), 400
        
        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        generated_prompts = []
        
        for round_num in range(1, round_count + 1):
            for i in range(1, num_prompts + 1):
                try:
                    result = generator.imagen_prompt_generator(
                        main_base=main_subject,
                        image_style=image_style,
                        theme=theme,
                        elements=elements,
                        emotional=mood,
                        color=color_palette,
                        image_detail=details,
                        lighting=lighting,
                        composition=composition,
                        setting=setting,
                        mood=mood
                    )
                    
                    # Clean Imagen prompt
                    imagen_prompt = clean_imagen_prompt(result["text"])
                    
                    metadata = generate_imagen_prompt_metadata(imagen_prompt, main_subject, image_style, mood, setting)
                    
                    generated_prompts.append({
                        "prompt": imagen_prompt,
                        "negative_prompt": negative_prompt,
                        "title": metadata["title"],
                        "description": metadata["description"], 
                        "keywords": metadata["keywords"],
                        "category": metadata["category"],
                        "round": round_num,
                        "index": i,
                        "provider": result["provider"],
                        "timestamp": time.time()
                    })
                    
                    time.sleep(2)
                    
                except Exception as e:
                    return jsonify({'error': f'Error generating Imagen prompt: {str(e)}'}), 500
        
        return jsonify({'prompts': generated_prompts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_storyboard', methods=['POST'])
def generate_storyboard():
    try:
        data = request.json
        api_key = data.get('api_key')
        provider = data.get('provider', 'gemini')
        model = data.get('model')
        context = data.get('context')
        keywords = data.get('keywords', [])
        num_scenes = data.get('num_scenes', 1)

        if not api_key or not context or not keywords:
            return jsonify({'error': 'API key, context, and keywords are required'}), 400

        if isinstance(keywords, str):
            keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        else:
            keywords_list = keywords

        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        result = generator.storyboard_generator(context=context, keywords=keywords_list, num_scenes=num_scenes)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk_generate', methods=['POST'])
def bulk_generate():
    try:
        data = request.json
        api_key = data.get('api_key')
        provider = data.get('provider', 'gemini')
        model = data.get('model')
        prompts_data = data.get('prompts_data', [])
        delay_between = data.get('delay_between', 3)
        max_retries = data.get('max_retries', 2)
        
        if not api_key or not prompts_data:
            return jsonify({'error': 'API key and prompts data are required'}), 400
        
        generator = PrompterGenerator(api_key=api_key, model_name=model, provider=provider)
        generated_prompts = []
        
        for i, prompt_config in enumerate(prompts_data):
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
                    if retry_count >= max_retries:
                        generated_prompts.append({
                            'index': i+1,
                            'main_base': prompt_config['main_base'],
                            'generated_prompt': f"Error: {str(e)}",
                            'provider': provider,
                            'status': 'Failed'
                        })
            
            time.sleep(delay_between)
        
        return jsonify({'prompts': generated_prompts})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_prompt', methods=['POST'])
def analyze_prompt():
    try:
        data = request.json
        main_base = data.get('main_base', '')
        theme = data.get('theme', '')
        elements = data.get('elements', '')
        
        if not main_base:
            return jsonify({'error': 'Main subject is required'}), 400
        
        analysis = optimizer.analyze_prompt_potential(main_base, theme, elements)
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/extract_metadata', methods=['POST'])
def extract_metadata():
    """Extract metadata from uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Get AI settings
        ai_key = request.form.get('ai_key')
        ai_provider = request.form.get('ai_provider', 'gemini')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Create metadata extractor
            extractor = create_metadata_extractor(ai_key, ai_provider)
            
            # Extract metadata
            metadata = extractor.extract_image_metadata(filepath)
            
            # Add file info
            metadata['upload_info'] = {
                'original_filename': filename,
                'upload_timestamp': timestamp,
                'file_path': filepath
            }
            
            return jsonify({
                'success': True,
                'metadata': metadata,
                'filename': unique_filename
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch_extract_metadata', methods=['POST'])
def batch_extract_metadata():
    """Extract metadata from multiple images"""
    try:
        if 'images' not in request.files:
            return jsonify({'error': 'No image files provided'}), 400
        
        files = request.files.getlist('images')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        # Get AI settings
        ai_key = request.form.get('ai_key')
        ai_provider = request.form.get('ai_provider', 'gemini')
        
        # Process each file
        results = []
        temp_files = []
        
        try:
            for file in files:
                if file.filename == '' or not allowed_file(file.filename):
                    continue
                
                # Save uploaded file
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                temp_files.append(filepath)
            
            if not temp_files:
                return jsonify({'error': 'No valid image files found'}), 400
            
            # Create metadata extractor
            extractor = create_metadata_extractor(ai_key, ai_provider)
            
            # Process images in batch
            batch_results = extractor.batch_process_images(temp_files)
            
            # Format results
            for result in batch_results:
                results.append({
                    'filename': os.path.basename(result['image_path']),
                    'success': result['success'],
                    'metadata': result.get('metadata', {}),
                    'error': result.get('error', ''),
                    'processed_at': result['processed_at']
                })
            
            return jsonify({
                'success': True,
                'results': results,
                'total_processed': len(results)
            })
            
        finally:
            # Clean up temp files
            for filepath in temp_files:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_image_keywords', methods=['POST'])
def generate_image_keywords():
    """Generate AI-powered keywords for image description"""
    try:
        data = request.json
        image_description = data.get('description', '')
        category = data.get('category', 'business')
        ai_key = data.get('ai_key')
        ai_provider = data.get('ai_provider', 'gemini')
        
        if not image_description:
            return jsonify({'error': 'Image description is required'}), 400
        
        if not ai_key:
            return jsonify({'error': 'AI API key is required'}), 400
        
        # Use the prompt generator to create keywords
        generator = PrompterGenerator(api_key=ai_key, provider=ai_provider)
        
        # Create a prompt for keyword generation
        keyword_prompt = (
            f"Generate 20 relevant keywords for a microstock image with this description: {image_description}\n"
            f"Category: {category}\n"
            f"Keywords should be:\n"
            f"- Relevant for stock photo buyers\n"
            f"- Commercially valuable\n"
            f"- Diverse in scope (technical, emotional, contextual)\n"
            f"- Separated by commas\n"
            f"- Professional and market-ready\n"
            f"Output only the keywords, no other text."
        )
        
        result = generator.prompt_generator(
            main_base=keyword_prompt,
            image_style="Keywords",
            theme="Commercial",
            elements="Stock Photography"
        )
        
        # Clean up the generated keywords
        keywords = result['text'].replace('\n', ', ').strip()
        keywords = ', '.join([kw.strip() for kw in keywords.split(',') if kw.strip()])
        
        # Analyze commercial potential
        analysis = optimizer.analyze_prompt_potential(image_description, category, keywords)
        
        return jsonify({
            'success': True,
            'keywords': keywords,
            'analysis': analysis,
            'provider': result['provider']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize_for_platform', methods=['POST'])
def optimize_for_platform():
    """Optimize image metadata for specific microstock platform"""
    try:
        data = request.json
        platform = data.get('platform', 'shutterstock')
        title = data.get('title', '')
        description = data.get('description', '')
        keywords = data.get('keywords', '')
        category = data.get('category', 'business')
        
        if not title or not description:
            return jsonify({'error': 'Title and description are required'}), 400
        
        # Platform-specific optimizations
        platform_requirements = {
            'shutterstock': {
                'title_max': 100,
                'description_max': 200,
                'keywords_max': 50,
                'requirements': [
                    'No people names or locations',
                    'Professional quality required',
                    'Model releases needed for people',
                    'Property releases for recognizable buildings'
                ]
            },
            'getty': {
                'title_max': 80,
                'description_max': 150,
                'keywords_max': 30,
                'requirements': [
                    'Premium quality only',
                    'Strict editorial guidelines',
                    'Comprehensive releases required',
                    'High commercial value'
                ]
            },
            'adobe_stock': {
                'title_max': 70,
                'description_max': 200,
                'keywords_max': 49,
                'requirements': [
                    'AI-generated content must be disclosed',
                    'No Adobe trademarks',
                    'Model releases required',
                    'Technical quality standards'
                ]
            },
            'istock': {
                'title_max': 100,
                'description_max': 200,
                'keywords_max': 50,
                'requirements': [
                    'Getty Images subsidiary',
                    'Professional standards',
                    'Exclusive content preferred',
                    'Diverse representation valued'
                ]
            }
        }
        
        platform_info = platform_requirements.get(platform, platform_requirements['shutterstock'])
        
        # Optimize content
        optimized = {
            'platform': platform,
            'title': title[:platform_info['title_max']],
            'description': description[:platform_info['description_max']],
            'keywords': keywords,
            'category': category,
            'requirements': platform_info['requirements'],
            'compliance_check': {
                'title_length': len(title) <= platform_info['title_max'],
                'description_length': len(description) <= platform_info['description_max'],
                'keywords_count': len(keywords.split(',')) <= platform_info['keywords_max']
            }
        }
        
        # Limit keywords if needed
        keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
        if len(keyword_list) > platform_info['keywords_max']:
            keyword_list = keyword_list[:platform_info['keywords_max']]
            optimized['keywords'] = ', '.join(keyword_list)
            optimized['keywords_truncated'] = True
        
        # Add optimization suggestions
        suggestions = []
        if len(title) > platform_info['title_max']:
            suggestions.append(f"Title too long - max {platform_info['title_max']} characters")
        if len(description) > platform_info['description_max']:
            suggestions.append(f"Description too long - max {platform_info['description_max']} characters")
        if len(keyword_list) > platform_info['keywords_max']:
            suggestions.append(f"Too many keywords - max {platform_info['keywords_max']} allowed")
        
        optimized['suggestions'] = suggestions
        optimized['compliant'] = len(suggestions) == 0
        
        return jsonify({
            'success': True,
            'optimized': optimized
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_metadata', methods=['POST'])
def export_metadata():
    """Export metadata in various formats"""
    try:
        data = request.json
        metadata_list = data.get('metadata_list', [])
        export_format = data.get('format', 'csv')
        
        if not metadata_list:
            return jsonify({'error': 'No metadata provided'}), 400
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f'.{export_format}') as temp_file:
            if export_format == 'csv':
                import csv
                writer = csv.writer(temp_file)
                
                # Write header
                headers = ['filename', 'title', 'description', 'keywords', 'category', 'width', 'height', 'file_size', 'quality_score']
                writer.writerow(headers)
                
                # Write data
                for item in metadata_list:
                    row = [
                        item.get('filename', ''),
                        item.get('title', ''),
                        item.get('description', ''),
                        item.get('keywords', ''),
                        item.get('category', ''),
                        item.get('width', ''),
                        item.get('height', ''),
                        item.get('file_size', ''),
                        item.get('quality_score', '')
                    ]
                    writer.writerow(row)
                    
            elif export_format == 'json':
                json.dump(metadata_list, temp_file, indent=2)
                
            else:
                return jsonify({'error': 'Unsupported format'}), 400
            
            temp_file_path = temp_file.name
        
        # Return file
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=f'image_metadata_{int(time.time())}.{export_format}',
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def clean_prompt(prompt_text: str, params_to_remove: list) -> str:
    """Clean and format a prompt by removing specified parameters."""
    clean_prompt = prompt_text.replace("/imagine", "").replace("`", "").strip()
    
    for param in params_to_remove:
        clean_prompt = re.sub(param, '', clean_prompt, flags=re.IGNORECASE)
    
    # Remove any remaining -- parameters
    clean_prompt = re.sub(r'--\w+(?:\s+[^\s\-]+)?', '', clean_prompt)
    
    # Clean up extra spaces and formatting
    clean_prompt = re.sub(r'\s+', ' ', clean_prompt)
    clean_prompt = clean_prompt.strip(' ,-.')
    
    return clean_prompt.strip() if clean_prompt.strip() else "professional business concept"

def clean_generated_prompt(prompt_text):
    """Clean Midjourney-specific parameters from generated prompts"""
    midjourney_params = [
        r'--ar\s+[\d:\.]+', r'--aspect\s+[\d:\.]+',
        r'--v\s+[\d\.]+', r'--version\s+[\d\.]+', 
        r'--stylize\s+\d+', r'--s\s+\d+',
        r'--chaos\s+\d+', r'--c\s+\d+',
        r'--quality\s+[\d\.]+', r'--q\s+[\d\.]+',
        r'--zoom\s+[\d\.]+', r'--z\s+[\d\.]+',
        r'--style\s+\w+', r'--st\s+\w+',
        r'--seed\s+\d+', r'--sameseed\s+\d+',
        r'--tile', r'--iw\s+[\d\.]+', r'--uplight', r'--upbeta', r'--upanime',
        r'--hd', r'--fast', r'--relax', r'--turbo'
    ]
    return clean_prompt(prompt_text, midjourney_params)

def clean_flux_prompt(prompt_text):
    """Clean and format FLUX1.dev prompts (should already be clean)"""
    midjourney_params = [
        r'--ar\s+[\d:\.]+', r'--aspect\s+[\d:\.]+',
        r'--v\s+[\d\.]+', r'--version\s+[\d\.]+', 
        r'--stylize\s+\d+', r'--s\s+\d+',
        r'--chaos\s+\d+', r'--c\s+\d+',
        r'--quality\s+[\d\.]+', r'--q\s+[\d\.]+',
        r'--zoom\s+[\d\.]+', r'--style\s+\w+', r'--seed\s+\d+'
    ]
    return clean_prompt(prompt_text, midjourney_params)

def clean_imagen_prompt(prompt_text):
    """Clean and format Google Imagen 4 prompts"""
    midjourney_params = [
        r'--ar\s+[\d:\.]+', r'--aspect\s+[\d:\.]+',
        r'--v\s+[\d\.]+', r'--version\s+[\d\.]+', 
        r'--stylize\s+\d+', r'--s\s+\d+',
        r'--chaos\s+\d+', r'--c\s+\d+',
        r'--quality\s+[\d\.]+', r'--q\s+[\d\.]+',
        r'--zoom\s+[\d\.]+', r'--style\s+\w+', r'--seed\s+\d+'
    ]
    return clean_prompt(prompt_text, midjourney_params)

def generate_prompt_metadata(prompt_text, main_base, theme, elements):
    try:
        keywords_list = []
        
        if main_base:
            keywords_list.extend(main_base.lower().split())
        if theme:
            keywords_list.extend(theme.lower().split())
        if elements:
            keywords_list.extend(elements.lower().split())
        
        common_keywords = ["professional", "business", "modern", "diverse", "corporate", "office", "success", "technology"]
        for keyword in common_keywords:
            if keyword in prompt_text.lower():
                keywords_list.append(keyword)
        
        unique_keywords = list(set(keywords_list))[:15]
        keywords_str = ", ".join(unique_keywords)
        
        if "businesswoman" in prompt_text.lower():
            title = "Professional Business Woman in Modern Office"
        elif "business" in prompt_text.lower():
            title = "Professional Business Scene"
        else:
            title = f"Professional {main_base.title() if main_base else 'Business'} Concept"
            
        description = f"High-quality professional image featuring {main_base.lower() if main_base else 'business concept'}"
        if theme:
            description += f" with {theme.lower()} theme"
        description += ". Perfect for commercial use and business presentations."
        
        if any(word in prompt_text.lower() for word in ["business", "office", "corporate", "professional"]):
            category = "Business"
        elif any(word in prompt_text.lower() for word in ["technology", "tech", "digital"]):
            category = "Technology"
        else:
            category = "Business"
            
        return {
            "title": title,
            "description": description,
            "keywords": keywords_str,
            "category": category
        }
        
    except Exception:
        return {
            "title": "Professional Business Concept",
            "description": "High-quality professional image perfect for commercial use.",
            "keywords": "professional, business, modern, commercial, corporate",
            "category": "Business"
        }

def generate_flux_prompt_metadata(prompt_text, main_subject, image_style, mood):
    try:
        keywords_list = []
        
        if main_subject:
            keywords_list.extend(main_subject.lower().split())
        if image_style:
            keywords_list.append(image_style.lower())
        if mood:
            keywords_list.extend(mood.lower().split())
        
        flux_keywords = ["photorealistic", "detailed", "sharp focus", "high quality", "cinematic", "professional"]
        for keyword in flux_keywords:
            if keyword in prompt_text.lower():
                keywords_list.append(keyword)
        
        unique_keywords = list(set(keywords_list))[:15]
        keywords_str = ", ".join(unique_keywords)
        
        if image_style == "Photography":
            title = f"Professional {main_subject.title()} Photography"
        elif image_style == "Digital Art":
            title = f"Digital Art of {main_subject.title()}"
        else:
            title = f"{image_style} {main_subject.title()}"
            
        description = f"High-quality {image_style.lower()} featuring {main_subject.lower()}"
        if mood:
            description += f" with {mood.lower()} mood"
        description += ". Generated using FLUX1.dev for professional results."
        
        if any(word in prompt_text.lower() for word in ["business", "office", "corporate", "professional"]):
            category = "Business"
        elif any(word in prompt_text.lower() for word in ["portrait", "person", "face"]):
            category = "People"
        else:
            category = "Creative"
            
        return {
            "title": title,
            "description": description,
            "keywords": keywords_str,
            "category": category
        }
        
    except Exception:
        return {
            "title": f"FLUX1.dev {main_subject.title() if main_subject else 'Creative'} Image",
            "description": "High-quality image generated with FLUX1.dev for professional use.",
            "keywords": "flux, stable diffusion, high quality, professional, creative",
            "category": "Creative"
        }

def generate_imagen_prompt_metadata(prompt_text, main_subject, image_style, mood, setting):
    try:
        keywords_list = []
        
        if main_subject:
            keywords_list.extend(main_subject.lower().split())
        if image_style:
            keywords_list.append(image_style.lower())
        if mood:
            keywords_list.extend(mood.lower().split())
        if setting:
            keywords_list.extend(setting.lower().split())
        
        imagen_keywords = ["photorealistic", "high-resolution", "commercial", "professional", "Adobe Stock", "detailed"]
        for keyword in imagen_keywords:
            if keyword.lower() in prompt_text.lower():
                keywords_list.append(keyword.lower())
        
        unique_keywords = list(set(keywords_list))[:15]
        keywords_str = ", ".join(unique_keywords)
        
        if image_style == "Photography":
            title = f"Professional {main_subject.title()} Photography"
        elif image_style == "Digital Art":
            title = f"Digital Art of {main_subject.title()}"
        elif image_style == "Conceptual Illustration":
            title = f"Conceptual {main_subject.title()} Illustration"
        else:
            title = f"{image_style} {main_subject.title()}"
            
        description = f"High-quality {image_style.lower()} featuring {main_subject.lower()}"
        if setting:
            description += f" in {setting.lower()}"
        if mood:
            description += f" with {mood.lower()} mood"
        description += ". Generated using Google Imagen 4 for Adobe Stock commercial use."
        
        if any(word in prompt_text.lower() for word in ["business", "office", "corporate", "professional"]):
            category = "Business"
        elif any(word in prompt_text.lower() for word in ["portrait", "person", "face", "people"]):
            category = "People"
        elif any(word in prompt_text.lower() for word in ["technology", "tech", "digital", "innovation"]):
            category = "Technology"
        elif any(word in prompt_text.lower() for word in ["lifestyle", "home", "wellness", "health"]):
            category = "Lifestyle"
        else:
            category = "Creative"
            
        return {
            "title": title,
            "description": description,
            "keywords": keywords_str,
            "category": category
        }
        
    except Exception:
        return {
            "title": f"Google Imagen 4 {main_subject.title() if main_subject else 'Creative'} Image",
            "description": "High-quality image generated with Google Imagen 4 for Adobe Stock commercial use.",
            "keywords": "imagen, google, high quality, professional, adobe stock, commercial",
            "category": "Creative"
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)