from dependencies import *
from chatWithPdf import show_chat_page
from chatWithMySQL import show_SQL_page


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
    elif st.session_state.current_page == "SQL":
        show_SQL_page()
        
if __name__ == '__main__':
    main()
