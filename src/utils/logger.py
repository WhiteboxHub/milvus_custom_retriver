import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Define log file paths
        self.all_logs_file = os.path.join(self.log_dir, "all_logs.log")
        self.success_logs_file = os.path.join(self.log_dir, "success_logs.log")
        self.failure_logs_file = os.path.join(self.log_dir, "failure_logs.log")
        
        # Create a custom logger
        self.logger = logging.getLogger("RAG_Logger")
        self.logger.setLevel(logging.DEBUG)
        
        self.success_logger = logging.getLogger("Success_Logger")
        self.success_logger.setLevel(logging.INFO)
        
        self.failure_logger = logging.getLogger("Failure_Logger")
        self.failure_logger.setLevel(logging.ERROR)
        
        # Define log format
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s")
        
        # Create handlers
        all_handler = logging.FileHandler(self.all_logs_file)
        success_handler = logging.FileHandler(self.success_logs_file)
        failure_handler = logging.FileHandler(self.failure_logs_file)
        
        # Set level for handlers
        all_handler.setLevel(logging.DEBUG)
        success_handler.setLevel(logging.INFO)
        failure_handler.setLevel(logging.ERROR)
        
        # Apply formatter
        all_handler.setFormatter(log_format)
        success_handler.setFormatter(log_format)
        failure_handler.setFormatter(log_format)
        
        # Add handlers to loggers
        self.logger.addHandler(all_handler)
        self.success_logger.addHandler(success_handler)
        self.success_logger.addHandler(all_handler)  # Ensure success logs also go to all_logs
        
        self.failure_logger.addHandler(failure_handler)
        self.failure_logger.addHandler(all_handler)  # Ensure failure logs also go to all_logs
    
    def log(self, message, source):
        """Log success messages."""
        log_message = f"{source} - {message}"
        self.success_logger.info(log_message)  # Log to success_logs and all_logs
    
    def error(self, message, source):
        """Log failure messages."""
        log_message = f"{source} - {message}"
        self.failure_logger.error(log_message)  # Log to failure_logs and all_logs
    
    def info(self, message, source):
        """Log debug messages."""
        self.logger.debug(f"{source} - {message}")

# # Example Usage
# if __name__ == "__main__":
#     logger = RAGLogger()
#     logger.log_success("Successfully retrieved documents", "retriever")
#     logger.log_failure("Failed to generate response", "generator")
#     logger.log_debug("Query processed successfully", "query_handler")
