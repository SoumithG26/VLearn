import os
import base64
from datetime import datetime

class FileHandler:
    def __init__(self):
        self.upload_dir = "uploads"
        self.ensure_upload_directory()
    
    def ensure_upload_directory(self):
        """Ensure the uploads directory exists"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    def save_uploaded_file(self, uploaded_file, resource_id, prefix="resource_"):
        """Save uploaded file and return the file path"""
        try:
            # Create filename with timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}{resource_id}_{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(self.upload_dir, filename)
            
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return file_path
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def get_file_as_base64(self, file_path):
        """Convert file to base64 string for embedding"""
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            print(f"Error converting file to base64: {e}")
            return None
    
    def delete_file(self, file_path):
        """Delete a file if it exists"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_file_info(self, file_path):
        """Get file information"""
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "exists": True
                }
            return {"exists": False}
        except Exception as e:
            print(f"Error getting file info: {e}")
            return {"exists": False}
