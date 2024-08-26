from Pdf import show_chat_page
import streamlit as st

def show_home_page():
    st.title("Home Page")
    st.write("This is the home page content.")
    
    # Thêm nút để điều hướng đến trang Chat
    if st.button("Go to Chat Page"):
        st.session_state.current_page = "Chat"
        st.rerun()

def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Chat":
        show_chat_page()
        
if __name__ == '__main__':
    main()
