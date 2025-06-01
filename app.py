import streamlit as st
import json
import os
from utils.db_data_manager import DBDataManager
from utils.auth_manager import require_auth, get_current_user, logout, init_session_state

# Page configuration
st.set_page_config(
    page_title="V-Learn",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
init_session_state()

# Check authentication
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

# Initialize data manager
data_manager = DBDataManager()

# Main page content
def main():
    st.title("📚 V-Learn: Learning Resources on the Go")
    st.markdown("---")
    
    # Welcome section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📖 Documentation Links")
        st.write("Access curated documentation for popular tools and technologies.")
        if st.button("Browse Documentation", use_container_width=True):
            st.switch_page("pages/1_📚_Documentation_Links.py")
    
    with col2:
        st.subheader("📁 Resource Library")
        st.write("Upload, share, and discover learning resources from the community.")
        if st.button("Explore Resources", use_container_width=True):
            st.switch_page("pages/2_📁_Resource_Library.py")
    
    with col3:
        st.subheader("🚀 Project Showcase")
        st.write("Showcase your projects and discover what others have built.")
        if st.button("View Projects", use_container_width=True):
            st.switch_page("pages/3_🚀_Project_Showcase.py")
    
    # Admin panel button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("---")
        if st.button("🔧 Admin Panel", use_container_width=True, type="secondary", key="main_admin_panel"):
            st.switch_page("pages/5_🔧_Admin_Panel.py")
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    resources = data_manager.load_resources()
    projects = data_manager.load_projects()
    user_data = data_manager.load_user_data()
    
    with col1:
        st.metric("Total Resources", len(resources))
    
    with col2:
        st.metric("Projects Showcased", len(projects))
    
    with col3:
        bookmarked = len(user_data.get("bookmarks", []))
        st.metric("Your Bookmarks", bookmarked)
    
    with col4:
        completed = len(user_data.get("completed", []))
        st.metric("Completed", completed)
    
    # Recent activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    if resources:
        st.write("**Latest Resources:**")
        recent_resources = sorted(resources, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]
        for resource in recent_resources:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• **{resource['title']}** - {resource['category']}")
                    st.caption(f"By {resource['author']} | {resource.get('description', 'No description')[:50]}...")
                with col2:
                    st.caption(resource.get('timestamp', 'Unknown date'))
    else:
        st.info("No resources uploaded yet. Be the first to share!")
    
    if projects:
        st.write("**Latest Projects:**")
        recent_projects = sorted(projects, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]
        for project in recent_projects:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• **{project['title']}** - {project['category']}")
                    st.caption(f"By {project['author']} | {project.get('description', 'No description')[:50]}...")
                with col2:
                    st.caption(project.get('timestamp', 'Unknown date'))
    else:
        st.info("No projects showcased yet. Share your work!")

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.title("V-Learn Navigation")
        
        # User info and logout
        current_user = get_current_user()
        if current_user:
            st.markdown(f"**Welcome, {current_user.get('full_name') or current_user.get('username')}!**")
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout()
        
        st.markdown("---")
        
        # Quick access to user resources
        if st.button("⭐ My Resources", use_container_width=True):
            st.switch_page("pages/4_⭐_My_Resources.py")
        
        if st.button("🔧 Admin Panel", use_container_width=True, key="sidebar_admin_panel"):
            st.switch_page("pages/5_🔧_Admin_Panel.py")
        
        st.markdown("---")
        
        # Search functionality
        st.subheader("🔍 Quick Search")
        search_term = st.text_input("Search resources/projects...")
        
        if search_term and st.button("Search", use_container_width=True):
            # Store search term in session state and navigate
            st.session_state.search_term = search_term
            st.switch_page("pages/2_📁_Resource_Library.py")
        
        st.markdown("---")
        
        # Upload shortcuts
        st.subheader("⚡ Quick Actions")
        if st.button("Upload Resource", use_container_width=True):
            st.session_state.show_upload = True
            st.switch_page("pages/2_📁_Resource_Library.py")
        
        if st.button("Share Project", use_container_width=True):
            st.session_state.show_project_upload = True
            st.switch_page("pages/3_🚀_Project_Showcase.py")

if __name__ == "__main__":
    render_sidebar()
    main()
