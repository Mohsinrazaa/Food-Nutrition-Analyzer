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
    DEFAULT_UNKNOWN_NUTRITION,
    CHATBOT_SYSTEM_PROMPT,
    CHATBOT_MAX_TOKENS,
    CHATBOT_TEMPERATURE,
    FOOD_RECOMMENDATION_SYSTEM_PROMPT,
    FOOD_ANALYSIS_ENHANCED_PROMPT,
    ANALYSIS_MODEL,
    CHAT_MODEL,
    RECOMMENDATION_MODEL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_openai_client():
    """Get OpenAI client with proper API key handling"""
    try:
        
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
           
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
        
        client = get_openai_client()
        if not client:
            return DEFAULT_UNKNOWN_NUTRITION
        
        
        img_bytes = file_obj.read()
        
        
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        
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

def get_chatbot_response(user_message, chat_history=None, analysis_result=None):
    """
    Generate a chatbot response using OpenAI's API.
    """
    try:
        client = get_openai_client()
        if not client:
            return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
        
        
        messages = [{"role": "system", "content": CHATBOT_SYSTEM_PROMPT}]
        
        
        if analysis_result and analysis_result.get("food_name") not in ["Not Food", "Unknown"]:
            context = f"Current food analysis result: {analysis_result['food_name']} with {analysis_result['calories']} calories. Nutritional facts: {analysis_result['nutritional_facts']}"
            messages.append({"role": "assistant", "content": f"I can see you've analyzed {analysis_result['food_name']}. How can I help you with this food or any other nutrition questions?"})
        
        
        if chat_history:
            for message in chat_history[-10:]:  # Keep last 10 messages for context
                messages.append(message)
        
        
        messages.append({"role": "user", "content": user_message})
        
        
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=CHATBOT_TEMPERATURE,
            max_tokens=CHATBOT_MAX_TOKENS
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error in get_chatbot_response: {e}")
        return "I'm sorry, I encountered an error while processing your message. Please try again."

def render_chatbot_interface():
    """
    Render the enhanced AI nutritionist chatbot interface.
    """
    st.header("🤖 AI Nutritionist Chat")
    st.markdown("**Chat with our advanced AI nutritionist for expert advice, meal planning, and personalized guidance!**")
    
    # Quick action buttons
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍎 Ask About Fruits", use_container_width=True):
            st.session_state.quick_question = "Tell me about the health benefits of different fruits and which ones I should include in my diet."
    
    with col2:
        if st.button("💪 Protein Sources", use_container_width=True):
            st.session_state.quick_question = "What are the best protein sources for a healthy diet and how much protein should I eat daily?"
    
    with col3:
        if st.button("🥗 Meal Planning", use_container_width=True):
            st.session_state.quick_question = "Help me create a balanced meal plan for the week with healthy breakfast, lunch, and dinner options."
    
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    
    if 'quick_question' in st.session_state:
        prompt = st.session_state.quick_question
        del st.session_state.quick_question
        
        
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        
        with st.chat_message("user"):
            st.write(prompt)
        
        
        analysis_result = st.session_state.get('enhanced_analysis_result', None)
        
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 AI Nutritionist is thinking..."):
                response = get_chatbot_response(prompt, st.session_state.chat_history, analysis_result)
                st.write(response)
        
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    
    if prompt := st.chat_input("Ask me about nutrition, food, or your analysis results..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        
        analysis_result = st.session_state.get('enhanced_analysis_result', None)
        
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 AI Nutritionist is thinking..."):
                response = get_chatbot_response(prompt, st.session_state.chat_history, analysis_result)
                st.write(response)
        
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("📋 Export Chat", use_container_width=True):
            if st.session_state.chat_history:
                chat_text = "\n\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in st.session_state.chat_history])
                st.download_button(
                    label="Download Chat History",
                    data=chat_text,
                    file_name="nutrition_chat_history.txt",
                    mime="text/plain"
                )
    
    with col3:
        if st.button("💡 Get Tips", use_container_width=True):
            st.session_state.quick_question = "Give me 5 practical nutrition tips for improving my daily diet and overall health."
    
    # Show context information
    if hasattr(st.session_state, 'enhanced_analysis_result'):
        result = st.session_state.enhanced_analysis_result
        if result.get("food_name") not in ["Not Food", "Unknown"]:
            st.info(f"💡 **Context Available**: I can see you've analyzed {result['food_name']}. Feel free to ask me specific questions about this food or any other nutrition topics!")

def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT
    )
    
    st.title("🧠 AI Food Intelligence Hub")
    st.markdown("**Advanced AI-powered food analysis, nutrition insights, and personalized recommendations!**")
    st.markdown("Upload food images for comprehensive analysis or chat with our AI nutritionist for expert advice.")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Smart Analysis", "🤖 AI Nutritionist", "💡 Recommendations", "📊 Health Insights"])
    
    with tab1:
        render_enhanced_food_analysis_interface()
    
    with tab2:
        render_chatbot_interface()
    
    with tab3:
        render_recommendations_interface()
    
    with tab4:
        render_health_insights_interface()

