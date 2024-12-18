import os
import json
import logging
import traceback
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import custom AI configuration and prompt management
from ai_templates import AIConfigManager
from prompt_manager import PromptManager
from dashboard import init_dashboard, dashboard_manager

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
except Exception as api_config_error:
    logger.error(f"API Configuration Error: {api_config_error}")
    raise

# Initialize Prompt Manager
prompt_manager = PromptManager()

# Initialize Dashboard
init_dashboard(app)

def process_advanced_settings(custom_instructions):
    """
    Process and validate advanced AI configuration settings
    
    :param custom_instructions: Dictionary of custom AI settings
    :return: Processed and validated configuration
    """
    # Default settings if not provided
    default_settings = {
        'promptContext': 'professional',
        'tone': 'professional',
        'customPrompt': '',
        'creativity': 0.7,
        'maxTokens': 1000
    }
    
    # Merge provided settings with defaults
    settings = {**default_settings, **custom_instructions} if custom_instructions else default_settings
    
    # Validate and sanitize settings
    context_mapping = {
        'entry': 'entry_level',
        'professional': 'professional',
        'executive': 'executive'
    }
    settings['promptContext'] = context_mapping.get(settings['promptContext'], 'professional')
    
    # Ensure creativity is within 0-1 range
    try:
        settings['creativity'] = max(0, min(1, float(settings['creativity'])))
    except (TypeError, ValueError):
        settings['creativity'] = 0.7
    
    # Validate max tokens
    token_options = [500, 1000, 1500, 2000]
    settings['maxTokens'] = int(settings['maxTokens']) if int(settings['maxTokens']) in token_options else 1000
    
    return settings

def generate_resume_content(user_data, **kwargs):
    """
    Advanced resume generation with flexible AI configuration and prompt management
    """
    # Process advanced settings
    advanced_settings = process_advanced_settings(kwargs.get('custom_instructions', {}))
    
    # Determine context based on experience level and advanced settings
    context_mapping = {
        'entry': 'entry_level',
        'mid': 'professional',
        'senior': 'professional',
        'executive': 'executive'
    }
    context = advanced_settings['promptContext'] or context_mapping.get(user_data.get('experience_level', 'professional'), 'professional')

    # Generate chat prompt with system instructions
    chat_prompt = prompt_manager.generate_chat_prompt(
        context=context,
        custom_instructions={
            'base_instruction': advanced_settings['customPrompt'] or 
                                f"Generate a {context} resume with a {advanced_settings['tone']} tone."
        }
    )

    # Use AIConfigManager to dynamically configure prompt
    ai_config = AIConfigManager.configure_ai_generation(
        user_data, 
        generation_type='resume',
        **kwargs
    )

    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Combine system instruction with dynamic prompt
        full_prompt = f"""{chat_prompt['system_instruction']}

Tone: {advanced_settings['tone']}
Formatting Guidelines: {chat_prompt.get('formatting_guidelines', 'Clean, professional layout')}

User Details:
- Name: {user_data.get('full_name', 'Applicant')}
- Industry: {user_data.get('industry', 'General')}
- Experience Level: {context}

{ai_config['prompt']}"""
        
        # Generate resume with dynamic configuration
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=advanced_settings['maxTokens'],
                temperature=advanced_settings['creativity']
            )
        )
        
        return response.text
    except Exception as e:
        return f"Error generating resume: {str(e)}"

