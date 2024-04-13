import React, { useRef, useState } from "react";

import LauncherPage from "./LauncherPage";
import { initialStateFactory } from "./state";

const App = ({ config }) => {
  const client = useRef(null);
  const [state, setState] = useState(initialStateFactory);

  const handleLaunch = async ({ channelName, userName }) => {
    const url = `${config.api.url}/channels/${channelName}/users/${userName}`;
    client.current = new WebSocket(url);

    client.current.onopen = () => {
      setState({
        connected: true,
        channelName,
        userName,
      });
    };

    client.current.onmessage = event => {
      const message = JSON.parse(event.data);
      console.log(message);
    }
  };

  if (!state.connected) {
    return (
      <LauncherPage onLaunch={handleLaunch} />
    )
  } else {
    throw Error();
  }
};

export default App;
