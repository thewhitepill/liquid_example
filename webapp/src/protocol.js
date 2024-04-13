class ProtocolError extends Error {

}

const ServerMessageType = {
  CHANNEL_STATE: "channel_state",
  MESSAGE_BROADCAST: "message_broadcast",
  USER_JOINED: "user_joined",
  USER_LEFT: "user_left"
};

const ClientMessageType = {
  MESSAGE_SEND_REQUEST: "message_send_request",
};

export {
  ClientMessageType,
  ProtocolError,
  ServerMessageType
};
