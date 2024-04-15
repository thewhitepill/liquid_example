import { useEffect, useRef, useState } from "react";

import ChatPage from "./ChatPage";
import LauncherPage from "./LauncherPage";
import {
  ClientMessageType,
  ProtocolError,
  ServerMessageType
} from "./protocol";

import { InvalidStateError, initialStateFactory } from "./state";
import { ensure } from "./utility";

const App = ({ config }) => {
  const client = useRef(null);
  const [state, setState] = useState(initialStateFactory);

  const handleMessageSend = content => {
    ensure(state.connected, InvalidStateError);

    const message = {
      type: ClientMessageType.MESSAGE_SEND_REQUEST,
      content
    }

    client.current.send(JSON.stringify(message));
  };

  const handleLaunch = async ({ channelName, userName }) => {
    const url = `${config.api.url}/channels/${channelName}/users/${userName}`;
    client.current = new WebSocket(url);

    client.current.onopen = () => {
      setState(
        state => ({
          ...state,
          connected: true
        })
      );
    };

    client.current.onmessage = event => {
      const message = JSON.parse(event.data);

      if (message.type === ServerMessageType.CHANNEL_STATE) {
        const { channel } = message;
        const user = channel.users.find(user => user.name === userName);

        setState(
          state => ({
            ...state,
            channel,
            user
          })
        );
      } else {
        throw new ProtocolError();
      }
    }
  };

  useEffect(
    () => {
      if (state.connected && state.channel && client.current) {
        client.current.onmessage = event => {
          const message = JSON.parse(event.data);

          if (message.type === ServerMessageType.MESSAGE_BROADCAST) {
            const channel = {
              ...state.channel,
              messages: [
                ...state.channel.messages,
                message.message
              ]
            };

            setState({ ...state, channel });
          } else if (message.type === ServerMessageType.USER_JOINED) {
            const { user } = message;
            const channel = {
              ...state.channel,
              users: [
                ...state.channel.users,
                user
              ]
            };

            setState({ ...state, channel });
          } else if (message.type === ServerMessageType.USER_LEFT) {
            const { user } = message;
            const channel = {
              ...state.channel,
              users: state.channel.users.filter(
                other => other.name !== user.name
              )
            };

            setState({ ...state, channel });
          } else {
            throw new ProtocolError();
          }
        };
      }
    },
    [state]
  );

  if (!state.connected) {
    return (
      <LauncherPage onLaunch={handleLaunch} />
    )
  }

  if (!state.channel) {
    return (
      <div>Connecting...</div>
    )
  }

  return (
    <ChatPage
      channel={state.channel}
      user={state.user}
      onMessageSend={handleMessageSend}
    />
  );
};

export default App;
