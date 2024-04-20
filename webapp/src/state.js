class InvalidStateError extends Error {

};

const initialStateFactory = () => ({
  error: false,
  errorMessage: null,
  connected: false,
  connecting: false,
  channel: null,
  user: null
});

export {
  InvalidStateError,

  initialStateFactory
};
