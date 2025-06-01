import streamlit as st
from utils.auth_manager import AuthManager, init_session_state

st.set_page_config(page_title="Login - V-Learn", page_icon="🔐", layout="centered")

auth_manager = AuthManager()
init_session_state()

def main():
    st.title("🔐 Welcome to V-Learn")
    st.markdown("Please log in to access your personalized learning dashboard")
    st.markdown("---")
    
    # Check if already authenticated
    if st.session_state.authenticated:
        st.success(f"Welcome back, {st.session_state.user['full_name'] or st.session_state.user['username']}!")
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("app.py")
        if st.button("Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
        return
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        login_form()
    
    with tab2:
        register_form()

def login_form():
    st.subheader("Login to Your Account")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)
        with col2:
            demo_button = st.form_submit_button("Demo Login", use_container_width=True, type="secondary")
        
        if login_button:
            if username and password:
                success, result = auth_manager.authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = result
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both username and password")
        
        if demo_button:
            # Demo login with admin account
            success, result = auth_manager.authenticate_user("admin", "admin123")
            if success:
                st.session_state.authenticated = True
                st.session_state.user = result
                st.success("Demo login successful!")
                st.rerun()
            else:
                st.error("Demo login failed")
    
    st.markdown("---")
    st.info("**Demo Account:** Username: `admin`, Password: `admin123`")

def register_form():
    st.subheader("Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="Choose a username")
            email = st.text_input("Email*", placeholder="your.email@example.com")
        
        with col2:
            full_name = st.text_input("Full Name", placeholder="Your full name")
            password = st.text_input("Password*", type="password", placeholder="Choose a secure password")
        
        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
        
        register_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if register_button:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = auth_manager.register_user(username, email, password, full_name)
                    if success:
                        st.success(message)
                        st.info("You can now login with your new account!")
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all required fields")

if __name__ == "__main__":
    main()