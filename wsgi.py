import os
from app import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)