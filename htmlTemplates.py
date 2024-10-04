css = '''
<style>
.rag-chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.rag-chat-message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.rag-chat-message .avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.rag-chat-message .avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rag-chat-message .message-content {
  flex-grow: 1;
  padding: 15px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  max-width: 80%;
}

.rag-chat-message.user .message-content {
  background-color: #DCF8C6;
  color: #000;
  margin-left: auto;
}

.rag-chat-message.bot .message-content {
  background-color: #E5E5EA;
  color: #000;
}

.rag-chat-message .sender-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.rag-chat-message .message-text {
  line-height: 1.4;
}

.rag-chat-message .timestamp {
  font-size: 0.8em;
  color: #999;
  text-align: right;
  margin-top: 5px;
}
</style>
'''

bot_template = '''
<div class="rag-chat-container">
  <div class="rag-chat-message bot">
    <div class="avatar">
      <img src="https://i.ibb.co/G92bxfR/bot-avatar.png" alt="Bot Avatar">
    </div>
    <div class="message-content">
      <div class="sender-name">RAG Bot</div>
      <div class="message-text">{{MSG}}</div>
    </div>
  </div>
'''

user_template = '''
<div class="rag-chat-message user">
    <div class="message-content">
      <div class="sender-name">You</div>
      <div class="message-text">{{MSG}}</div>
    </div>
    <div class="avatar">
      <img src="https://i.ibb.co/7CL6X3Q/user-avatar.png" alt="User Avatar">
    </div>
  </div>
</div>
'''