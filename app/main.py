import subprocess
import threading
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
import os
#ui_path = os.path.abspath("/frontend/ui.py")
logger = get_logger(__name__)
load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Backend server failed to start: {e}")
        raise CustomException("Backend server failed to start", error_detail=e)
    
def run_frontend():
    try:
        logger.info("Starting frontend server...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Frontend server failed to start: {e}")
        raise CustomException("Frontend server failed to start", error_detail=e)

if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend)
        frontend_thread = threading.Thread(target=run_frontend)

        backend_thread.start()
        time.sleep(2)  # Ensure backend starts before frontend
        frontend_thread.start()
    except CustomException as e:
        logger.exception(f"Application failed to start: {str(e)}")
    
