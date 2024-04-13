const ensure = (expression, errorType = Error) => {
  if (!expression) {
    throw new errorType();
  }
};

export {
  ensure
};
