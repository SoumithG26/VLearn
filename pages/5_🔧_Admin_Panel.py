import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db_data_manager import DBDataManager
from utils.auth_manager import require_auth, init_session_state, get_current_user, is_admin

st.set_page_config(page_title="Admin Panel", page_icon="🔧", layout="wide")

# Check authentication
init_session_state()
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

# Check admin privileges
if not is_admin():
    st.error("Access denied. This page requires administrator privileges.")
    st.stop()

data_manager = DBDataManager()

def main():
    st.title("🔧 Admin Panel")
    st.markdown("Manage V-Learn platform content and users")
    st.markdown("---")
    
    # Admin authentication (simple password protection)
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        admin_login()
        return
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "📚 Documentation Links", 
        "📁 Resources", 
        "🚀 Projects", 
        "👥 Users"
    ])
    
    with tab1:
        admin_dashboard()
    
    with tab2:
        manage_documentation_links()
    
    with tab3:
        manage_resources()
    
    with tab4:
        manage_projects()
    
    with tab5:
        manage_users()

def admin_login():
    st.subheader("🔐 Admin Login")
    st.info("This is a demo admin panel. In production, use proper authentication.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Admin Password", type="password", placeholder="Enter 'admin123'")
        
        if st.button("Login", use_container_width=True):
            if password == "admin123":  # Demo password
                st.session_state.admin_authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid password. Use 'admin123' for demo.")

