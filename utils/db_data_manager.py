from utils.database import DatabaseManager

class DBDataManager:
    """Database-based data manager that replaces the file-based approach"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def load_documentation_links(self):
        """Load documentation links from database"""
        return self.db.get_documentation_links()
    
    def save_documentation_links(self, links):
        """This method is kept for compatibility but not used since we add links individually"""
        pass
    
    def add_documentation_link(self, title, url, description, category, rating=5):
        """Add a new documentation link"""
        return self.db.add_documentation_link(title, url, description, category, rating)
    
    def load_resources(self):
        """Load resources from database"""
        return self.db.get_resources()
    
    def save_resources(self, resources):
        """This method is kept for compatibility but not used since we add resources individually"""
        pass
    
    def add_resource(self, title, author, category, type, description, content=None, file_path=None, original_filename=None):
        """Add a new resource"""
        return self.db.add_resource(title, author, category, type, description, content, file_path, original_filename)
    
    def load_projects(self):
        """Load projects from database"""
        return self.db.get_projects()
    
    def save_projects(self, projects):
        """This method is kept for compatibility but not used since we add projects individually"""
        pass
    
    def add_project(self, title, author, category, description, technologies=None, github_url=None, 
                   demo_url=None, external_link=None, status=None, challenges=None, learnings=None, future_plans=None, 
                   image_path=None):
        """Add a new project"""
        return self.db.add_project(title, author, category, description, technologies, github_url,
                                 demo_url, external_link, status, challenges, learnings, future_plans, image_path)
    
    def load_user_data(self, user_id=None):
        """Load user data from database"""
        if user_id is None:
            from utils.auth_manager import get_current_user
            user = get_current_user()
            user_id = user['username'] if user else 'default_user'
        return self.db.get_user_data(user_id)
    
    def save_user_data(self, user_data):
        """Save user data to database"""
        self.db.update_user_data(
            bookmarks=user_data.get('bookmarks'),
            completed=user_data.get('completed'),
            todo=user_data.get('todo')
        )
    
    def add_bookmark(self, item_id, item_type=None):
        """Add item to bookmarks"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.add_bookmark(item_id, user_id)
    
    def remove_bookmark(self, item_id):
        """Remove item from bookmarks"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.remove_bookmark(item_id, user_id)
    
    def add_completed(self, item_id):
        """Add item to completed list"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.add_completed(item_id, user_id)
    
    def remove_completed(self, item_id):
        """Remove item from completed list"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.remove_completed(item_id, user_id)
    
    def add_todo(self, item_id):
        """Add item to todo list"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.add_todo(item_id, user_id)
    
    def remove_todo(self, item_id):
        """Remove item from todo list"""
        from utils.auth_manager import get_current_user
        user = get_current_user()
        user_id = user['username'] if user else 'default_user'
        self.db.remove_todo(item_id, user_id)