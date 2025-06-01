import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DocumentationLink(Base):
    __tablename__ = 'documentation_links'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(String(100))
    rating = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resource(Base):
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    category = Column(String(100))
    type = Column(String(50))  # Link, Text, Image, Video, File
    description = Column(Text)
    content = Column(Text)  # For text content or URLs
    file_path = Column(String(500))  # For uploaded files
    original_filename = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    technologies = Column(JSON)  # Store as JSON array
    github_url = Column(String(500))
    demo_url = Column(String(500))
    external_link = Column(String(500))
    status = Column(String(50))
    challenges = Column(Text)
    learnings = Column(Text)
    future_plans = Column(Text)
    image_path = Column(String(500))
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserData(Base):
    __tablename__ = 'user_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), default='default_user')  # For future multi-user support
    bookmarks = Column(JSON)  # Store as JSON array
    completed = Column(JSON)  # Store as JSON array
    todo = Column(JSON)  # Store as JSON array
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        
        # Initialize with default data if empty
        self.initialize_default_data()
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def initialize_default_data(self):
        """Initialize database with default data if empty"""
        session = self.get_session()
        try:
            # Check if documentation links exist
            if session.query(DocumentationLink).count() == 0:
                self.create_default_documentation_links(session)
            
            # Check if user data exists
            if session.query(UserData).count() == 0:
                default_user_data = UserData(
                    user_id='default_user',
                    bookmarks=[],
                    completed=[],
                    todo=[]
                )
                session.add(default_user_data)
            
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error initializing default data: {e}")
        finally:
            session.close()
    
    def create_default_documentation_links(self, session):
        """Create default documentation links"""
        default_links = [
            {
                "title": "Python Official Documentation",
                "url": "https://docs.python.org/3/",
                "description": "The official Python documentation with tutorials, library reference, and language reference.",
                "category": "Programming",
                "rating": 5
            },
            {
                "title": "Git Documentation",
                "url": "https://git-scm.com/doc",
                "description": "Official Git documentation including tutorials, reference manual, and videos.",
                "category": "Tools",
                "rating": 5
            },
            {
                "title": "Streamlit Documentation",
                "url": "https://docs.streamlit.io/",
                "description": "Complete guide to building data apps with Streamlit framework.",
                "category": "Frameworks",
                "rating": 5
            },
            {
                "title": "JavaScript MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "description": "Comprehensive JavaScript documentation and tutorials from Mozilla.",
                "category": "Programming",
                "rating": 5
            },
            {
                "title": "React Documentation",
                "url": "https://react.dev/",
                "description": "Official React documentation with interactive tutorials and examples.",
                "category": "Frameworks",
                "rating": 5
            },
            {
                "title": "Docker Documentation",
                "url": "https://docs.docker.com/",
                "description": "Complete Docker documentation covering containers, images, and deployment.",
                "category": "DevOps",
                "rating": 5
            },
            {
                "title": "VS Code Documentation",
                "url": "https://code.visualstudio.com/docs",
                "description": "Official Visual Studio Code documentation and setup guides.",
                "category": "Tools",
                "rating": 5
            },
            {
                "title": "Pandas Documentation",
                "url": "https://pandas.pydata.org/docs/",
                "description": "Official Pandas documentation for data manipulation and analysis.",
                "category": "Programming",
                "rating": 5
            },
            {
                "title": "Node.js Documentation",
                "url": "https://nodejs.org/docs/",
                "description": "Official Node.js documentation and API reference.",
                "category": "Programming",
                "rating": 5
            },
            {
                "title": "GitHub Documentation",
                "url": "https://docs.github.com/",
                "description": "Complete GitHub documentation covering repositories, actions, and collaboration.",
                "category": "Tools",
                "rating": 5
            }
        ]
        
        for link_data in default_links:
            doc_link = DocumentationLink(**link_data)
            session.add(doc_link)
    
    # Documentation Links methods
    def get_documentation_links(self):
        """Get all documentation links"""
        session = self.get_session()
        try:
            links = session.query(DocumentationLink).all()
            return [
                {
                    'id': link.id,
                    'title': link.title,
                    'url': link.url,
                    'description': link.description,
                    'category': link.category,
                    'rating': link.rating
                }
                for link in links
            ]
        finally:
            session.close()
    
    def add_documentation_link(self, title, url, description, category, rating=5):
        """Add a new documentation link"""
        session = self.get_session()
        try:
            new_link = DocumentationLink(
                title=title,
                url=url,
                description=description,
                category=category,
                rating=rating
            )
            session.add(new_link)
            session.commit()
            return new_link.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Resources methods
    def get_resources(self):
        """Get all resources"""
        session = self.get_session()
        try:
            resources = session.query(Resource).all()
            return [
                {
                    'id': resource.id,
                    'title': resource.title,
                    'author': resource.author,
                    'category': resource.category,
                    'type': resource.type,
                    'description': resource.description,
                    'content': resource.content,
                    'file_path': resource.file_path,
                    'original_filename': resource.original_filename,
                    'timestamp': str(resource.created_at) if resource.created_at else ''
                }
                for resource in resources
            ]
        finally:
            session.close()
    
    def add_resource(self, title, author, category, type, description, content=None, file_path=None, original_filename=None):
        """Add a new resource"""
        session = self.get_session()
        try:
            new_resource = Resource(
                title=title,
                author=author,
                category=category,
                type=type,
                description=description,
                content=content,
                file_path=file_path,
                original_filename=original_filename
            )
            session.add(new_resource)
            session.commit()
            return new_resource.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Projects methods
    def get_projects(self):
        """Get all projects"""
        session = self.get_session()
        try:
            projects = session.query(Project).all()
            return [
                {
                    'id': project.id,
                    'title': project.title,
                    'author': project.author,
                    'category': project.category,
                    'description': project.description,
                    'technologies': project.technologies if project.technologies is not None else [],
                    'github_url': project.github_url,
                    'demo_url': project.demo_url,
                    'external_link': project.external_link,
                    'status': project.status,
                    'challenges': project.challenges,
                    'learnings': project.learnings,
                    'future_plans': project.future_plans,
                    'image_path': project.image_path,
                    'likes': project.likes,
                    'timestamp': str(project.created_at) if project.created_at else ''
                }
                for project in projects
            ]
        finally:
            session.close()
    
    def add_project(self, title, author, category, description, technologies=None, github_url=None, 
                   demo_url=None, external_link=None, status=None, challenges=None, learnings=None, future_plans=None, 
                   image_path=None):
        """Add a new project"""
        session = self.get_session()
        try:
            new_project = Project(
                title=title,
                author=author,
                category=category,
                description=description,
                technologies=technologies or [],
                github_url=github_url,
                demo_url=demo_url,
                external_link=external_link,
                status=status,
                challenges=challenges,
                learnings=learnings,
                future_plans=future_plans,
                image_path=image_path
            )
            session.add(new_project)
            session.commit()
            return new_project.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # User Data methods
    def get_user_data(self, user_id='default_user'):
        """Get user data"""
        session = self.get_session()
        try:
            user_data = session.query(UserData).filter_by(user_id=user_id).first()
            if not user_data:
                # Create default user data
                user_data = UserData(
                    user_id=user_id,
                    bookmarks=[],
                    completed=[],
                    todo=[]
                )
                session.add(user_data)
                session.commit()
            
            return {
                'bookmarks': user_data.bookmarks if user_data.bookmarks is not None else [],
                'completed': user_data.completed if user_data.completed is not None else [],
                'todo': user_data.todo if user_data.todo is not None else []
            }
        finally:
            session.close()
    
    def update_user_data(self, bookmarks=None, completed=None, todo=None, user_id='default_user'):
        """Update user data"""
        session = self.get_session()
        try:
            user_data = session.query(UserData).filter_by(user_id=user_id).first()
            if not user_data:
                user_data = UserData(user_id=user_id)
                session.add(user_data)
            
            if bookmarks is not None:
                user_data.bookmarks = bookmarks
            if completed is not None:
                user_data.completed = completed
            if todo is not None:
                user_data.todo = todo
            
            # Updated timestamp will be handled automatically by SQLAlchemy onupdate
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def add_bookmark(self, item_id, user_id='default_user'):
        """Add item to bookmarks"""
        user_data = self.get_user_data(user_id)
        bookmarks = user_data['bookmarks']
        if item_id not in bookmarks:
            bookmarks.append(item_id)
            self.update_user_data(bookmarks=bookmarks, user_id=user_id)
    
    def remove_bookmark(self, item_id, user_id='default_user'):
        """Remove item from bookmarks"""
        user_data = self.get_user_data(user_id)
        bookmarks = user_data['bookmarks']
        if item_id in bookmarks:
            bookmarks.remove(item_id)
            self.update_user_data(bookmarks=bookmarks, user_id=user_id)
    
    def add_completed(self, item_id, user_id='default_user'):
        """Add item to completed list"""
        user_data = self.get_user_data(user_id)
        completed = user_data['completed']
        todo = user_data['todo']
        
        if item_id not in completed:
            completed.append(item_id)
        # Remove from todo if present
        if item_id in todo:
            todo.remove(item_id)
        
        self.update_user_data(completed=completed, todo=todo, user_id=user_id)
    
    def remove_completed(self, item_id, user_id='default_user'):
        """Remove item from completed list"""
        user_data = self.get_user_data(user_id)
        completed = user_data['completed']
        if item_id in completed:
            completed.remove(item_id)
            self.update_user_data(completed=completed, user_id=user_id)
    
    def add_todo(self, item_id, user_id='default_user'):
        """Add item to todo list"""
        user_data = self.get_user_data(user_id)
        todo = user_data['todo']
        if item_id not in todo:
            todo.append(item_id)
            self.update_user_data(todo=todo, user_id=user_id)
    
    def remove_todo(self, item_id, user_id='default_user'):
        """Remove item from todo list"""
        user_data = self.get_user_data(user_id)
        todo = user_data['todo']
        if item_id in todo:
            todo.remove(item_id)
            self.update_user_data(todo=todo, user_id=user_id)