def analyze_food_image_enhanced(file_obj):
    """
    Enhanced food analysis using advanced LLM with comprehensive nutritional data.
    """
    try:
        client = get_openai_client()
        if not client:
            return DEFAULT_UNKNOWN_NUTRITION
        
        img_bytes = file_obj.read()
        
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        response = client.chat.completions.create(
            model=ANALYSIS_MODEL,
            messages=[
                {"role": "system", "content": FOOD_ANALYSIS_ENHANCED_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this food image and provide comprehensive nutritional information."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=1000
        )
    except Exception as e:
        logger.error(f"Error in analyze_food_image_enhanced: {e}")
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

def get_food_recommendations(analysis_result, user_preferences=""):
    """
    Get personalized food recommendations based on analysis results.
    """
    try:
        client = get_openai_client()
        if not client:
            return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
        
        context = f"Food analyzed: {analysis_result.get('food_name', 'Unknown')} with {analysis_result.get('calories', 0)} calories. "
        context += f"Nutritional facts: {analysis_result.get('nutritional_facts', {})}. "
        context += f"Health score: {analysis_result.get('health_score', 'N/A')}. "
        context += f"User preferences: {user_preferences if user_preferences else 'No specific preferences mentioned'}"
        
        messages = [
            {"role": "system", "content": FOOD_RECOMMENDATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Based on this food analysis: {context}. Please provide personalized recommendations for healthier alternatives, cooking tips, and dietary improvements."}
        ]
        
        response = client.chat.completions.create(
            model=RECOMMENDATION_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error in get_food_recommendations: {e}")
        return "I'm sorry, I encountered an error while generating recommendations. Please try again."

def render_enhanced_food_analysis_interface():
    """
    Render the enhanced food analysis interface with advanced LLM features.
    """
    
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
        
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-openai-api-key-here":
            st.success(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")
        else:
            st.error("❌ API key not found or not configured")
    
    with st.sidebar:
        st.header("📸 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=SUPPORTED_IMAGE_FORMATS,
            help="Upload an image of food to analyze its nutritional content"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🧠 Smart Analysis Results")
        
        if uploaded_file is not None:
            with st.spinner("🤖 AI is analyzing your food image..."):
                try:
                    uploaded_file.seek(0)
                    result = analyze_food_image_enhanced(uploaded_file)
                    
                    st.session_state.enhanced_analysis_result = result
                    
                    if result["food_name"] == "Not Food":
                        st.warning("⚠️ The uploaded image doesn't appear to contain food.")
                    elif result["food_name"] == "Unknown":
                        st.error("❌ Unable to analyze the image. Please try a clearer image.")
                    else:
                        st.success(f"✅ Successfully analyzed: **{result['food_name']}**")

                    col1a, col1b = st.columns(2)
                    with col1a:
                        st.metric("Food Name", result["food_name"])
                        st.metric("Serving Size", result.get("serving_size", "N/A"))
                    with col1b:
                        st.metric("Calories", f"{result['calories']} kcal")
                        health_score = result.get("health_score", 0)
                        if health_score > 0:
                            st.metric("Health Score", f"{health_score}/10", delta=f"{health_score-5}" if health_score != 5 else None)
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing image: {str(e)}")
                    logger.error(f"Error in analyze_food_image_enhanced: {e}")
                    st.session_state.enhanced_analysis_result = DEFAULT_UNKNOWN_NUTRITION
        else:
            st.info("👆 Please upload an image to get started!")
    
    with col2:
        st.header("📊 Enhanced Nutritional Facts")
        
        if uploaded_file is not None and hasattr(st.session_state, 'enhanced_analysis_result'):
            result = st.session_state.enhanced_analysis_result
            if result["food_name"] not in ["Not Food", "Unknown"]:
                nutrition = result["nutritional_facts"]
                
                st.markdown("### Macronutrients")
                col2a, col2b = st.columns(2)
                
                with col2a:
                    st.metric("Protein", nutrition.get("protein", "N/A"))
                    st.metric("Carbohydrates", nutrition.get("carbohydrates", "N/A"))
                    st.metric("Sugar", nutrition.get("sugar", "N/A"))
                
                with col2b:
                    st.metric("Total Fat", nutrition.get("total_fat", "N/A"))
                    st.metric("Saturated Fat", nutrition.get("saturated_fat", "N/A"))
                    st.metric("Fiber", nutrition.get("fiber", "N/A"))
                
                st.metric("Sodium", nutrition.get("sodium", "N/A"))
                st.metric("Cholesterol", nutrition.get("cholesterol", "N/A"))
                
                if result.get("health_benefits"):
                    st.markdown("### 🌟 Health Benefits")
                    for benefit in result["health_benefits"]:
                        st.write(f"• {benefit}")
                
                if result.get("dietary_tags"):
                    st.markdown("### 🏷️ Dietary Tags")
                    tags = " ".join([f"`{tag}`" for tag in result["dietary_tags"]])
                    st.markdown(tags)
                
                if result.get("cooking_suggestions"):
                    st.markdown("### 👨‍🍳 Cooking Tip")
                    st.info(f"💡 {result['cooking_suggestions']}")
                
                if result.get("allergen_warnings"):
                    st.markdown("### ⚠️ Allergen Warnings")
                    for allergen in result["allergen_warnings"]:
                        st.warning(f"⚠️ Contains: {allergen}")
                
                st.markdown("### ℹ️ Additional Information")
                st.info("💡 This enhanced analysis is powered by advanced AI and should be used as a general guide. For precise nutritional information, consult a nutritionist or food database.")
            else:
                st.warning("No nutritional information available for non-food items.")
        else:
            st.info("Upload an image to see enhanced nutritional facts here!")
    
    st.markdown("---")
    st.markdown(
        "**Note:** This enhanced analysis uses advanced AI models to provide comprehensive nutritional insights. "
        "Results are estimates and should not replace professional nutritional advice."
    )

def render_recommendations_interface():
    """
    Render the AI-powered recommendations interface.
    """
    st.header("💡 AI-Powered Recommendations")
    st.markdown("Get personalized food recommendations and dietary advice based on your analysis results!")
    
    if hasattr(st.session_state, 'enhanced_analysis_result'):
        result = st.session_state.enhanced_analysis_result
        if result.get("food_name") not in ["Not Food", "Unknown"]:
            st.success(f"✅ Found analysis results for: **{result['food_name']}**")
            
            st.subheader("🎯 Your Preferences")
            user_preferences = st.text_area(
                "Tell us about your dietary goals, restrictions, or preferences:",
                placeholder="e.g., I want to lose weight, I'm vegetarian, I have diabetes, I want to build muscle...",
                height=100
            )
            
            if st.button("🤖 Get AI Recommendations", type="primary"):
                with st.spinner("🧠 AI is generating personalized recommendations..."):
                    recommendations = get_food_recommendations(result, user_preferences)
                    st.markdown("### 🎯 Your Personalized Recommendations")
                    st.write(recommendations)
        else:
            st.warning("⚠️ Please analyze a food image first to get personalized recommendations.")
    else:
        st.info("👆 Please analyze a food image in the 'Smart Analysis' tab first to get personalized recommendations!")
    
    st.markdown("---")
    st.subheader("💡 General Nutrition Tips")
    st.info("""
    **Healthy Eating Guidelines:**
    - Aim for 5-7 servings of fruits and vegetables daily
    - Choose whole grains over refined grains
    - Include lean proteins in every meal
    - Stay hydrated with 8-10 glasses of water daily
    - Limit processed foods and added sugars
    - Practice portion control
    """)

def render_health_insights_interface():
    """
    Render the health insights and analytics interface.
    """
    st.header("📊 Health Insights & Analytics")
    st.markdown("Track your nutritional patterns and get insights about your eating habits!")
    
    if hasattr(st.session_state, 'enhanced_analysis_result'):
        result = st.session_state.enhanced_analysis_result
        if result.get("food_name") not in ["Not Food", "Unknown"]:
            st.success(f"📈 Analyzing insights for: **{result['food_name']}**")
            
            health_score = result.get("health_score", 0)
            if health_score > 0:
                st.subheader("🏆 Health Score Analysis")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Health Score", f"{health_score}/10")
                
                with col2:
                    if health_score >= 8:
                        st.success("🟢 Excellent!")
                    elif health_score >= 6:
                        st.warning("🟡 Good")
                    else:
                        st.error("🔴 Needs Improvement")
                
                with col3:
                    st.metric("Improvement Needed", f"{10-health_score} points")
            
            st.subheader("📊 Nutritional Breakdown")
            nutrition = result.get("nutritional_facts", {})
            
            if nutrition:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Macronutrients**")
                    macronutrients = {
                        "Protein": nutrition.get("protein", "0g"),
                        "Carbs": nutrition.get("carbohydrates", "0g"),
                        "Fat": nutrition.get("total_fat", "0g")
                    }
                    for nutrient, value in macronutrients.items():
                        st.write(f"• {nutrient}: {value}")
                
                with col2:
                    st.markdown("**Micronutrients**")
                    micronutrients = {
                        "Fiber": nutrition.get("fiber", "0g"),
                        "Sodium": nutrition.get("sodium", "0mg"),
                        "Sugar": nutrition.get("sugar", "0g")
                    }
                    for nutrient, value in micronutrients.items():
                        st.write(f"• {nutrient}: {value}")
            
            if result.get("health_benefits"):
                st.subheader("🌟 Health Benefits")
                for i, benefit in enumerate(result["health_benefits"], 1):
                    st.write(f"{i}. {benefit}")
            
            if result.get("dietary_tags"):
                st.subheader("🏷️ Dietary Profile")
                tags = result["dietary_tags"]
                for tag in tags:
                    st.write(f"• {tag}")
        else:
            st.warning("⚠️ Please analyze a food image first to see health insights.")
    else:
        st.info("👆 Please analyze a food image in the 'Smart Analysis' tab first to see health insights!")
    
    st.markdown("---")
    st.subheader("📚 Health Education")
    
    with st.expander("🔍 Understanding Health Scores"):
        st.write("""
        **Health Score Scale (1-10):**
        - **8-10**: Excellent nutritional value, highly recommended
        - **6-7**: Good nutritional value with some room for improvement
        - **4-5**: Moderate nutritional value, consider healthier alternatives
        - **1-3**: Poor nutritional value, limit consumption
        
        *Scores are based on nutrient density, processing level, and overall health impact.*
        """)
    
    with st.expander("📖 Reading Nutrition Labels"):
        st.write("""
        **Key Nutrients to Watch:**
        - **Protein**: Essential for muscle and tissue repair
        - **Fiber**: Aids digestion and helps control blood sugar
        - **Sodium**: High levels can increase blood pressure
        - **Sugar**: Added sugars provide empty calories
        - **Saturated Fat**: Can increase cholesterol levels
        """)

if __name__ == "__main__":
    main()
