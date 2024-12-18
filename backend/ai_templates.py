class AIPromptTemplates:
    """
    Centralized management of AI prompt templates with customization options
    """
    @staticmethod
    def get_resume_generation_template(customization_level='professional'):
        """
        Generate resume templates with different levels of customization
        """
        templates = {
            'entry': {
                'prompt': """Create an entry-level resume that emphasizes:
                - Educational achievements
                - Internships and academic projects
                - Transferable skills
                - Potential for growth
                - Clear, concise formatting""",
                'max_tokens': 800
            },
            'professional': {
                'prompt': """Create a professional resume that highlights:
                - Comprehensive work experience
                - Quantifiable achievements
                - Industry-specific skills
                - Career progression
                - Advanced formatting and ATS optimization""",
                'max_tokens': 1200
            },
            'executive': {
                'prompt': """Develop an executive-level resume that demonstrates:
                - Strategic leadership experience
                - High-impact organizational contributions
                - Complex problem-solving skills
                - Comprehensive professional narrative
                - Executive branding and positioning""",
                'max_tokens': 1500
            }
        }
        return templates.get(customization_level, templates['professional'])

    @staticmethod
    def get_resume_optimization_template(industry='technology'):
        """
        Provide industry-specific resume optimization strategies
        """
        industry_strategies = {
            'technology': {
                'keywords': ['agile', 'scrum', 'cloud', 'machine learning', 'data analysis'],
                'focus_areas': ['technical skills', 'project impact', 'innovation']
            },
            'finance': {
                'keywords': ['risk management', 'financial modeling', 'compliance', 'portfolio'],
                'focus_areas': ['quantitative skills', 'regulatory knowledge', 'strategic planning']
            },
            'healthcare': {
                'keywords': ['patient care', 'clinical', 'compliance', 'electronic health records'],
                'focus_areas': ['certifications', 'specialized skills', 'patient outcomes']
            },
            'marketing': {
                'keywords': ['digital marketing', 'SEO', 'content strategy', 'analytics'],
                'focus_areas': ['campaign performance', 'creative solutions', 'brand development']
            }
        }
        return industry_strategies.get(industry, industry_strategies['technology'])

    @staticmethod
    def generate_custom_prompt(user_data, template_type='resume', **kwargs):
        """
        Generate a highly customized AI prompt based on user data and preferences
        """
        base_prompt = f"""
        Context: {template_type.upper()} GENERATION for {user_data.get('industry', 'general')} industry

        User Profile:
        - Name: {user_data.get('full_name', 'Not Provided')}
        - Experience Level: {user_data.get('experience_level', 'Not Specified')}
        - Key Skills: {user_data.get('skills', 'Not Provided')}

        Additional Context:
        {kwargs.get('additional_context', '')}

        Special Instructions:
        1. Maintain professional tone
        2. Use industry-specific terminology
        3. Highlight unique professional attributes
        4. Ensure ATS compatibility
        5. Focus on achievements over responsibilities

        Desired Outcome:
        Create a compelling, personalized professional document that 
        effectively communicates the user's professional value proposition.
        """
        
        # Allow for deep customization through kwargs
        for key, value in kwargs.items():
            if key.startswith('custom_'):
                base_prompt += f"\n\nCustom Instruction - {key[7:].replace('_', ' ').title()}:\n{value}"
        
        return base_prompt

class AIConfigManager:
    """
    Manage AI configuration and provide flexible prompt injection
    """
    @classmethod
    def configure_ai_generation(cls, user_data, generation_type='resume', **kwargs):
        """
        Dynamically configure AI generation with multiple customization layers
        """
        # Base template selection
        if generation_type == 'resume':
            template = AIPromptTemplates.get_resume_generation_template(
                user_data.get('customization_level', 'professional')
            )
        elif generation_type == 'optimization':
            template = AIPromptTemplates.get_resume_optimization_template(
                user_data.get('industry', 'technology')
            )
        else:
            template = {}

        # Generate custom prompt
        custom_prompt = AIPromptTemplates.generate_custom_prompt(
            user_data, 
            template_type=generation_type, 
            **kwargs
        )

        return {
            'prompt': custom_prompt,
            'max_tokens': template.get('max_tokens', 1000),
            'temperature': kwargs.get('temperature', 0.7),
            'additional_config': kwargs
        }
