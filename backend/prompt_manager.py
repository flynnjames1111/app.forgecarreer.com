import json
from typing import Dict, List, Any, Optional

class PromptManager:
    """
    Advanced Prompt Management System for AI-driven Resume Generation
    Inspired by Google AI Studio's Prompt Design Techniques
    """
    
    def __init__(self):
        # Predefined system instructions for different contexts
        self.system_instructions = {
            'professional': {
                'base_instruction': """You are a professional resume writer with 20+ years of experience 
                in career development and talent acquisition. Your goal is to create compelling, 
                ATS-optimized resumes that highlight professional achievements and potential.""",
                'tone': 'Formal, professional, achievement-focused',
                'formatting_guidelines': 'Use clean, modern resume formatting with clear sections'
            },
            'entry_level': {
                'base_instruction': """You are a career coach specializing in helping early-career 
                professionals create impactful resumes. Focus on potential, academic achievements, 
                and transferable skills.""",
                'tone': 'Encouraging, potential-driven, optimistic',
                'formatting_guidelines': 'Use a clean, contemporary layout that emphasizes education and potential'
            },
            'executive': {
                'base_instruction': """You are a high-level executive recruitment specialist 
                crafting strategic, leadership-oriented resumes for C-suite and senior management roles.""",
                'tone': 'Strategic, authoritative, impact-driven',
                'formatting_guidelines': 'Use a sophisticated, executive-level resume format'
            }
        }

        # Structured prompt examples for different resume types
        self.structured_prompt_examples = {
            'professional_resume': [
                {
                    'input': {
                        'name': 'Sarah Johnson',
                        'industry': 'Technology',
                        'experience_level': 'Mid-Level Software Engineer',
                        'key_skills': ['Python', 'Machine Learning', 'Data Analysis']
                    },
                    'output': """Professional Summary:
Innovative software engineer with 5+ years of experience in developing 
scalable machine learning solutions. Proven track record of improving 
system efficiency by 40% through advanced data analysis techniques.

Key Achievements:
- Developed predictive analytics model reducing operational costs by $250K annually
- Led cross-functional team in implementing AI-driven product recommendations"""
                },
                {
                    'input': {
                        'name': 'Michael Chen',
                        'industry': 'Finance',
                        'experience_level': 'Senior Financial Analyst',
                        'key_skills': ['Financial Modeling', 'Risk Management', 'Strategic Planning']
                    },
                    'output': """Professional Summary:
Strategic financial analyst with expertise in comprehensive risk management 
and financial modeling. Consistently delivers data-driven insights that 
drive organizational growth and optimize financial performance.

Key Achievements:
- Reduced investment portfolio risk by 25% through advanced predictive modeling
- Implemented cost-saving strategies resulting in $1.5M annual savings"""
                }
            ]
        }

    def generate_chat_prompt(
        self, 
        context: str = 'professional', 
        custom_instructions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Generate a chat-style prompt with system instructions and optional customizations
        
        :param context: Predefined context (professional, entry_level, executive)
        :param custom_instructions: Additional custom instructions to modify base prompt
        :return: Comprehensive prompt configuration
        """
        base_instructions = self.system_instructions.get(context, self.system_instructions['professional'])
        
        # Merge custom instructions if provided
        if custom_instructions:
            base_instructions.update(custom_instructions)
        
        return {
            'system_instruction': base_instructions['base_instruction'],
            'tone': base_instructions['tone'],
            'formatting_guidelines': base_instructions['formatting_guidelines']
        }

    def create_structured_prompt(
        self, 
        prompt_type: str = 'professional_resume', 
        additional_examples: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a structured prompt with examples for consistent output
        
        :param prompt_type: Type of structured prompt
        :param additional_examples: Optional additional examples to extend base examples
        :return: Structured prompt configuration
        """
        base_examples = self.structured_prompt_examples.get(prompt_type, [])
        
        # Extend examples if additional are provided
        if additional_examples:
            base_examples.extend(additional_examples)
        
        return {
            'prompt_type': prompt_type,
            'examples': base_examples
        }

    def tune_model_behavior(
        self, 
        task: str, 
        examples: List[Dict[str, Any]], 
        tuning_parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Simulate model fine-tuning by providing task-specific examples
        
        :param task: Specific task for model tuning
        :param examples: List of input-output example pairs
        :param tuning_parameters: Optional parameters to adjust model behavior
        :return: Tuning configuration
        """
        default_tuning_params = {
            'temperature': 0.7,  # Creativity vs. consistency
            'max_tokens': 1000,  # Output length
            'top_p': 0.9,        # Nucleus sampling
            'frequency_penalty': 0.5  # Reduce repetition
        }
        
        # Merge default and custom tuning parameters
        tuning_config = {**default_tuning_params, **(tuning_parameters or {})}
        
        return {
            'task': task,
            'examples': examples,
            'tuning_parameters': tuning_config
        }

    def export_prompt_configuration(self, prompt_config: Dict[str, Any]) -> str:
        """
        Export prompt configuration to a JSON file for persistence and sharing
        
        :param prompt_config: Prompt configuration dictionary
        :return: JSON representation of prompt configuration
        """
        return json.dumps(prompt_config, indent=2)

# Example Usage
def main():
    prompt_manager = PromptManager()
    
    # Generate a professional resume chat prompt
    professional_prompt = prompt_manager.generate_chat_prompt(
        context='professional',
        custom_instructions={
            'base_instruction': 'Focus on technology industry resumes'
        }
    )
    print("Professional Prompt:", professional_prompt)
    
    # Create a structured resume prompt
    structured_prompt = prompt_manager.create_structured_prompt(
        prompt_type='professional_resume',
        additional_examples=[{
            'input': {
                'name': 'Emily Rodriguez',
                'industry': 'Marketing',
                'experience_level': 'Digital Marketing Specialist'
            },
            'output': """Professional Summary:
Innovative digital marketing professional with a data-driven approach 
to creating impactful marketing strategies..."""
        }]
    )
    print("\nStructured Prompt:", structured_prompt)
    
    # Model behavior tuning
    tuning_config = prompt_manager.tune_model_behavior(
        task='resume_generation',
        examples=structured_prompt['examples'],
        tuning_parameters={'temperature': 0.5}
    )
    print("\nTuning Configuration:", tuning_config)

if __name__ == '__main__':
    main()
