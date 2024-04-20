import { useEffect, useRef } from "react";

const ErrorDialog = ({ open, message, onClose }) => {
  const rootRef = useRef(null);

  useEffect(
    () => {
      if (!rootRef.current) {
        return;
      }

      if (open) {
        rootRef.current.showModal();
      } else {
        rootRef.current.close();
      }
    },
    [open, rootRef.current]
  );

  return (
    <dialog ref={rootRef} className="nes-dialog">
      <div method="dialog">
        <p class="title">Oops!</p>
        <p>An unexpected error has occurred.</p>
        <section class="dialog-menu">
          <button class="nes-btn" onClick={onClose}>
            OK
          </button>
        </section>
      </div>
    </dialog>
  );
};

export default ErrorDialog;
