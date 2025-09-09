"""
Demo script showing how to use the food analyzer functions programmatically.
"""

import json
from config import DEFAULT_NON_FOOD_NUTRITION, DEFAULT_UNKNOWN_NUTRITION

def demo_nutrition_analysis():
    """Demonstrate the nutrition analysis structure."""
    print("🍽️ Food Nutrition Analyzer Demo")
    print("=" * 40)
    
    print("\n📊 Example Analysis Results:")
    print("-" * 30)
    
    # Example 1: Food analysis
    food_example = {
        "food_name": "Grilled Chicken Salad",
        "calories": 320,
        "nutritional_facts": {
            "protein": "28g",
            "carbohydrates": "12g",
            "total_fat": "18g",
            "fiber": "4g",
            "sodium": "450mg"
        }
    }
    
    print("✅ Food Analysis Example:")
    print(json.dumps(food_example, indent=2))
    
    # Example 2: Non-food analysis
    print("\n⚠️  Non-Food Analysis Example:")
    print(json.dumps(DEFAULT_NON_FOOD_NUTRITION, indent=2))
    
    # Example 3: Unknown/Error analysis
    print("\n❓ Unknown/Error Analysis Example:")
    print(json.dumps(DEFAULT_UNKNOWN_NUTRITION, indent=2))
    
    print("\n💡 Usage Tips:")
    print("- Upload clear, well-lit food images for best results")
    print("- The AI can identify various cuisines and food types")
    print("- Nutritional values are estimates based on visual analysis")
    print("- Results may vary depending on image quality and food visibility")

if __name__ == "__main__":
    demo_nutrition_analysis()
