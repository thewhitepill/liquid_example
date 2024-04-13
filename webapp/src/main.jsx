import React from "react";
import { createRoot } from "react-dom/client";

import App from "./App";
import config from "./config";

const root = createRoot(document.getElementById("app"));

root.render(
  <React.StrictMode>
    <App config={config} />
  </React.StrictMode>
);
