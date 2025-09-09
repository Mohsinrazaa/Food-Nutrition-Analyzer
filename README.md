# Food Nutrition Analyzer 🍽️

A Streamlit application that uses OpenAI's GPT-4 Vision model to analyze food images and provide detailed nutritional information.

## Features

- 📸 Upload food images (PNG, JPG, JPEG)
- 🤖 AI-powered food identification
- 📊 Detailed nutritional analysis including:
  - Calories
  - Protein, Carbohydrates, Total Fat
  - Fiber and Sodium content
- 🎨 Clean and intuitive user interface
- ⚠️ Handles non-food images gracefully

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API Key**
   - Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Option 1**: Update `.streamlit/secrets.toml` with your actual API key
   - **Option 2**: Create a `.env` file with `OPENAI_API_KEY=your-actual-key-here`
   - **Option 3**: Set environment variable: `export OPENAI_API_KEY=your-actual-key-here`

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the App**
   - Open your browser and go to `http://localhost:8501`

## Usage

1. Upload an image of food using the sidebar
2. Wait for the AI analysis to complete
3. View the identified food name, calories, and nutritional facts
4. The app will warn you if the uploaded image doesn't contain food

## Requirements

- Python 3.8+
- OpenAI API key with GPT-4 Vision access
- Internet connection for API calls

## Notes

- This app provides estimated nutritional information based on AI analysis
- Results should be used as a general guide only
- For precise nutritional information, consult a nutritionist or food database
- The app handles various image formats and sizes automatically

## Troubleshooting

- **API Key Error**: Make sure your OpenAI API key is correctly set in `.streamlit/secrets.toml`
- **Image Upload Issues**: Ensure the image is in PNG, JPG, or JPEG format
- **Analysis Errors**: Check your internet connection and OpenAI API quota
