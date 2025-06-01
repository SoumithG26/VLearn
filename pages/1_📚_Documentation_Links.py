import streamlit as st
import json
from utils.db_data_manager import DBDataManager
from utils.auth_manager import require_auth, init_session_state

st.set_page_config(page_title="Documentation Links", page_icon="📚", layout="wide")

# Check authentication
init_session_state()
if not require_auth():
    st.switch_page("pages/0_🔐_Login.py")

data_manager = DBDataManager()

def main():
    st.title("📚 Documentation Links")
    st.markdown("Curated documentation links for popular tools and technologies")
    st.markdown("---")
    
    # Load documentation links
    doc_links = data_manager.load_documentation_links()
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search documentation...", placeholder="e.g., Python, Git, React")
    with col2:
        categories = list(set([link['category'] for link in doc_links]))
        selected_category = st.selectbox("Filter by category", ["All"] + categories)
    
    # Filter links based on search and category
    filtered_links = doc_links
    
    if search_term:
        filtered_links = [
            link for link in filtered_links 
            if search_term.lower() in link['title'].lower() 
            or search_term.lower() in link['description'].lower()
        ]
    
    if selected_category != "All":
        filtered_links = [link for link in filtered_links if link['category'] == selected_category]
    
    # Display links in cards
    if filtered_links:
        # Group by category
        links_by_category = {}
        for link in filtered_links:
            category = link['category']
            if category not in links_by_category:
                links_by_category[category] = []
            links_by_category[category].append(link)
        
        for category, links in links_by_category.items():
            st.subheader(f"📂 {category}")
            
            # Create columns for cards
            cols = st.columns(2)
            for idx, link in enumerate(links):
                with cols[idx % 2]:
                    with st.container():
                        st.markdown(f"### [{link['title']}]({link['url']})")
                        st.write(link['description'])
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.caption(f"🏷️ {link['category']}")
                        with col2:
                            st.caption(f"⭐ {link['rating']}/5")
                        with col3:
                            if st.button(f"Bookmark", key=f"bookmark_{link['id']}"):
                                data_manager.add_bookmark(link['id'], 'documentation')
                                st.success("Bookmarked!")
                                st.rerun()
                        
                        st.markdown("---")
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No documentation links found matching your criteria.")
    
    # Add new documentation link (Admin feature)
    with st.expander("➕ Suggest New Documentation Link"):
        st.write("Help improve V-Learn by suggesting new documentation links!")
        
        with st.form("add_doc_link"):
            title = st.text_input("Title*")
            url = st.text_input("URL*")
            description = st.text_area("Description*")
            category = st.selectbox("Category", ["Programming", "Tools", "Frameworks", "Databases", "DevOps", "Design", "Other"])
            
            if st.form_submit_button("Submit Suggestion"):
                if title and url and description:
                    # Add to database
                    data_manager.add_documentation_link(title, url, description, category, 5)
                    st.success("Thank you for your suggestion! Link has been added.")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

if __name__ == "__main__":
    main()
