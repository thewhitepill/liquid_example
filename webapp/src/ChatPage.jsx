const ChatPage = ({ channel, user }) => {
  return (
    <div>
      <div>
        <h1>#{channel.name}</h1>
        <ul>
          {channel.messages.map((message, index) => (
            <li key={index}>
              {message.sender_name}: {message.content}
            </li>
          ))}
        </ul>
        <input type="text" />
      </div>
      <div>
        <h2>Users</h2>
        <ul>
          {channel.users.map(({ name }) => (
            <li key={name}>{name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatPage;
