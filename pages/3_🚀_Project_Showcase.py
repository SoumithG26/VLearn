import streamlit as st
import json
from datetime import datetime
from utils.db_data_manager import DBDataManager
from utils.file_handler import FileHandler
from utils.auth_manager import require_auth, init_session_state, get_current_user

st.set_page_config(page_title="Project Showcase", page_icon="🚀", layout="wide")

# Check authentication
init_session_state()
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

data_manager = DBDataManager()
file_handler = FileHandler()

def main():
    st.title("🚀 Project Showcase")
    st.markdown("Showcase your projects and discover what others have built")
    st.markdown("---")
    
    # Tabs
    tab1, tab2 = st.tabs(["🔍 Browse Projects", "📤 Share Project"])
    
    with tab1:
        browse_projects()
    
    with tab2:
        upload_project()

def browse_projects():
    projects = data_manager.load_projects()
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search projects...", placeholder="Title, description, or author")
    
    with col2:
        categories = list(set([project['category'] for project in projects])) if projects else []
        selected_category = st.selectbox("Category", ["All"] + categories)
    
    with col3:
        tech_stacks = []
        for project in projects:
            tech_stacks.extend(project.get('technologies', []))
        unique_techs = list(set(tech_stacks))
        selected_tech = st.selectbox("Technology", ["All"] + unique_techs)
    
    # Filter projects
    filtered_projects = projects
    
    if search_term:
        filtered_projects = [
            project for project in filtered_projects
            if search_term.lower() in project['title'].lower()
            or search_term.lower() in project.get('description', '').lower()
            or search_term.lower() in project['author'].lower()
        ]
    
    if selected_category != "All":
        filtered_projects = [p for p in filtered_projects if p['category'] == selected_category]
    
    if selected_tech != "All":
        filtered_projects = [p for p in filtered_projects if selected_tech in p.get('technologies', [])]
    
    # Sort options
    sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title A-Z"])
    
    if sort_option == "Newest First":
        filtered_projects.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    elif sort_option == "Oldest First":
        filtered_projects.sort(key=lambda x: x.get('timestamp', ''))
    elif sort_option == "Title A-Z":
        filtered_projects.sort(key=lambda x: x['title'])
    
    st.markdown("---")
    
    # Display projects
    if filtered_projects:
        st.write(f"Found {len(filtered_projects)} projects")
        
        # Display in grid layout
        cols = st.columns(2)
        
        for idx, project in enumerate(filtered_projects):
            with cols[idx % 2]:
                with st.container():
                    # Project header
                    st.subheader(project['title'])
                    st.write(f"**By:** {project['author']}")
                    
                    # Project image/screenshot
                    if project.get('image_path'):
                        try:
                            st.image(project['image_path'], use_container_width=True)
                        except:
                            st.info("📷 Image not available")
                    else:
                        st.info("📷 No preview image")
                    
                    # Description
                    st.write(project.get('description', 'No description available'))
                    
                    # Technologies used
                    if project.get('technologies'):
                        st.write("**Technologies:**")
                        tech_cols = st.columns(min(len(project['technologies']), 4))
                        for i, tech in enumerate(project['technologies'][:4]):
                            with tech_cols[i]:
                                st.caption(f"🔧 {tech}")
                        if len(project['technologies']) > 4:
                            st.caption(f"... and {len(project['technologies']) - 4} more")
                    
                    # Project details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"📂 {project['category']}")
                        st.caption(f"📅 {project.get('timestamp', 'Unknown date')}")
                    
                    with col2:
                        if project.get('github_url'):
                            st.markdown(f"[🔗 GitHub]({project['github_url']})")
                        if project.get('demo_url'):
                            st.markdown(f"[🌐 Live Demo]({project['demo_url']})")
                        if project.get('external_link'):
                            st.markdown(f"[📄 External Link]({project['external_link']})")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("⭐ Bookmark", key=f"bookmark_proj_{project['id']}"):
                            data_manager.add_bookmark(project['id'], 'project')
                            st.success("Bookmarked!")
                            st.rerun()
                    
                    with col2:
                        if st.button("👍 Like", key=f"like_proj_{project['id']}"):
                            # In a real app, this would increment likes
                            st.success("Liked!")
                    
                    st.markdown("---")
                    st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No projects found matching your criteria.")