def optimize_resume(existing_resume, job_description, **kwargs):
    """
    Advanced resume optimization with prompt management
    """
    # Process advanced settings
    advanced_settings = process_advanced_settings(kwargs.get('custom_instructions', {}))
    
    # Prepare user data for optimization
    user_data = kwargs.get('user_data', {})
    user_data['job_description'] = job_description

    # Create structured prompt with resume optimization examples
    structured_prompt = prompt_manager.create_structured_prompt(
        prompt_type='professional_resume',
        additional_examples=kwargs.get('additional_examples', [])
    )

    # Use AIConfigManager to dynamically configure optimization prompt
    ai_config = AIConfigManager.configure_ai_generation(
        user_data, 
        generation_type='optimization',
        existing_resume=existing_resume,
        **kwargs
    )

    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Combine structured prompt examples with dynamic optimization prompt
        full_prompt = f"""Optimize the following resume for the given job description:

Existing Resume:
{existing_resume}

Job Description:
{job_description}

Optimization Instructions:
- Tone: {advanced_settings['tone']}
- Context: {advanced_settings.get('promptContext', 'professional')}
- Custom Guidance: {advanced_settings.get('customPrompt', 'Enhance resume relevance')}

Example Optimizations:
{json.dumps(structured_prompt['examples'], indent=2)}

{ai_config['prompt']}"""
        
        # Optimize resume with dynamic configuration
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=advanced_settings['maxTokens'],
                temperature=advanced_settings['creativity']
            )
        )
        
        return response.text
    except Exception as e:
        return f"Error optimizing resume: {str(e)}"

def safe_generate_resume_content(user_data, **kwargs):
    """
    Safely generate resume content with comprehensive error handling
    """
    try:
        # Existing generation logic
        resume_content = generate_resume_content(user_data, **kwargs)
        
        # Validate generated content
        if not resume_content or len(resume_content) < 50:
            raise ValueError("Generated resume content is too short")
        
        return resume_content
    except Exception as e:
        logger.error(f"Resume Generation Error: {e}")
        logger.error(traceback.format_exc())
        return f"Error generating resume: {str(e)}"

def safe_optimize_resume(existing_resume, job_description, **kwargs):
    """
    Safely optimize resume with comprehensive error handling
    """
    try:
        # Existing optimization logic
        optimized_resume = optimize_resume(existing_resume, job_description, **kwargs)
        
        # Validate optimized content
        if not optimized_resume or len(optimized_resume) < 50:
            raise ValueError("Optimized resume content is too short")
        
        return optimized_resume
    except Exception as e:
        logger.error(f"Resume Optimization Error: {e}")
        logger.error(traceback.format_exc())
        return f"Error optimizing resume: {str(e)}"

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        user_data = request.json
        
        # Validate input
        required_fields = ['full_name', 'email', 'industry', 'experience_level']
        for field in required_fields:
            if not user_data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Optional: Allow custom prompt injection
        custom_instructions = user_data.get('custom_instructions', {})
        
        # Generate resume content with error handling
        resume_content = safe_generate_resume_content(
            user_data, 
            custom_instructions=custom_instructions
        )
        
        # Log resume generation activity
        dashboard_manager.log_resume_generation(
            user_id=user_data.get('email', 'unknown'),
            resume_details=user_data
        )
        
        return jsonify({
            "resume_content": resume_content,
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Unexpected error in resume generation: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/optimize-resume', methods=['POST'])
def optimize_resume_endpoint():
    try:
        data = request.json
        existing_resume = data.get('resume_content', '')
        job_description = data.get('job_description', '')
        
        # Validate input
        if not existing_resume:
            return jsonify({"error": "Missing resume content"}), 400
        if not job_description:
            return jsonify({"error": "Missing job description"}), 400
        
        # Optional: Allow custom prompt injection
        custom_instructions = data.get('custom_instructions', {})

        # Optimize resume with error handling
        optimized_resume = safe_optimize_resume(
            existing_resume, 
            job_description,
            user_data=data,
            custom_instructions=custom_instructions
        )
        
        # Log resume optimization activity
        dashboard_manager.log_resume_optimization(
            user_id=data.get('email', 'unknown'),
            optimization_details=data
        )
        
        return jsonify({
            "optimized_resume": optimized_resume,
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Unexpected error in resume optimization: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_global_exception(e):
    """Global error handler"""
    logger.error(f"Unhandled Exception: {e}")
    logger.error(traceback.format_exc())
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
