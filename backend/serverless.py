import os
import sys
import json
import logging
import traceback
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app as flask_app

def serverless_handler(event, context):
    """
    Netlify serverless function handler
    Converts Netlify event to Flask request
    """
    try:
        # Fix for running behind proxy
        flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)
        
        # Convert Netlify event to Flask request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Log incoming request details for debugging
        logger.info(f"Serverless Request: {http_method} {path}")
        
        # Simulate Flask request
        with flask_app.test_request_context(
            path=path, 
            method=http_method, 
            headers=headers, 
            data=body.encode('utf-8') if body else None
        ):
            response = flask_app.full_dispatch_request()
            
            return {
                'statusCode': response.status_code,
                'body': response.get_data(as_text=True),
                'headers': dict(response.headers)
            }
    except Exception as e:
        # Comprehensive error logging
        logger.error(f"Serverless Handler Error: {e}")
        logger.error(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Serverless Error',
                'details': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

# Expose handler for Netlify
handler = serverless_handler