def upload_project():
    st.subheader("📤 Share Your Project")
    
    with st.form("upload_project", clear_on_submit=True):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Project Title*")
            author = st.text_input("Your Name*", value="Anonymous")
            category = st.selectbox("Category*", [
                "Web Application", "Mobile App", "Desktop Application", "Data Science",
                "Machine Learning", "Game Development", "DevOps", "Open Source Library",
                "Academic Project", "Personal Project", "Other"
            ])
        
        with col2:
            github_url = st.text_input("GitHub URL", placeholder="https://github.com/username/repo")
            demo_url = st.text_input("Demo/Live URL", placeholder="https://yourproject.com")
            external_link = st.text_input("External Link", placeholder="Documentation, blog post, etc.")
            project_status = st.selectbox("Project Status", ["Completed", "In Progress", "Planning"])
        
        # Description
        description = st.text_area("Project Description*", height=150, 
                                 placeholder="Describe your project, its purpose, key features, and what you learned building it.")
        
        # Technologies
        st.write("**Technologies Used:**")
        col1, col2, col3 = st.columns(3)
        
        technologies = []
        with col1:
            if st.checkbox("Python"):
                technologies.append("Python")
            if st.checkbox("JavaScript"):
                technologies.append("JavaScript")
            if st.checkbox("React"):
                technologies.append("React")
            if st.checkbox("Node.js"):
                technologies.append("Node.js")
        
        with col2:
            if st.checkbox("HTML/CSS"):
                technologies.append("HTML/CSS")
            if st.checkbox("SQL"):
                technologies.append("SQL")
            if st.checkbox("MongoDB"):
                technologies.append("MongoDB")
            if st.checkbox("Docker"):
                technologies.append("Docker")
        
        with col3:
            if st.checkbox("AWS"):
                technologies.append("AWS")
            if st.checkbox("Git"):
                technologies.append("Git")
            if st.checkbox("API"):
                technologies.append("API")
            if st.checkbox("Machine Learning"):
                technologies.append("Machine Learning")
        
        # Additional technologies
        other_tech = st.text_input("Other Technologies (comma-separated)", 
                                  placeholder="Flutter, Django, PostgreSQL")
        if other_tech:
            technologies.extend([tech.strip() for tech in other_tech.split(',')])
        
        # Project image/screenshot
        uploaded_image = st.file_uploader("Upload Project Screenshot/Image", 
                                        type=['jpg', 'jpeg', 'png', 'gif'])
        
        # Additional details
        with st.expander("📋 Additional Details (Optional)"):
            challenges = st.text_area("Challenges Faced", 
                                    placeholder="What challenges did you encounter and how did you solve them?")
            learnings = st.text_area("Key Learnings", 
                                   placeholder="What did you learn from this project?")
            future_plans = st.text_area("Future Plans", 
                                      placeholder="What features or improvements do you plan to add?")
        
        if st.form_submit_button("Share Project"):
            if title and author and category and description:
                # Handle image upload
                image_path = None
                if uploaded_image:
                    temp_id = 1  # Will be replaced with actual ID after database insert
                    image_path = file_handler.save_uploaded_file(uploaded_image, temp_id, prefix="project_")
                
                # Add project to database
                project_id = data_manager.add_project(
                    title=title,
                    author=author,
                    category=category,
                    description=description,
                    technologies=technologies,
                    github_url=github_url,
                    demo_url=demo_url,
                    external_link=external_link,
                    status=project_status,
                    challenges=challenges,
                    learnings=learnings,
                    future_plans=future_plans,
                    image_path=image_path
                )
                
                st.success("Project shared successfully! Thank you for contributing to the community.")
                st.balloons()
            else:
                st.error("Please fill in all required fields (marked with *).")

if __name__ == "__main__":
    main()
