class ProtocolError extends Error {

}

const ServerMessageType = {
  CHANNEL_STATE: "channel_state",
  MESSAGE_BROADCAST: "message_broadcast",
  USER_JOIN: "user_join",
  USER_LEAVE: "user_leave"
};

const ClientMessageType = {
  MESSAGE_SEND_REQUEST: "message_send_request",
};

export {
  ClientMessageType,
  ProtocolError,
  ServerMessageType
};
