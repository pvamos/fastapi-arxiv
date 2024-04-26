# main.py

import uvicorn
from app.main import app, configure_logging

if __name__ == "__main__":
    configure_logging()  # Ensure that logging is configured
    uvicorn.run(app, host="0.0.0.0", port=8000)

