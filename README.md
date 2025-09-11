# 🧠 AI Food Intelligence Hub

https://food-nutrition-analyzergit-rhbqqhw75aesdxpqu4osth.streamlit.app/

An advanced AI-powered food analysis platform that combines multiple OpenAI models to provide comprehensive nutritional insights, personalized recommendations, and intelligent health guidance.

## 🚀 Features

### 📸 Smart Analysis
- **Enhanced AI Analysis**: Uses GPT-4o for superior food identification and nutritional analysis
- **Comprehensive Data**: Extended nutritional facts including sugar, saturated fat, cholesterol
- **Health Scoring**: AI-generated health scores (1-10) for each food item
- **Dietary Tags**: Automatic categorization (vegetarian, gluten-free, etc.)
- **Health Benefits**: AI-identified health benefits of analyzed foods
- **Cooking Tips**: Personalized cooking suggestions
- **Allergen Warnings**: Automatic allergen detection and warnings

### 🤖 AI Nutritionist Chat
- **Advanced Chatbot**: Powered by GPT-4o-mini for efficient, intelligent conversations
- **Context Awareness**: References your food analysis results in conversations
- **Quick Actions**: Pre-built buttons for common nutrition questions
- **Chat Export**: Download your conversation history
- **Expert Guidance**: Professional nutrition advice and meal planning

### 💡 AI-Powered Recommendations
- **Personalized Suggestions**: Custom recommendations based on your food analysis
- **Dietary Preferences**: Input your goals, restrictions, and preferences
- **Healthy Alternatives**: AI-suggested healthier food options
- **Cooking Improvements**: Tips to make your meals more nutritious

### 📊 Health Insights & Analytics
- **Health Score Analysis**: Visual breakdown of food health scores
- **Nutritional Breakdown**: Detailed macronutrient and micronutrient analysis
- **Health Education**: Expandable sections explaining nutrition concepts
- **Dietary Profile**: Comprehensive dietary categorization

## 🛠️ Technical Features

- **Multi-Model Architecture**: Different OpenAI models optimized for specific tasks
- **Enhanced UI**: Modern tabbed interface with intuitive navigation
- **Session Management**: Persistent chat history and analysis results
- **Error Handling**: Robust error handling and user feedback
- **Responsive Design**: Works seamlessly on desktop and mobile devices

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

## 🎯 Usage

### Smart Analysis Tab
1. Upload a food image using the sidebar
2. Wait for the enhanced AI analysis to complete
3. View comprehensive nutritional data, health scores, and dietary information
4. Explore health benefits, cooking tips, and allergen warnings

### AI Nutritionist Chat Tab
1. Ask questions about nutrition, food, or your analysis results
2. Use quick action buttons for common topics
3. Get personalized advice based on your food analysis
4. Export your chat history for future reference

### Recommendations Tab
1. Input your dietary goals and preferences
2. Get AI-powered personalized recommendations
3. Discover healthier alternatives and cooking tips
4. Access general nutrition guidelines

### Health Insights Tab
1. View detailed health score analysis
2. Explore nutritional breakdowns and dietary profiles
3. Learn about nutrition concepts and health scoring
4. Track your nutritional patterns

## 📋 Requirements

- Python 3.8+
- OpenAI API key with GPT-4o and GPT-4o-mini access
- Internet connection for API calls
- Modern web browser (Chrome, Firefox, Safari, Edge)

## ⚠️ Important Notes

- **AI-Powered Analysis**: All nutritional information is AI-generated and should be used as a general guide
- **Professional Advice**: For medical conditions or specific dietary needs, consult healthcare professionals
- **Accuracy**: Results are estimates based on visual analysis and may vary from actual nutritional content
- **Privacy**: Images are processed by OpenAI and not stored locally
- **Cost**: API usage may incur costs based on your OpenAI plan

## 🔧 Advanced Configuration

The app uses different OpenAI models for different tasks:
- **GPT-4o**: Enhanced food analysis and recommendations
- **GPT-4o-mini**: Efficient chatbot conversations
- **Custom Prompts**: Specialized prompts for nutrition expertise

## Troubleshooting

- **API Key Error**: Make sure your OpenAI API key is correctly set in `.streamlit/secrets.toml`
- **Image Upload Issues**: Ensure the image is in PNG, JPG, or JPEG format
- **Analysis Errors**: Check your internet connection and OpenAI API quota
