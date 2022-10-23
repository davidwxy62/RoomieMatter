import React from "react";
import { createRoot } from "react-dom/client";
import StatusButton from "./statusbutton";
// Create a root
const root = createRoot(document.getElementById("reactEntry"));
// This method is only called once
// Insert the post component into the DOM
root.render(<StatusButton url="/api/status" />);
