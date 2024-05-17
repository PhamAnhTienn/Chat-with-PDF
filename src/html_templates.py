css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}
.chat-message.user {
    background-color: #2f2f2f;
    flex-direction: row-reverse;
}
.chat-message.bot {
    background-color: #2f2f2f;
    flex-direction: row;
}
.chat-message .avatar {
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.chat-message .avatar img {
    max-width: 40px;
    max-height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message.bot .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}

.chat-message.user .message {
    padding: 0 1.5rem;
    color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://seeklogo.com/images/C/chatgpt-logo-02AFA704B5-seeklogo.com.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_1280.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''