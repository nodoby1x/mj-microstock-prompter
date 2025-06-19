# 🎨 MJ Microstock Prompter Pro

> **Advanced Midjourney prompt generator optimized for maximum microstock sales success**

*Originally based on [Midjourney-Prompt-Builder](https://github.com/Nafi7393/Midjourney-Prompt-Builder) by [Nafi7393](https://github.com/Nafi7393), now completely enhanced for professional microstock photography.*

## 🌟 Overview

**MJ Microstock Prompter Pro** is a comprehensive AI-powered tool designed specifically for creating **high-converting Midjourney prompts** that generate images optimized for **microstock sales success**. 

### 🎯 **What makes this special?**
- **Commercial-First Approach**: Every prompt is optimized for maximum microstock appeal
- **Multi-AI Support**: Both Gemini and OpenAI integration for diverse prompt generation
- **Real-Time Optimization**: Live analysis and suggestions for better commercial potential
- **Microstock Intelligence**: Built-in knowledge of trending keywords and buyer preferences

---

## ✨ Key Features

### 🚀 **Core Functionality**
- **Dual AI Providers**: Seamless switching between Gemini and OpenAI models
- **Smart Prompt Engineering**: Automatically injects high-value commercial keywords
- **Bulk Generation**: Process multiple prompts with CSV import/export
- **Real-Time Analysis**: Live marketability scoring and optimization suggestions
- **Export Options**: Download prompts as organized TXT files with timestamps

### 🧠 **Microstock Intelligence**
- **Category Detection**: Automatically identifies business, tech, lifestyle, healthcare niches
- **Trend Analysis**: Suggests bestselling alternatives and trending subjects
- **Commercial Optimization**: Ensures diversity, professionalism, and market appeal
- **Quality Scoring**: Rates prompts for sales potential (0-100 scale)

### 🎨 **Advanced Features**
- **Preset Configurations**: Optimized Midjourney settings for different use cases
- **Diversity Optimization**: Automatic inclusion of inclusive demographics
- **Professional Quality**: Studio lighting and composition recommendations
- **SEO-Friendly**: High-demand keywords and commercial terminology

### 📊 **Professional Tools**
- **Multi-Page Interface**: Dedicated pages for single and bulk generation
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
- **Streamlit** (Latest version)
- **API Keys**: Gemini and/or OpenAI accounts

### **Dependencies**
```
streamlit==1.28.0
python-dotenv==1.0.0
google-generativeai==0.3.2
openai==1.3.0
pandas (for CSV processing)
```

---

## 🚀 Quick Start Installation

### **1. Clone Repository**
```bash
git clone https://github.com/your-username/mj-microstock-prompter.git
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
```

### **5. Launch Application**
```bash
# Multi-page interface (Recommended)
streamlit run app.py

# Legacy single-page interface
streamlit run web.py
```

---

## 📚 Usage Guide

### **🎯 Single Prompt Generation**
1. **Select AI Provider**: Choose between Gemini or OpenAI
2. **Configure Subject**: Enter your main image concept
3. **Add Details**: Specify style, theme, elements, and mood
4. **Real-Time Analysis**: View marketability score and suggestions
5. **Generate**: Create optimized microstock prompts
6. **Export**: Download as TXT files

### **⚡ Bulk Processing**
1. **Upload CSV**: Use provided template or manual entry
2. **Configure Settings**: Set delays, retries, and batch sizes
3. **Monitor Progress**: Track generation with live statistics
4. **Export Results**: Download complete datasets with analysis

### **📊 Optimization Features**
- **Marketability Scoring**: 0-100 commercial appeal rating
- **Missing Elements**: Identification of sales-boosting additions
- **Trending Alternatives**: Suggestions for higher-performing subjects
- **Category-Specific Tips**: Targeted advice for different industries

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
├── app.py                    # Multi-page application entry
├── web.py                    # Legacy single-page interface
├── gemini_page.py           # Single prompt generator
├── bulk_prompt.py           # Bulk processing interface
├── controller.py            # Enhanced AI prompt controller
├── microstock_optimizer.py  # Optimization analysis engine
├── microstock_templates.py  # Commercial templates and keywords
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── style.css             # UI styling
└── README.md            # This documentation
```

---

## 🔧 Configuration Options

### **Environment Variables**
```bash
# API Configuration
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# Application Settings
DEFAULT_PROVIDER=gemini
DEFAULT_MODEL=gemini-1.5-flash
MAX_PROMPTS_PER_REQUEST=10
DEFAULT_DELAY_SECONDS=3
```

### **Microstock Presets**
- **High-Quality Business**: `--ar 16:9 --q 2 --stylize 100 --chaos 10`
- **Commercial Photography**: `--ar 16:9 --q 2 --stylize 50 --chaos 20`
- **Lifestyle/Editorial**: `--ar 16:9 --q 2 --stylize 200 --chaos 30`

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

## 🤝 Contributing

We welcome contributions to improve microstock optimization! Areas for enhancement:

- **New AI Providers**: Additional API integrations
- **Enhanced Templates**: More category-specific optimizations
- **UI/UX Improvements**: Better user experience design
- **Performance**: Faster generation and processing
- **Analytics**: Advanced success tracking

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Original Project**: [Midjourney-Prompt-Builder](https://github.com/Nafi7393/Midjourney-Prompt-Builder) by [Nafi7393](https://github.com/Nafi7393)
- **Microstock Industry**: Research and insights from leading stock photography platforms
- **AI Providers**: Google (Gemini) and OpenAI for powerful language models

---

## 🚀 **Ready to Generate Bestselling Microstock Prompts?**

**Launch the application and start creating prompts optimized for maximum commercial success!**

```bash
streamlit run app.py
```

*Transform your creative ideas into profitable microstock images with AI-powered optimization.*
