import os
import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import google.generativeai as genai

dashboard_bp = Blueprint('dashboard', __name__)

class DashboardManager:
    def __init__(self):
        self.usage_data = {
            'total_resumes': 0,
            'total_optimizations': 0,
            'user_activities': []
        }
        
    def log_resume_generation(self, user_id, resume_details):
        """Log resume generation activity"""
        activity = {
            'user_id': user_id,
            'type': 'resume_generation',
            'details': resume_details,
            'timestamp': datetime.now().isoformat()
        }
        self.usage_data['total_resumes'] += 1
        self.usage_data['user_activities'].append(activity)
        return activity
    
    def log_resume_optimization(self, user_id, optimization_details):
        """Log resume optimization activity"""
        activity = {
            'user_id': user_id,
            'type': 'resume_optimization',
            'details': optimization_details,
            'timestamp': datetime.now().isoformat()
        }
        self.usage_data['total_optimizations'] += 1
        self.usage_data['user_activities'].append(activity)
        return activity
    
    def generate_ai_insights(self, user_activities):
        """Generate AI-powered insights based on user activities"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare insights prompt
            insights_prompt = f"""Analyze the following user resume generation activities and provide personalized career development insights:

Activities Summary:
{json.dumps(user_activities, indent=2)}

Please provide:
1. Skill development recommendations
2. Career progression suggestions
3. Resume improvement insights
4. Potential career paths based on observed patterns
"""
            
            response = model.generate_content(insights_prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"

dashboard_manager = DashboardManager()

@dashboard_bp.route('/dashboard/usage-stats', methods=['GET'])
@cross_origin()
def get_usage_stats():
    """Retrieve overall usage statistics"""
    return jsonify({
        'total_resumes': dashboard_manager.usage_data['total_resumes'],
        'total_optimizations': dashboard_manager.usage_data['total_optimizations'],
        'recent_activities': dashboard_manager.usage_data['user_activities'][-5:]  # Last 5 activities
    })

@dashboard_bp.route('/dashboard/ai-insights', methods=['POST'])
@cross_origin()
def get_ai_insights():
    """Generate AI-powered career insights"""
    user_id = request.json.get('user_id')
    user_activities = [
        activity for activity in dashboard_manager.usage_data['user_activities'] 
        if activity['user_id'] == user_id
    ]
    
    insights = dashboard_manager.generate_ai_insights(user_activities)
    
    return jsonify({
        'user_id': user_id,
        'insights': insights
    })

@dashboard_bp.route('/resume/log-generation', methods=['POST'])
@cross_origin()
def log_resume_generation():
    """Log a resume generation event"""
    resume_details = request.json
    user_id = resume_details.get('user_id')
    
    activity = dashboard_manager.log_resume_generation(user_id, resume_details)
    
    return jsonify({
        'status': 'success',
        'activity': activity
    })

@dashboard_bp.route('/resume/log-optimization', methods=['POST'])
@cross_origin()
def log_resume_optimization():
    """Log a resume optimization event"""
    optimization_details = request.json
    user_id = optimization_details.get('user_id')
    
    activity = dashboard_manager.log_resume_optimization(user_id, optimization_details)
    
    return jsonify({
        'status': 'success',
        'activity': activity
    })

def init_dashboard(app):
    """Initialize dashboard blueprint"""
    app.register_blueprint(dashboard_bp)
