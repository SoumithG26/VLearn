import json
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        self.ensure_data_files()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def ensure_data_files(self):
        """Ensure all data files exist with default content"""
        # Documentation links
        doc_file = os.path.join(self.data_dir, "documentation_links.json")
        if not os.path.exists(doc_file):
            self.save_documentation_links(self.get_default_documentation_links())
        
        # Resources
        resources_file = os.path.join(self.data_dir, "resources.json")
        if not os.path.exists(resources_file):
            self.save_resources([])
        
        # Projects
        projects_file = os.path.join(self.data_dir, "projects.json")
        if not os.path.exists(projects_file):
            self.save_projects([])
        
        # User data
        user_file = os.path.join(self.data_dir, "user_data.json")
        if not os.path.exists(user_file):
            self.save_user_data({
                "bookmarks": [],
                "completed": [],
                "todo": []
            })
    
    def get_default_documentation_links(self):
        """Return default documentation links"""
        return [
            {
                "id": 1,
                "title": "Python Official Documentation",
                "url": "https://docs.python.org/3/",
                "description": "The official Python documentation with tutorials, library reference, and language reference.",
                "category": "Programming",
                "rating": 5
            },
            {
                "id": 2,
                "title": "Git Documentation",
                "url": "https://git-scm.com/doc",
                "description": "Official Git documentation including tutorials, reference manual, and videos.",
                "category": "Tools",
                "rating": 5
            },
            {
                "id": 3,
                "title": "Streamlit Documentation",
                "url": "https://docs.streamlit.io/",
                "description": "Complete guide to building data apps with Streamlit framework.",
                "category": "Frameworks",
                "rating": 5
            },
            {
                "id": 4,
                "title": "JavaScript MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "description": "Comprehensive JavaScript documentation and tutorials from Mozilla.",
                "category": "Programming",
                "rating": 5
            },
            {
                "id": 5,
                "title": "React Documentation",
                "url": "https://react.dev/",
                "description": "Official React documentation with interactive tutorials and examples.",
                "category": "Frameworks",
                "rating": 5
            },
            {
                "id": 6,
                "title": "Docker Documentation",
                "url": "https://docs.docker.com/",
                "description": "Complete Docker documentation covering containers, images, and deployment.",
                "category": "DevOps",
                "rating": 5
            },
            {
                "id": 7,
                "title": "VS Code Documentation",
                "url": "https://code.visualstudio.com/docs",
                "description": "Official Visual Studio Code documentation and setup guides.",
                "category": "Tools",
                "rating": 5
            },
            {
                "id": 8,
                "title": "Pandas Documentation",
                "url": "https://pandas.pydata.org/docs/",
                "description": "Official Pandas documentation for data manipulation and analysis.",
                "category": "Programming",
                "rating": 5
            },
            {
                "id": 9,
                "title": "Node.js Documentation",
                "url": "https://nodejs.org/docs/",
                "description": "Official Node.js documentation and API reference.",
                "category": "Programming",
                "rating": 5
            },
            {
                "id": 10,
                "title": "GitHub Documentation",
                "url": "https://docs.github.com/",
                "description": "Complete GitHub documentation covering repositories, actions, and collaboration.",
                "category": "Tools",
                "rating": 5
            }
        ]
    
    def load_documentation_links(self):
        """Load documentation links from file"""
        try:
            with open(os.path.join(self.data_dir, "documentation_links.json"), 'r') as f:
                return json.load(f)
        except:
            return self.get_default_documentation_links()
    
    def save_documentation_links(self, links):
        """Save documentation links to file"""
        with open(os.path.join(self.data_dir, "documentation_links.json"), 'w') as f:
            json.dump(links, f, indent=2)
    
    def load_resources(self):
        """Load resources from file"""
        try:
            with open(os.path.join(self.data_dir, "resources.json"), 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_resources(self, resources):
        """Save resources to file"""
        with open(os.path.join(self.data_dir, "resources.json"), 'w') as f:
            json.dump(resources, f, indent=2)
    
    def load_projects(self):
        """Load projects from file"""
        try:
            with open(os.path.join(self.data_dir, "projects.json"), 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_projects(self, projects):
        """Save projects to file"""
        with open(os.path.join(self.data_dir, "projects.json"), 'w') as f:
            json.dump(projects, f, indent=2)
    
    def load_user_data(self):
        """Load user data from file"""
        try:
            with open(os.path.join(self.data_dir, "user_data.json"), 'r') as f:
                return json.load(f)
        except:
            return {"bookmarks": [], "completed": [], "todo": []}
    
    def save_user_data(self, user_data):
        """Save user data to file"""
        with open(os.path.join(self.data_dir, "user_data.json"), 'w') as f:
            json.dump(user_data, f, indent=2)
    
    def add_bookmark(self, item_id, item_type=None):
        """Add item to bookmarks"""
        user_data = self.load_user_data()
        if item_id not in user_data.get("bookmarks", []):
            user_data.setdefault("bookmarks", []).append(item_id)
            self.save_user_data(user_data)
    
    def remove_bookmark(self, item_id):
        """Remove item from bookmarks"""
        user_data = self.load_user_data()
        if item_id in user_data.get("bookmarks", []):
            user_data["bookmarks"].remove(item_id)
            self.save_user_data(user_data)
    
    def add_completed(self, item_id):
        """Add item to completed list"""
        user_data = self.load_user_data()
        if item_id not in user_data.get("completed", []):
            user_data.setdefault("completed", []).append(item_id)
            # Remove from todo if present
            if item_id in user_data.get("todo", []):
                user_data["todo"].remove(item_id)
            self.save_user_data(user_data)
    
    def remove_completed(self, item_id):
        """Remove item from completed list"""
        user_data = self.load_user_data()
        if item_id in user_data.get("completed", []):
            user_data["completed"].remove(item_id)
            self.save_user_data(user_data)
    
    def add_todo(self, item_id):
        """Add item to todo list"""
        user_data = self.load_user_data()
        if item_id not in user_data.get("todo", []):
            user_data.setdefault("todo", []).append(item_id)
            self.save_user_data(user_data)
    
    def remove_todo(self, item_id):
        """Remove item from todo list"""
        user_data = self.load_user_data()
        if item_id in user_data.get("todo", []):
            user_data["todo"].remove(item_id)
            self.save_user_data(user_data)
