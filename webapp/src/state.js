class InvalidStateError extends Error {

};

const initialStateFactory = () => ({
  connected: false,
  channel: null,
  user: null
});

export {
  InvalidStateError,

  initialStateFactory
};
