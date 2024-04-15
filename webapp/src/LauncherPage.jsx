import React from "react";
import { useForm } from "react-hook-form";

const LauncherPage = ({ onLaunch }) => {
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
            className="nes-input"
            defaultValue=""
          />
        </div>
        <div class="nes-field">
          <label for="userName">User</label>
          <input
            {...register("userName")}
            className="nes-input"
            defaultValue=""
          />
        </div>
        <input
          type="submit"
          class="nes-btn is-primary"
          value="Join"
        />
      </form>
    </div>
  );
};

export default LauncherPage;
