from app import create_app
import os
import sys

app = create_app()

# Add health check endpoint for Docker
@app.route('/health')
def health_check():
    """Health check endpoint for Docker/Kubernetes"""
    try:
        # Test basic imports
        import flask
        import nltk
        import numpy
        import sklearn
        
        # Check if Firebase is available
        firebase_status = "disabled"
        try:
            import firebase_admin
            firebase_status = "enabled"
        except ImportError:
            firebase_status = "not available"
        
        # Check if model file exists
        model_status = "not found"
        model_path = os.path.join('app', 'model', 'siamese_model.h5')
        if os.path.exists(model_path):
            model_status = "available"
        
        return {
            'status': 'healthy',
            'timestamp': os.popen('date').read().strip(),
            'version': '1.0.0',
            'firebase': firebase_status,
            'model': model_status,
            'python_version': sys.version
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': os.popen('date').read().strip()
        }, 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('embeddings', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Get configuration from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    print(f"Starting CodeScan application on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)