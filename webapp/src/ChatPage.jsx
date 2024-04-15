import { useRef } from "react";

const ChatPage = ({
  channel,
  user,
  onMessageSend
}) => {
  const messageInputRef = useRef(null);

  const handleMessageSendButtonClick = () => {
    const content = messageInputRef.current.value;
    onMessageSend(content);

    messageInputRef.current.value = "";
  };

  return (
    <div className="chat-page">
      <header>
          <h2>#{channel.name}</h2>
      </header>
      <section>
        <main>
          <div className="messages nes-container">
            <ul>
              {channel.messages.map((message, index) => (
                <li key={index}>
                  {message.sender_name}: {message.content}
                </li>
              ))}
            </ul>
          </div>
          <div className="controls">
            <textarea
              ref={messageInputRef}
              class="nes-textarea"
              placeholder="Type a message..."
            />
            <button
              className="nes-btn is-primary"
              onClick={handleMessageSendButtonClick}
            >
              Send
            </button>
          </div>
        </main>
        <aside>
          <h3>{`Online Users (${channel.users.length})`}</h3>
          <ul>
            {channel.users.map(({ name }) => (
              <li key={name}>
                <i class="nes-icon heart" />
                {name}
              </li>
            ))}
          </ul>
        </aside>
      </section>
    </div>
  );
};

export default ChatPage;
