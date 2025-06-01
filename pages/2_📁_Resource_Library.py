import streamlit as st
import json
from datetime import datetime
from utils.db_data_manager import DBDataManager
from utils.file_handler import FileHandler
from utils.auth_manager import require_auth, init_session_state, get_current_user

st.set_page_config(page_title="Resource Library", page_icon="📁", layout="wide")

# Check authentication
init_session_state()
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

data_manager = DBDataManager()
file_handler = FileHandler()

def main():
    st.title("📁 Resource Library")
    st.markdown("Upload, share, and discover learning resources from the community")
    st.markdown("---")
    
    # Check if upload should be shown from session state
    show_upload = st.session_state.get('show_upload', False)
    
    # Tabs for different sections
    tab1, tab2 = st.tabs(["🔍 Browse Resources", "📤 Upload Resource"])
    
    with tab1:
        browse_resources()
    
    with tab2:
        upload_resource()

def browse_resources():
    resources = data_manager.load_resources()
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Check for search from session state
        default_search = st.session_state.get('search_term', '')
        search_term = st.text_input("🔍 Search resources...", value=default_search, placeholder="Title, description, or author")
        # Clear search term from session state
        if 'search_term' in st.session_state:
            del st.session_state.search_term
    
    with col2:
        categories = list(set([resource['category'] for resource in resources])) if resources else []
        selected_category = st.selectbox("Category", ["All"] + categories)
    
    with col3:
        resource_types = list(set([resource['type'] for resource in resources])) if resources else []
        selected_type = st.selectbox("Type", ["All"] + resource_types)
    
    # Filter resources
    filtered_resources = resources
    
    if search_term:
        filtered_resources = [
            resource for resource in filtered_resources
            if search_term.lower() in resource['title'].lower()
            or search_term.lower() in resource.get('description', '').lower()
            or search_term.lower() in resource['author'].lower()
        ]
    
    if selected_category != "All":
        filtered_resources = [r for r in filtered_resources if r['category'] == selected_category]
    
    if selected_type != "All":
        filtered_resources = [r for r in filtered_resources if r['type'] == selected_type]
    
    # Sort options
    sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title A-Z", "Title Z-A"])
    
    if sort_option == "Newest First":
        filtered_resources.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    elif sort_option == "Oldest First":
        filtered_resources.sort(key=lambda x: x.get('timestamp', ''))
    elif sort_option == "Title A-Z":
        filtered_resources.sort(key=lambda x: x['title'])
    elif sort_option == "Title Z-A":
        filtered_resources.sort(key=lambda x: x['title'], reverse=True)
    
    st.markdown("---")
    
    # Display resources
    if filtered_resources:
        st.write(f"Found {len(filtered_resources)} resources")
        
        for resource in filtered_resources:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Resource header
                    st.subheader(resource['title'])
                    st.write(f"**Author:** {resource['author']}")
                    st.write(f"**Description:** {resource.get('description', 'No description available')}")
                    
                    # Tags
                    col_tag1, col_tag2, col_tag3 = st.columns(3)
                    with col_tag1:
                        st.caption(f"📂 {resource['category']}")
                    with col_tag2:
                        st.caption(f"📄 {resource['type']}")
                    with col_tag3:
                        st.caption(f"📅 {resource.get('timestamp', 'Unknown date')}")
                    
                    # Content display based on type
                    display_resource_content(resource)
                
                with col2:
                    # Action buttons
                    user_data = data_manager.load_user_data()
                    resource_id = resource['id']
                    
                    is_bookmarked = resource_id in user_data.get('bookmarks', [])
                    is_completed = resource_id in user_data.get('completed', [])
                    is_todo = resource_id in user_data.get('todo', [])
                    
                    if st.button("⭐ Bookmark" if not is_bookmarked else "❌ Remove Bookmark", 
                               key=f"bookmark_{resource_id}"):
                        if is_bookmarked:
                            data_manager.remove_bookmark(resource_id)
                        else:
                            data_manager.add_bookmark(resource_id, 'resource')
                        st.rerun()
                    
                    if st.button("✅ Mark Done" if not is_completed else "↩️ Mark Undone", 
                               key=f"complete_{resource_id}"):
                        if is_completed:
                            data_manager.remove_completed(resource_id)
                        else:
                            data_manager.add_completed(resource_id)
                        st.rerun()
                    
                    if st.button("📝 Add to Todo" if not is_todo else "❌ Remove from Todo", 
                               key=f"todo_{resource_id}"):
                        if is_todo:
                            data_manager.remove_todo(resource_id)
                        else:
                            data_manager.add_todo(resource_id)
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No resources found matching your criteria. Try adjusting your search or filters.")

