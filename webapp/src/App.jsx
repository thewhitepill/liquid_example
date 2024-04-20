import { useEffect, useRef, useState } from "react";

import ChatPage from "./ChatPage";
import ErrorDialog from "./ErrorDialog";
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

  const closeErrorDialog = () => {
    setState(
      state => ({
        ...state,
        error: false,
        errorMessage: null
      })
    );
  };

  const handleMessageSend = content => {
    ensure(state.connected, InvalidStateError);

    if (!client.current) {
      return;
    }

    const message = {
      type: ClientMessageType.MESSAGE_SEND_REQUEST,
      content
    }

    client.current.send(JSON.stringify(message));
  };

  const handleLaunch = async ({ channelName, userName }) => {
    const url = `${config.api.url}/channels/${channelName}/users/${userName}`;
    client.current = new WebSocket(url);

    setState(
      state => ({
        ...state,
        connecting: true
      })
    );

    client.current.onerror = event => {
      setState(
        state => ({
          ...state,
          connecting: false,
          error: true,
          errorMessage: "Failed to connect to the server."
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
            connecting: false,
            connected: true,
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
          } else if (message.type === ServerMessageType.USER_JOIN) {
            const { user } = message;
            const channel = {
              ...state.channel,
              users: [
                ...state.channel.users,
                user
              ]
            };

            setState({ ...state, channel });
          } else if (message.type === ServerMessageType.USER_LEAVE) {
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

  const content = state.connected
    ? (
      <ChatPage
        channel={state.channel}
        user={state.user}
        onMessageSend={handleMessageSend}
      />
    ) : (
      <LauncherPage
        connecting={state.connecting}
        onLaunch={handleLaunch}
      />
    );

  return (
    <>
      {content}
      <ErrorDialog
        open={state.error}
        onClose={closeErrorDialog}
        message={state.errorMessage}
      />
    </>
  );
};

export default App;
