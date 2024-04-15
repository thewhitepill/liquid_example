class InvalidStateError extends Error {

};

const initialStateFactory = () => ({
  connected: false,
  channel: null,
  user: null
});

const testStateFactory = () => ({
  connected: true,
  channel: {
    name: "test",
    messages: [
      { sender_name: "asdf", content: "hiii" },
      { sender_name: "asdf", content: "hiii" }
    ],
    users: [
      { name: "asdf" },
      { name: "asdf" }
    ]
  }
});

export {
  InvalidStateError,

  testStateFactory as initialStateFactory
};
