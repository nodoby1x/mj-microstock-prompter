# 🎨 MJ Microstock Prompter Pro

> **Advanced AI prompt generator for Midjourney and FLUX1.dev optimized for microstock success**

## 🌟 Overview

**MJ Microstock Prompter Pro** is a comprehensive AI-powered web application designed specifically for creating **high-converting prompts** for both **Midjourney** and **FLUX1.dev** that generate images optimized for **microstock sales success**. 

### 🎯 **What makes this special?**
- **Dual AI Model Support**: Generate prompts for both Midjourney and FLUX1.dev Stable Diffusion
- **Modern Flask Interface**: Professional web application with responsive Bootstrap UI
- **Multi-AI Providers**: Seamless switching between Gemini and OpenAI for diverse prompt generation
- **Image Metadata Tools**: Advanced metadata extraction and optimization for microstock platforms
- **Real-Time Optimization**: Live analysis and suggestions for better commercial potential
- **Microstock Intelligence**: Built-in knowledge of trending keywords and buyer preferences

---

## ✨ Key Features

### 🚀 **Core Functionality**
- **Dual Model Support**: Generate prompts for Midjourney and FLUX1.dev Stable Diffusion
- **Modern Flask Web Interface**: Professional responsive web application
- **Multi AI Providers**: Seamless switching between Gemini and OpenAI models
- **Smart Prompt Engineering**: Automatically injects high-value commercial keywords
- **Bulk Generation**: Process multiple prompts with CSV import/export
- **Image Metadata Tools**: Extract and optimize metadata for microstock platforms
- **Real-Time Analysis**: Live marketability scoring and optimization suggestions

### 🧠 **Microstock Intelligence**
- **Category Detection**: Automatically identifies business, tech, lifestyle, healthcare niches
- **Trend Analysis**: Suggests bestselling alternatives and trending subjects
- **Commercial Optimization**: Ensures diversity, professionalism, and market appeal
- **Quality Scoring**: Rates prompts for sales potential (0-100 scale)
- **Platform Optimization**: Optimize metadata for Shutterstock, Getty, Adobe Stock, iStock

### 🎨 **Advanced Features**
- **FLUX1.dev Integration**: Generate high-quality Stable Diffusion prompts with negative prompts
- **Preset Configurations**: Optimized settings for different AI models and use cases
- **Diversity Optimization**: Automatic inclusion of inclusive demographics
- **Professional Quality**: Studio lighting and composition recommendations
- **Batch Processing**: Handle multiple images and prompts efficiently

### 📊 **Professional Tools**
- **RESTful API**: Clean API endpoints for integration
- **Bootstrap 5 Interface**: Modern, responsive web design
- **Progress Tracking**: Real-time generation progress with statistics
- **Error Handling**: Comprehensive validation and retry mechanisms
- **Configuration Management**: Environment-based API key management

---

## 🖼️ Interface Preview

![MJ Microstock Prompter Interface](image.png)

*Professional interface designed for efficient microstock prompt generation*

---

## 🛠️ Technical Requirements

### **Prerequisites**
- **Python 3.8+** (Recommended: 3.9 or higher)
- **Flask** (Latest version)
- **API Keys**: Gemini and/or OpenAI accounts

### **Dependencies**
```
flask==2.3.3
python-dotenv==1.0.0
google-generativeai==0.3.2
openai==1.3.0
pillow>=9.0.0
piexif>=1.1.3
pandas>=1.3.0
difflib2>=0.1.0
```

---

## 🚀 Quick Start Installation

### **1. Clone Repository**
```bash
git clone https://github.com/nodoby1x/mj-microstock-prompter.git
cd mj-microstock-prompter
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

### **5. Launch Application**
```bash
# Flask web application
python app.py

