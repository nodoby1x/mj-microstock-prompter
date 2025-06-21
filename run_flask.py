#!/usr/bin/env python3
"""
Simple test script to verify Flask migration
Run this after setting up your virtual environment and installing Flask
"""

try:
    from flask import Flask
    print("✅ Flask is installed and importable")
    
    # Try to import our app
    from app import app
    print("✅ Flask app imported successfully")
    
    print("🚀 Flask migration completed successfully!")
    print("📝 To run the application:")
    print("   1. Activate your virtual environment: source .venv/Scripts/activate")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Run the app: python app.py")
    print("   4. Open browser to: http://localhost:5000")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📋 Please install Flask dependencies first:")
    print("   pip install flask python-dotenv google-generativeai openai pillow piexif pandas")

except Exception as e:
    print(f"❌ Error: {e}")