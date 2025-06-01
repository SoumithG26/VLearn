import hashlib
import streamlit as st
from utils.database import DatabaseManager
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        # Add User table to existing database
        User.metadata.create_all(bind=self.db.engine)
        
        # Create default admin user if not exists
        self.create_default_admin()
    
    def hash_password(self, password):
        """Hash a password for storing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
    
    def create_default_admin(self):
        """Create default admin user if not exists"""
        session = self.db.get_session()
        try:
            admin_user = session.query(User).filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@vlearn.com',
                    password_hash=self.hash_password('admin123'),
                    full_name='Administrator',
                    is_admin=True
                )
                session.add(admin_user)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating admin user: {e}")
        finally:
            session.close()
    
    def register_user(self, username, email, password, full_name=""):
        """Register a new user"""
        session = self.db.get_session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return False, "Username or email already exists"
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=self.hash_password(password),
                full_name=full_name
            )
            session.add(new_user)
            session.commit()
            
            # Create user data entry
            from utils.database import UserData
            user_data = UserData(
                user_id=username,
                bookmarks=[],
                completed=[],
                todo=[]
            )
            session.add(user_data)
            session.commit()
            
            return True, "User registered successfully"
        
        except Exception as e:
            session.rollback()
            return False, f"Registration failed: {str(e)}"
        finally:
            session.close()
    
    def authenticate_user(self, username, password):
        """Authenticate a user"""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            
            if user and self.verify_password(password, user.password_hash):
                # Update last login
                user.last_login = datetime.utcnow()
                session.commit()
                
                return True, {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_admin': user.is_admin
                }
            
            return False, "Invalid username or password"
        
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
        finally:
            session.close()
    
    def get_user_by_username(self, username):
        """Get user details by username"""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_admin': user.is_admin,
                    'created_at': user.created_at,
                    'last_login': user.last_login
                }
            return None
        finally:
            session.close()
    
    def get_all_users(self):
        """Get all users (admin only)"""
        session = self.db.get_session()
        try:
            users = session.query(User).all()
            return [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_admin': user.is_admin,
                    'created_at': user.created_at,
                    'last_login': user.last_login
                }
                for user in users
            ]
        finally:
            session.close()
    
    def update_user_profile(self, username, email=None, full_name=None):
        """Update user profile"""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                if email:
                    user.email = email
                if full_name:
                    user.full_name = full_name
                session.commit()
                return True, "Profile updated successfully"
            return False, "User not found"
        except Exception as e:
            session.rollback()
            return False, f"Update failed: {str(e)}"
        finally:
            session.close()
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and self.verify_password(old_password, user.password_hash):
                user.password_hash = self.hash_password(new_password)
                session.commit()
                return True, "Password changed successfully"
            return False, "Current password is incorrect"
        except Exception as e:
            session.rollback()
            return False, f"Password change failed: {str(e)}"
        finally:
            session.close()

def init_session_state():
    """Initialize session state for authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

def require_auth():
    """Decorator-like function to require authentication"""
    init_session_state()
    if not st.session_state.authenticated:
        return False
    return True

def get_current_user():
    """Get current logged-in user"""
    if st.session_state.authenticated and st.session_state.user:
        return st.session_state.user
    return None

def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    return user and user.get('is_admin', False)