# The application will be available at: http://localhost:5000
```

---

## 📚 Usage Guide

### **🎯 Single Prompt Generation**
1. **Navigate to GEN AI**: Access single prompt generator at `/gemini`
2. **Select AI Provider**: Choose between Gemini or OpenAI
3. **Configure Subject**: Enter your main image concept
4. **Add Details**: Specify style, theme, elements, and mood
5. **Real-Time Analysis**: View marketability score and suggestions
6. **Generate**: Create optimized microstock prompts
7. **Copy Results**: Use generated prompts in Midjourney

### **🤖 FLUX1.dev Generation**
1. **Navigate to FLUX1.dev**: Access FLUX generator at `/flux`
2. **Configure Parameters**: Set main subject, style, lighting, composition
3. **Quality Settings**: Choose inference steps and aspect ratio
4. **Negative Prompts**: Automatically generated for better results
5. **Generate**: Create Stable Diffusion optimized prompts

### **⚡ Bulk Processing**
1. **Navigate to Bulk Prompt**: Access batch generator at `/bulk`
2. **Upload CSV**: Use provided template or manual entry
3. **Configure Settings**: Set delays, retries, and batch sizes
4. **Monitor Progress**: Track generation with live statistics
5. **Export Results**: Download complete datasets with analysis

### **📸 Image Metadata Tools**
1. **Navigate to Image Metadata**: Access tools at `/metadata`
2. **Upload Images**: Single or batch image processing
3. **Extract Metadata**: AI-powered metadata extraction
4. **Optimize for Platforms**: Format for Shutterstock, Getty, Adobe Stock
5. **Export Data**: Download metadata in CSV or JSON format

### **📊 Optimization Features**
- **Marketability Scoring**: 0-100 commercial appeal rating
- **Missing Elements**: Identification of sales-boosting additions
- **Trending Alternatives**: Suggestions for higher-performing subjects
- **Category-Specific Tips**: Targeted advice for different industries
- **Platform Compliance**: Ensure metadata meets platform requirements

---

## 🎨 Microstock Optimization System

### **📈 High-Value Keywords**
- **Business**: professional, teamwork, leadership, success, corporate, diversity
- **Technology**: innovation, digital, AI, smart, connected, future, automation
- **Lifestyle**: wellness, balance, happiness, family, home, comfort, health
- **Healthcare**: medical, care, wellness, treatment, prevention, professional

### **🎯 Commercial Success Formula**
```
Subject + Professional/Diverse + Modern/Contemporary + Commercial Context = Higher Sales
```

### **✅ Best Practices**
- ✅ Include diverse demographics for broader appeal
- ✅ Add professional lighting and studio quality indicators
- ✅ Use trending, evergreen keywords
- ✅ Specify modern, contemporary styling
- ✅ Include negative space for text overlay

### **❌ Avoid These Elements**
- ❌ Trademarks, logos, or brand-specific content
- ❌ Seasonal or location-specific references
- ❌ Poor lighting or amateur composition
- ❌ Outdated technology or fashion
- ❌ Text or readable content in images

---

## 📁 Project Structure

```
mj-microstock-prompter/
├── app.py                      # Flask web application entry point
├── controller.py               # Enhanced AI prompt controller
├── microstock_optimizer.py     # Optimization analysis engine
├── microstock_templates.py     # Commercial templates and keywords
├── image_metadata_extractor.py # Image metadata processing
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── run_flask.py               # Flask migration verification
├── templates/                  # HTML templates
│   ├── base.html              # Base template with Bootstrap
│   ├── index.html             # Home page
│   ├── gemini.html            # Single prompt generator
│   ├── flux.html              # FLUX1.dev generator
│   ├── bulk.html              # Bulk processing interface
│   └── metadata.html          # Image metadata tools
├── static/                     # Static web assets
│   ├── style.css              # Custom CSS styling
│   └── app.js                 # JavaScript functions
├── uploads/                    # Image upload directory
├── .env.example               # Environment configuration template
├── README.md                  # This documentation
└── README_FLASK.md           # Flask migration documentation
```

---

## 🔧 Configuration Options

### **Environment Variables**
```bash
# API Configuration
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
FLASK_SECRET_KEY=your_secret_key

# Application Settings
DEFAULT_PROVIDER=gemini
DEFAULT_MODEL=gemini-2.5-flash
MAX_PROMPTS_PER_REQUEST=10
DEFAULT_DELAY_SECONDS=3
```

### **Prompt Presets**

#### **Midjourney Configuration**
- **High-Quality Business**: `--ar 16:9 --q 2 --stylize 100 --chaos 10`
- **Commercial Photography**: `--ar 16:9 --q 2 --stylize 50 --chaos 20`
- **Lifestyle/Editorial**: `--ar 16:9 --q 2 --stylize 200 --chaos 30`

#### **FLUX1.dev Configuration**
- **Aspect Ratios**: 1:1 (Square), 16:9 (Landscape), 9:16 (Portrait), 4:3, 3:2
- **Inference Steps**: 20-50 (default: 28)
- **Quality Tags**: high resolution, sharp focus, detailed, professional
- **Negative Prompts**: blurry, low quality, distorted, amateur

---

## 📊 Performance Metrics

### **Optimization Scoring**
- **90-100**: Excellent commercial potential, trending keywords, professional quality
- **70-89**: Good marketability, minor optimizations needed
- **50-69**: Average appeal, requires commercial enhancements
- **0-49**: Low sales potential, needs significant optimization

### **Success Indicators**
- ✅ Diverse demographic representation
- ✅ Professional/business context
- ✅ Modern, contemporary styling
- ✅ High-quality technical specifications
- ✅ Commercial keyword density

---

## 🔌 API Endpoints

The Flask application provides comprehensive RESTful API endpoints:

### **Prompt Generation**
- `POST /api/generate_prompts` - Generate Midjourney prompts
- `POST /api/generate_flux_prompts` - Generate FLUX1.dev prompts  
- `POST /api/bulk_generate` - Bulk prompt generation

### **Analysis & Optimization**
- `POST /api/analyze_prompt` - Analyze prompt commercial potential
- `POST /api/optimize_for_platform` - Platform-specific metadata optimization

### **Image Metadata**
- `POST /api/extract_metadata` - Single image metadata extraction
- `POST /api/batch_extract_metadata` - Batch image processing
- `POST /api/generate_image_keywords` - AI-powered keyword generation
- `POST /api/export_metadata` - Export metadata in CSV/JSON

## 🤝 Contributing

We welcome contributions to improve microstock optimization! Areas for enhancement:

- **New AI Providers**: Additional API integrations (Claude, Llama, etc.)
- **Enhanced Templates**: More category-specific optimizations
- **UI/UX Improvements**: Better user experience design
- **Performance**: Faster generation and processing
- **Analytics**: Advanced success tracking
- **Platform Integration**: Direct uploads to microstock platforms

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Microstock Industry**: Research and insights from leading stock photography platforms
- **AI Providers**: Google (Gemini) and OpenAI for powerful language models

---

## 🚀 **Ready to Generate Bestselling Microstock Prompts?**

**Launch the Flask web application and start creating prompts optimized for maximum commercial success!**

```bash
python app.py
```

Open your browser to **http://localhost:5000** and access:
- **🎨 GEN AI**: Single Midjourney prompt generation
- **🤖 FLUX1.dev**: Stable Diffusion prompt creation  
- **⚡ Bulk Prompt**: Batch processing for multiple prompts
- **📸 Image Metadata**: AI-powered metadata extraction and optimization

*Transform your creative ideas into profitable microstock images with dual AI model support and advanced optimization tools.*