def admin_dashboard():
    st.subheader("📊 Platform Overview")
    
    # Load data for statistics
    resources = data_manager.load_resources()
    projects = data_manager.load_projects()
    doc_links = data_manager.load_documentation_links()
    user_data = data_manager.load_user_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resources", len(resources))
    
    with col2:
        st.metric("Total Projects", len(projects))
    
    with col3:
        st.metric("Documentation Links", len(doc_links))
    
    with col4:
        total_interactions = len(user_data.get('bookmarks', [])) + len(user_data.get('completed', [])) + len(user_data.get('todo', []))
        st.metric("User Interactions", total_interactions)
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Recent Resources")
        if resources:
            recent_resources = sorted(resources, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
            for resource in recent_resources:
                with st.container():
                    st.write(f"**{resource['title']}** - {resource['type']}")
                    st.caption(f"By {resource['author']} | {resource.get('timestamp', 'Unknown date')}")
        else:
            st.info("No resources available")
    
    with col2:
        st.subheader("🚀 Recent Projects")
        if projects:
            recent_projects = sorted(projects, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
            for project in recent_projects:
                with st.container():
                    st.write(f"**{project['title']}** - {project['category']}")
                    st.caption(f"By {project['author']} | {project.get('timestamp', 'Unknown date')}")
        else:
            st.info("No projects available")

def manage_documentation_links():
    st.subheader("📚 Manage Documentation Links")
    
    # Display current links
    doc_links = data_manager.load_documentation_links()
    
    if doc_links:
        st.write(f"**Total Links: {len(doc_links)}**")
        
        # Convert to DataFrame for better display
        df = pd.DataFrame(doc_links)
        df = df[['id', 'title', 'category', 'rating', 'url']]
        
        # Display with edit options
        for idx, link in enumerate(doc_links):
            with st.expander(f"{link['title']} ({link['category']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**URL:** {link['url']}")
                    st.write(f"**Description:** {link['description']}")
                    st.write(f"**Rating:** {link['rating']}/5")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_doc_{link['id']}"):
                        # In a real app, you'd implement delete functionality
                        st.warning("Delete functionality would be implemented here")
    else:
        st.info("No documentation links found")
    
    # Add new link section
    st.markdown("---")
    st.subheader("➕ Add New Documentation Link")
    
    with st.form("add_doc_link_admin"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title*")
            url = st.text_input("URL*")
            category = st.selectbox("Category", ["Programming", "Tools", "Frameworks", "Databases", "DevOps", "Design", "Other"])
        
        with col2:
            description = st.text_area("Description*")
            rating = st.slider("Rating", 1, 5, 5)
        
        if st.form_submit_button("Add Documentation Link"):
            if title and url and description:
                data_manager.add_documentation_link(title, url, description, category, rating)
                st.success("Documentation link added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

def manage_resources():
    st.subheader("📁 Manage Resources")
    
    resources = data_manager.load_resources()
    
    if resources:
        st.write(f"**Total Resources: {len(resources)}**")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = list(set([r['category'] for r in resources]))
            filter_category = st.selectbox("Filter by Category", ["All"] + categories)
        
        with col2:
            types = list(set([r['type'] for r in resources]))
            filter_type = st.selectbox("Filter by Type", ["All"] + types)
        
        with col3:
            authors = list(set([r['author'] for r in resources]))
            filter_author = st.selectbox("Filter by Author", ["All"] + authors)
        
        # Apply filters
        filtered_resources = resources
        if filter_category != "All":
            filtered_resources = [r for r in filtered_resources if r['category'] == filter_category]
        if filter_type != "All":
            filtered_resources = [r for r in filtered_resources if r['type'] == filter_type]
        if filter_author != "All":
            filtered_resources = [r for r in filtered_resources if r['author'] == filter_author]
        
        st.write(f"**Showing {len(filtered_resources)} resources**")
        
        # Display resources
        for resource in filtered_resources:
            with st.expander(f"{resource['title']} - {resource['type']} ({resource['category']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Author:** {resource['author']}")
                    st.write(f"**Description:** {resource.get('description', 'No description')}")
                    st.write(f"**Created:** {resource.get('timestamp', 'Unknown')}")
                    
                    if resource.get('content'):
                        st.write(f"**Content:** {resource['content'][:100]}...")
                    
                    if resource.get('file_path'):
                        st.write(f"**File:** {resource.get('original_filename', 'Unknown file')}")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_res_{resource['id']}"):
                        st.warning("Delete functionality would be implemented here")
                    
                    if st.button("✏️ Edit", key=f"edit_res_{resource['id']}"):
                        st.info("Edit functionality would be implemented here")
    else:
        st.info("No resources found")

def manage_projects():
    st.subheader("🚀 Manage Projects")
    
    projects = data_manager.load_projects()
    
    if projects:
        st.write(f"**Total Projects: {len(projects)}**")
        
        # Display projects
        for project in projects:
            with st.expander(f"{project['title']} - {project['category']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Author:** {project['author']}")
                    st.write(f"**Description:** {project.get('description', 'No description')}")
                    st.write(f"**Status:** {project.get('status', 'Unknown')}")
                    st.write(f"**Technologies:** {', '.join(project.get('technologies', []))}")
                    
                    if project.get('github_url'):
                        st.write(f"**GitHub:** {project['github_url']}")
                    
                    if project.get('demo_url'):
                        st.write(f"**Demo:** {project['demo_url']}")
                    
                    st.write(f"**Created:** {project.get('timestamp', 'Unknown')}")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_proj_{project['id']}"):
                        st.warning("Delete functionality would be implemented here")
                    
                    if st.button("✏️ Edit", key=f"edit_proj_{project['id']}"):
                        st.info("Edit functionality would be implemented here")
    else:
        st.info("No projects found")

def manage_users():
    st.subheader("👥 User Management")
    
    user_data = data_manager.load_user_data()
    
    # User statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Bookmarked Items", len(user_data.get('bookmarks', [])))
    
    with col2:
        st.metric("Completed Items", len(user_data.get('completed', [])))
    
    with col3:
        st.metric("Todo Items", len(user_data.get('todo', [])))
    
    # User activity details
    st.markdown("---")
    st.subheader("User Activity Details")
    
    if user_data.get('bookmarks'):
        st.write("**Bookmarked Items:**")
        st.write(user_data['bookmarks'])
    
    if user_data.get('completed'):
        st.write("**Completed Items:**")
        st.write(user_data['completed'])
    
    if user_data.get('todo'):
        st.write("**Todo Items:**")
        st.write(user_data['todo'])
    
    # Reset user data option
    st.markdown("---")
    st.subheader("⚠️ Admin Actions")
    
    if st.button("🔄 Reset User Data", type="secondary"):
        if st.button("Confirm Reset", type="primary"):
            # Reset user data
            data_manager.save_user_data({
                "bookmarks": [],
                "completed": [],
                "todo": []
            })
            st.success("User data reset successfully!")
            st.rerun()

if __name__ == "__main__":
    main()