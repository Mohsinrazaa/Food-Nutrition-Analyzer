import streamlit as st
import base64
import json
import logging
import io
from openai import OpenAI
from PIL import Image
import os
import dotenv
dotenv.load_dotenv()
from config import (
    OPENAI_MODEL, 
    OPENAI_TEMPERATURE, 
    SUPPORTED_IMAGE_FORMATS,
    APP_TITLE,
    APP_ICON,
    APP_LAYOUT,
    DEFAULT_NON_FOOD_NUTRITION,
    DEFAULT_UNKNOWN_NUTRITION
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client with proper API key handling"""
    try:
        # Try to get API key from Streamlit secrets first
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            # Fallback to environment variable
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it in .streamlit/secrets.toml or as an environment variable.")
        
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")
        return None

system_prompt = """You are a Food Nutrition Analyzer AI. You will receive a food image and your task is to identify the dish and provide its estimated nutritional information in JSON format.

Rules:
1. If the image clearly contains food, analyze it and return the following JSON strictly:
{
    "food_name": "<dish name>",
    "calories": <integer>,
    "nutritional_facts": {
        "protein": "<value in g>",
        "carbohydrates": "<value in g>",
        "total_fat": "<value in g>",
        "fiber": "<value in g>",
        "sodium": "<value in mg>"
    }
}

2. If the image is NOT food or is irrelevant (e.g., scenery, humans, objects, random items), respond with:
{
    "food_name": "Not Food",
    "calories": 0,
    "nutritional_facts": {
        "protein": "0g",
        "carbohydrates": "0g",
        "total_fat": "0g",
        "fiber": "0g",
        "sodium": "0mg"
    }
}

3. Keep the response concise and valid JSON only (no extra explanations, no text outside the JSON).
"""

def analyze_food_image(file_obj):
    """
    Takes an uploaded image file and returns JSON response
    with food name, calories, and nutritional facts.
    If not food, returns 'Not Food' JSON.
    """
    try:
        # Get OpenAI client
        client = get_openai_client()
        if not client:
            return DEFAULT_UNKNOWN_NUTRITION
        
        # Process image
        img_bytes = file_obj.read()
        
        # Convert image to RGB if needed and determine format
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        # Make API call
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this food image and provide nutritional information."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=500
        )
    except Exception as e:
        logger.error(f"Error in analyze_food_image: {e}")
        return DEFAULT_UNKNOWN_NUTRITION

    result = response.choices[0].message.content.strip()
   
    try:
        if result.startswith('```json') and result.endswith('```'):
            result = result[7:-3].strip()  
        elif result.startswith('```') and result.endswith('```'):
            result = result[3:-3].strip() 
       
        parsed_json = json.loads(result)
        return parsed_json
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Raw response: {result}")

        return DEFAULT_UNKNOWN_NUTRITION

def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT
    )
    
    st.title("🍽️ Food Nutrition Analyzer")
    st.markdown("Upload an image of food to get detailed nutritional information!")
    
    # Debug information (only show in development)
    if st.checkbox("Show Debug Info", help="Enable this to see debugging information"):
        st.write("**Debug Information:**")
        try:
            client = get_openai_client()
            if client:
                st.success("✅ OpenAI client initialized successfully")
            else:
                st.error("❌ Failed to initialize OpenAI client")
        except Exception as e:
            st.error(f"❌ Error initializing OpenAI client: {e}")
        
        # Show API key status (masked)
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-openai-api-key-here":
            st.success(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")
        else:
            st.error("❌ API key not found or not configured")
    
    # Sidebar for image upload
    with st.sidebar:
        st.header("📸 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=SUPPORTED_IMAGE_FORMATS,
            help="Upload an image of food to analyze its nutritional content"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 Analysis Results")
        
        if uploaded_file is not None:
            with st.spinner("Analyzing your food image..."):
                try:
                    # Reset file pointer
                    uploaded_file.seek(0)
                    result = analyze_food_image(uploaded_file)
                    
                    # Store result in session state for use in other columns
                    st.session_state.analysis_result = result
                    
                    # Display results
                    if result["food_name"] == "Not Food":
                        st.warning("⚠️ The uploaded image doesn't appear to contain food.")
                    elif result["food_name"] == "Unknown":
                        st.error("❌ Unable to analyze the image. Please try a clearer image.")
                    else:
                        st.success(f"✅ Successfully analyzed: **{result['food_name']}**")
                    
                    # Display food name and calories
                    st.metric("Food Name", result["food_name"])
                    st.metric("Calories", f"{result['calories']} kcal")
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing image: {str(e)}")
                    logger.error(f"Error in analyze_food_image: {e}")
                    st.session_state.analysis_result = DEFAULT_UNKNOWN_NUTRITION
        else:
            st.info("👆 Please upload an image to get started!")
    
    with col2:
        st.header("🥗 Nutritional Facts")
        
        if uploaded_file is not None and hasattr(st.session_state, 'analysis_result'):
            result = st.session_state.analysis_result
            if result["food_name"] not in ["Not Food", "Unknown"]:
                # Create a nice display of nutritional facts
                nutrition = result["nutritional_facts"]
                
                # Display nutritional facts in a structured way
                st.markdown("### Macronutrients")
                col2a, col2b = st.columns(2)
                
                with col2a:
                    st.metric("Protein", nutrition["protein"])
                    st.metric("Carbohydrates", nutrition["carbohydrates"])
                
                with col2b:
                    st.metric("Total Fat", nutrition["total_fat"])
                    st.metric("Fiber", nutrition["fiber"])
                
                st.metric("Sodium", nutrition["sodium"])
                
                # Additional info
                st.markdown("### Additional Information")
                st.info("💡 This analysis is based on AI estimation and should be used as a general guide. For precise nutritional information, consult a nutritionist or food database.")
            else:
                st.warning("No nutritional information available for non-food items.")
        else:
            st.info("Upload an image to see nutritional facts here!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Note:** This app uses AI to analyze food images and provide estimated nutritional information. "
        "Results are approximate and should not replace professional nutritional advice."
    )

if __name__ == "__main__":
    main()
