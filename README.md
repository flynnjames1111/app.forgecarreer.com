# CareerForge AI 🚀

## AI-Powered Resume Generation and Career Development Platform

### 🌟 Overview
CareerForge AI is an innovative platform that leverages artificial intelligence to help professionals create, optimize, and enhance their resumes with unprecedented precision and insight.

### 🔧 Features
- AI-Powered Resume Generation
- Resume Optimization
- Personalized Career Insights
- Advanced Prompt Configuration
- Real-time Dashboard Tracking

### 💻 Tech Stack
- Backend: Python, Flask
- AI: Google Gemini API
- Deployment: Netlify
- Frontend: HTML, CSS, JavaScript

### 🚀 Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run the application

### 🔐 Environment Setup
Create a `.env` file with:
```
GEMINI_API_KEY=your_api_key_here
```

### 📦 Dependencies
See `requirements.txt` for full list of dependencies

### 🌐 Deployment
Deployed on Netlify with serverless functions

### 🤝 Contributing
Contributions welcome! Please read our contribution guidelines.

### 📄 License
[Your License Here]

### 💡 Contact
Email: support@careerforgeai.com

## 🌟 Advanced AI Configuration Features

#### Comprehensive Prompt Management
- **Dynamic Context Selection**
  - Entry Level
  - Professional
  - Executive

- **Tone Customization**
  - Professional and Formal
  - Conversational and Friendly
  - Creative and Dynamic
  - Technical and Precise

- **Custom Prompt Injection**
  - Free-text area for specific resume generation instructions
  - Tailor AI output to unique requirements

#### AI Generation Parameters
- **Creativity Level Slider**
  - Control AI's creativity from conservative to innovative
  - Range: 0 (highly consistent) to 1 (highly creative)

- **Resume Length Control**
  - Short (500 tokens)
  - Standard (1000 tokens)
  - Detailed (1500 tokens)
  - Comprehensive (2000 tokens)

### 🔧 Technical Implementation

#### Prompt Management System
- Flexible configuration processing
- Intelligent setting validation
- Seamless integration with Gemini AI

#### Key Components
- `process_advanced_settings()`: Validate and sanitize AI configuration
- `generate_resume_content()`: Dynamic resume generation
- `optimize_resume()`: Context-aware resume optimization

### 💡 Example Use Cases

1. **Recent Graduate**
   ```python
   # Entry-level context with academic focus
   custom_instructions = {
       'promptContext': 'entry',
       'tone': 'conversational',
       'customPrompt': 'Highlight academic projects and potential'
   }
   ```

2. **Senior Professional**
   ```python
   # Professional context with technical precision
   custom_instructions = {
       'promptContext': 'professional',
       'tone': 'technical',
       'creativity': 0.5,
       'maxTokens': 1500
   }
   ```

3. **Executive Candidate**
   ```python
   # Executive context with leadership emphasis
   custom_instructions = {
       'promptContext': 'executive',
       'tone': 'professional',
       'customPrompt': 'Focus on strategic leadership and impact'
   }
   ```

### 🚀 Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Gemini API key in `.env`
4. Run the application: `python backend/app.py`

### 🤝 Contributing
We welcome contributions! Please read our contribution guidelines before submitting a pull request.

### 📄 License
This project is open-source, licensed under the MIT License.

### 🔒 Security Notes
- Never commit your `.env` file to version control
- Keep your OpenAI API key confidential
- Use environment variables for sensitive information

### 📝 Support
For issues or questions, please open a GitHub issue or contact support@careerforgeai.com
