import streamlit as st
from utils.db_data_manager import DBDataManager
from utils.auth_manager import require_auth, init_session_state

st.set_page_config(page_title="My Resources", page_icon="⭐", layout="wide")

# Check authentication
init_session_state()
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

data_manager = DBDataManager()

def main():
    st.title("⭐ My Resources")
    st.markdown("Manage your bookmarked resources, completed items, and todo list")
    st.markdown("---")
    
    # Load user data
    user_data = data_manager.load_user_data()
    resources = data_manager.load_resources()
    projects = data_manager.load_projects()
    doc_links = data_manager.load_documentation_links()
    
    # Tabs for different user resource categories
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Bookmarks", "✅ Completed", "📝 Todo List", "📊 Progress"])
    
    with tab1:
        display_bookmarks(user_data, resources, projects, doc_links)
    
    with tab2:
        display_completed(user_data, resources)
    
    with tab3:
        display_todo(user_data, resources)
    
    with tab4:
        display_progress(user_data, resources, projects)

def display_bookmarks(user_data, resources, projects, doc_links):
    st.subheader("📚 Your Bookmarked Items")
    
    bookmarks = user_data.get('bookmarks', [])
    
    if not bookmarks:
        st.info("You haven't bookmarked anything yet. Start exploring and bookmark items you want to save!")
        return
    
    # Categorize bookmarks
    resource_bookmarks = []
    project_bookmarks = []
    doc_bookmarks = []
    
    for bookmark_id in bookmarks:
        # Check if it's a resource
        resource = next((r for r in resources if r['id'] == bookmark_id), None)
        if resource:
            resource_bookmarks.append(resource)
            continue
        
        # Check if it's a project
        project = next((p for p in projects if p['id'] == bookmark_id), None)
        if project:
            project_bookmarks.append(project)
            continue
        
        # Check if it's documentation
        doc = next((d for d in doc_links if d['id'] == bookmark_id), None)
        if doc:
            doc_bookmarks.append(doc)
    
    # Display bookmarked resources
    if resource_bookmarks:
        st.write("**📁 Bookmarked Resources:**")
        for resource in resource_bookmarks:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **{resource['title']}** - {resource['category']}")
                    st.caption(f"By {resource['author']} | {resource.get('description', '')[:100]}...")
                with col2:
                    if st.button("❌", key=f"remove_res_{resource['id']}", help="Remove bookmark"):
                        data_manager.remove_bookmark(resource['id'])
                        st.rerun()
        st.markdown("---")
    
    # Display bookmarked projects
    if project_bookmarks:
        st.write("**🚀 Bookmarked Projects:**")
        for project in project_bookmarks:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **{project['title']}** - {project['category']}")
                    st.caption(f"By {project['author']} | {project.get('description', '')[:100]}...")
                with col2:
                    if st.button("❌", key=f"remove_proj_{project['id']}", help="Remove bookmark"):
                        data_manager.remove_bookmark(project['id'])
                        st.rerun()
        st.markdown("---")
    
    # Display bookmarked documentation
    if doc_bookmarks:
        st.write("**📚 Bookmarked Documentation:**")
        for doc in doc_bookmarks:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **[{doc['title']}]({doc['url']})** - {doc['category']}")
                    st.caption(doc.get('description', '')[:100] + "...")
                with col2:
                    if st.button("❌", key=f"remove_doc_{doc['id']}", help="Remove bookmark"):
                        data_manager.remove_bookmark(doc['id'])
                        st.rerun()

def display_completed(user_data, resources):
    st.subheader("✅ Completed Resources")
    
    completed_ids = user_data.get('completed', [])
    
    if not completed_ids:
        st.info("You haven't marked any resources as completed yet. Start learning and track your progress!")
        return
    
    completed_resources = []
    for resource_id in completed_ids:
        resource = next((r for r in resources if r['id'] == resource_id), None)
        if resource:
            completed_resources.append(resource)
    
    if completed_resources:
        st.write(f"You have completed **{len(completed_resources)}** resources! 🎉")
        
        for resource in completed_resources:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **{resource['title']}** - {resource['category']}")
                    st.caption(f"By {resource['author']} | Completed")
                with col2:
                    if st.button("↩️", key=f"uncomplete_{resource['id']}", help="Mark as not completed"):
                        data_manager.remove_completed(resource['id'])
                        st.rerun()
    else:
        st.info("Some completed resources may no longer be available.")

def display_todo(user_data, resources):
    st.subheader("📝 Your Todo List")
    
    todo_ids = user_data.get('todo', [])
    
    if not todo_ids:
        st.info("Your todo list is empty. Add resources you want to learn later!")
        return
    
    todo_resources = []
    for resource_id in todo_ids:
        resource = next((r for r in resources if r['id'] == resource_id), None)
        if resource:
            todo_resources.append(resource)
    
    if todo_resources:
        st.write(f"You have **{len(todo_resources)}** items in your todo list:")
        
        for resource in todo_resources:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"• **{resource['title']}** - {resource['category']}")
                    st.caption(f"By {resource['author']} | {resource.get('description', '')[:100]}...")
                with col2:
                    if st.button("✅", key=f"complete_todo_{resource['id']}", help="Mark as completed"):
                        data_manager.remove_todo(resource['id'])
                        data_manager.add_completed(resource['id'])
                        st.rerun()
                with col3:
                    if st.button("❌", key=f"remove_todo_{resource['id']}", help="Remove from todo"):
                        data_manager.remove_todo(resource['id'])
                        st.rerun()
    else:
        st.info("Some todo resources may no longer be available.")

def display_progress(user_data, resources, projects):
    st.subheader("📊 Your Learning Progress")
    
    total_resources = len(resources)
    completed_count = len(user_data.get('completed', []))
    bookmarked_count = len(user_data.get('bookmarks', []))
    todo_count = len(user_data.get('todo', []))
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Completed", completed_count)
    
    with col2:
        st.metric("Bookmarked", bookmarked_count)
    
    with col3:
        st.metric("Todo Items", todo_count)
    
    with col4:
        completion_rate = (completed_count / total_resources * 100) if total_resources > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Progress bar
    if total_resources > 0:
        st.write("**Overall Progress:**")
        progress = completed_count / total_resources
        st.progress(progress)
        st.caption(f"You've completed {completed_count} out of {total_resources} available resources")
    
    st.markdown("---")
    
    # Learning streaks and achievements
    st.subheader("🏆 Achievements")
    
    achievements = []
    
    if completed_count >= 1:
        achievements.append("🎯 First Completion - Completed your first resource!")
    
    if completed_count >= 5:
        achievements.append("📚 Knowledge Seeker - Completed 5 resources!")
    
    if completed_count >= 10:
        achievements.append("🔥 Learning Streak - Completed 10 resources!")
    
    if bookmarked_count >= 5:
        achievements.append("⭐ Collector - Bookmarked 5 items!")
    
    if todo_count >= 3:
        achievements.append("📝 Planner - Added 3 items to todo list!")
    
    if achievements:
        for achievement in achievements:
            st.success(achievement)
    else:
        st.info("Start learning to unlock achievements! Complete resources, bookmark items, and build your learning journey.")
    
    # Learning recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    if todo_count > 0:
        st.info(f"You have {todo_count} items in your todo list. Consider working on them next!")
    
    if bookmarked_count > completed_count:
        st.info("You have more bookmarked items than completed ones. Time to start learning!")
    
    if completed_count > 0 and todo_count == 0:
        st.info("Great job on completing resources! Consider adding more items to your todo list to continue learning.")

if __name__ == "__main__":
    main()
