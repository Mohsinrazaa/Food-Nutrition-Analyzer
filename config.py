"""
Configuration settings for the Food Nutrition Analyzer app.
"""

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.2

# Supported image formats
SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg']

# App Configuration
APP_TITLE = "Food Nutrition Analyzer"
APP_ICON = "🍽️"
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
