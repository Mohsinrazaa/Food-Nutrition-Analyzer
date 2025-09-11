"""
Configuration settings for the Food Nutrition Analyzer app.
"""

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.2

# Supported image formats
SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg']

# App Configuration
APP_TITLE = "AI Food Intelligence Hub"
APP_ICON = "🧠"
APP_LAYOUT = "wide"

# Default nutritional values for non-food items
DEFAULT_NON_FOOD_NUTRITION = {
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

# Default values for unknown/error cases
DEFAULT_UNKNOWN_NUTRITION = {
    "food_name": "Unknown",
    "calories": 0,
    "nutritional_facts": {
        "protein": "0g",
        "carbohydrates": "0g",
        "total_fat": "0g",
        "fiber": "0g",
        "sodium": "0mg"
    }
}

# Chatbot Configuration
CHATBOT_SYSTEM_PROMPT = """You are a helpful nutrition and food analysis assistant. You can help users with:

1. Food and nutrition questions
2. Explaining nutritional information
3. Providing dietary advice and recommendations
4. Helping interpret food analysis results
5. General health and wellness tips related to food

Keep your responses:
- Accurate and evidence-based
- Helpful and encouraging
- Concise but informative
- Professional but friendly

If users ask about specific medical conditions or need medical advice, always recommend they consult with a healthcare professional or registered dietitian.

You can reference the food analysis results if they're available in the conversation context."""

CHATBOT_MAX_TOKENS = 1000
CHATBOT_TEMPERATURE = 0.7

# Advanced LLM Features
FOOD_RECOMMENDATION_SYSTEM_PROMPT = """You are an advanced AI nutritionist and food recommendation expert. You can:

1. Analyze food images and provide detailed nutritional insights
2. Suggest healthy alternatives and improvements
3. Create personalized meal plans based on dietary preferences
4. Provide cooking tips and preparation methods
5. Explain complex nutritional concepts in simple terms
6. Offer dietary advice for specific health goals

Always provide evidence-based recommendations and encourage users to consult healthcare professionals for medical advice."""

FOOD_ANALYSIS_ENHANCED_PROMPT = """You are an advanced AI food analysis system. Analyze the provided food image and return comprehensive information in this JSON format:

{
    "food_name": "<detailed dish name>",
    "calories": <integer>,
    "serving_size": "<estimated serving size>",
    "nutritional_facts": {
        "protein": "<value in g>",
        "carbohydrates": "<value in g>",
        "total_fat": "<value in g>",
        "fiber": "<value in g>",
        "sodium": "<value in mg>",
        "sugar": "<value in g>",
        "saturated_fat": "<value in g>",
        "cholesterol": "<value in mg>"
    },
    "health_benefits": ["<benefit 1>", "<benefit 2>", "<benefit 3>"],
    "dietary_tags": ["<tag1>", "<tag2>", "<tag3>"],
    "cooking_suggestions": "<brief cooking tip>",
    "health_score": <integer 1-10>,
    "allergen_warnings": ["<allergen1>", "<allergen2>"]
}

If the image is not food, return the same structure with appropriate "Not Food" values."""

# LLM Model Configuration
ANALYSIS_MODEL = "gpt-4o"  # More powerful model for analysis
CHAT_MODEL = "gpt-4o-mini"  # Efficient model for chat
RECOMMENDATION_MODEL = "gpt-4o"  # Advanced model for recommendations