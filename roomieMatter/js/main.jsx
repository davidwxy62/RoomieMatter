import React from "react";
import { createRoot } from "react-dom/client";
import RequestList from "./requestlist";
import Index from "./index";

if (document.getElementById("reactEntry_pendingRequests")) {
    const root_pendingRequests = createRoot(document.getElementById("reactEntry_pendingRequests"));
    root_pendingRequests.render(<RequestList url="/api/pendingRequests" />);
}

if (document.getElementById("reactEntry_index")) {
    const root_statusButton = createRoot(document.getElementById("reactEntry_index"));
    root_statusButton.render(<Index/>);
}

