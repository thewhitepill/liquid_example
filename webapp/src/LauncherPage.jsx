import clsx from "clsx";
import { useForm } from "react-hook-form";

const LauncherPage = ({ connecting, onLaunch }) => {
  const { register, handleSubmit } = useForm();

  return (
    <div className="launcher-page">
      <form
        className="launcher nes-container with-title"
        onSubmit={handleSubmit(onLaunch)}
      >
        <p class="title">Log in</p>
        <div class="nes-field">
          <label for="channelName">Channel</label>
          <input
            {...register("channelName")}
            className={
              clsx(
                "nes-input",
                {
                  "is-disabled": connecting
                }
              )
            }
            defaultValue=""
          />
        </div>
        <div class="nes-field">
          <label for="userName">User</label>
          <input
            {...register("userName")}
            className={
              clsx(
                "nes-input",
                {
                  "is-disabled": connecting
                }
              )
            }
            defaultValue=""
          />
        </div>
        <input
          type="submit"
          className={
            clsx(
              "nes-btn",
              {
                "is-primary": !connecting,
                "is-disabled": connecting
              }
            )
          }
          value={
            connecting ? "Connecting..." : "Connect"
          }
        />
      </form>
    </div>
  );
};

export default LauncherPage;
