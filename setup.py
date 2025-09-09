"""
Setup script for the Food Nutrition Analyzer application.
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_secrets_file():
    """Check if secrets.toml exists and has API key"""
    secrets_path = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_path):
        print("❌ secrets.toml file not found!")
        return False
    
    with open(secrets_path, 'r') as f:
        content = f.read()
        if "your-openai-api-key-here" in content:
            print("⚠️  Please update your OpenAI API key in .streamlit/secrets.toml")
            return False
    
    print("✅ API key configuration looks good!")
    return True

def create_directories():
    """Create necessary directories"""
    os.makedirs(".streamlit", exist_ok=True)
    print("✅ Directories created!")

def main():
    print("🍽️ Food Nutrition Analyzer Setup")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return
    
    # Check secrets file
    if not check_secrets_file():
        print("\n📝 Next steps:")
        print("1. Get your OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Update .streamlit/secrets.toml with your API key")
        print("3. Run: streamlit run app.py")
        return
    
    print("\n🎉 Setup complete! You can now run the app with:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()
