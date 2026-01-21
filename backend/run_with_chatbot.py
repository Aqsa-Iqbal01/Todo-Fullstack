#!/usr/bin/env python
"""Script to run the backend with chatbot enabled"""

import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003, reload=False)