def display_resource_content(resource):
    """Display resource content based on its type"""
    if resource['type'] == 'Link':
        if resource.get('content'):
            st.markdown(f"🔗 [Open Link]({resource['content']})")
    
    elif resource['type'] == 'Text':
        if resource.get('content'):
            with st.expander("📄 View Content"):
                st.text_area("", resource['content'], height=200, disabled=True, label_visibility="collapsed")
    
    elif resource['type'] == 'Image':
        if resource.get('file_path'):
            try:
                st.image(resource['file_path'], caption=resource['title'], use_container_width=True)
            except:
                st.error("Image file not found")
    
    elif resource['type'] == 'Video':
        if resource.get('content'):
            # Check if it's a YouTube link or other video URL
            if 'youtube.com' in resource['content'] or 'youtu.be' in resource['content']:
                st.video(resource['content'])
            else:
                st.markdown(f"🎥 [Watch Video]({resource['content']})")
    
    elif resource['type'] == 'File':
        if resource.get('file_path'):
            st.markdown(f"📁 File: {resource.get('original_filename', 'Unknown')}")
            # In a real app, you'd provide download functionality

def upload_resource():
    st.subheader("📤 Upload New Resource")
    
    with st.form("upload_resource", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Resource Title*")
            author = st.text_input("Your Name*", value="Anonymous")
            category = st.selectbox("Category*", [
                "Programming", "Data Science", "Web Development", "Mobile Development",
                "DevOps", "Design", "Business", "Academic", "Tutorial", "Documentation", "Other"
            ])
        
        with col2:
            resource_type = st.selectbox("Resource Type*", [
                "Link", "Text", "Image", "Video", "File"
            ])
            description = st.text_area("Description*")
        
        # Content input based on type
        content = None
        uploaded_file = None
        
        if resource_type == "Link":
            content = st.text_input("URL*", placeholder="https://example.com")
        
        elif resource_type == "Text":
            content = st.text_area("Text Content*", height=200)
        
        elif resource_type == "Video":
            content = st.text_input("Video URL*", placeholder="YouTube URL or direct video link")
        
        elif resource_type == "Image":
            uploaded_file = st.file_uploader(
                "Upload Image*",
                type=['jpg', 'jpeg', 'png', 'gif']
            )
        
        elif resource_type == "File":
            uploaded_file = st.file_uploader(
                "Upload File*",
                type=['pdf', 'doc', 'docx', 'txt', 'zip', 'ppt', 'pptx', 'xls', 'xlsx']
            )
        
        if st.form_submit_button("Upload Resource"):
            if title and author and category and description:
                if resource_type in ["Link", "Text", "Video"] and not content:
                    st.error(f"Please provide the {resource_type.lower()} content.")
                elif resource_type in ["Image", "File"] and not uploaded_file:
                    st.error(f"Please upload a {resource_type.lower()} file.")
                else:
                    # Save the resource to database
                    file_path = None
                    original_filename = None
                    
                    # Handle file uploads
                    if uploaded_file:
                        # Generate temporary ID for file naming
                        temp_id = 1  # Will be replaced with actual ID after database insert
                        file_path = file_handler.save_uploaded_file(uploaded_file, temp_id)
                        original_filename = uploaded_file.name
                    
                    # Add resource to database
                    resource_id = data_manager.add_resource(
                        title=title,
                        author=author,
                        category=category,
                        type=resource_type,
                        description=description,
                        content=content,
                        file_path=file_path,
                        original_filename=original_filename
                    )
                    
                    st.success("Resource uploaded successfully!")
                    st.balloons()
            else:
                st.error("Please fill in all required fields.")

if __name__ == "__main__":
    main()
