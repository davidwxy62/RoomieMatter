import React from "react";
import { createRoot } from "react-dom/client";
import RequestList from "./requestlist";
import IndexPage from "./indexpage";

if (document.getElementById("reactEntry_pendingRequests")) {
    const root_pendingRequests = createRoot(document.getElementById("reactEntry_pendingRequests"));
    root_pendingRequests.render(<RequestList url="/api/pendingRequests" />);
}

if (document.getElementById("reactEntry_indexPage")) {
    const root_statusButton = createRoot(document.getElementById("reactEntry_indexPage"));
    root_statusButton.render(<IndexPage/>);
}

