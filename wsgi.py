import os
from app import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 10000))
    # Bind to 0.0.0.0 to listen on all available interfaces
    app.run(host="0.0.0.0", port=port)