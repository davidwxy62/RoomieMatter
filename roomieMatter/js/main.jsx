import React from "react";
import { createRoot } from "react-dom/client";
import StatusButton from "./statusbutton";
import RequestList from "./requestlist";

if (document.getElementById("reactEntry_pendingRequests")) {
    const root_pendingRequests = createRoot(document.getElementById("reactEntry_pendingRequests"));
    root_pendingRequests.render(<RequestList url="/api/pendingRequests" />);
}

if (document.getElementById("reactEntry_statusButton")) {
    const root_statusButton = createRoot(document.getElementById("reactEntry_statusButton"));
    root_statusButton.render(<StatusButton url="/api/status" />);
}
