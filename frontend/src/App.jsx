import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import Workflows from "./pages/Workflows";
import Approvals from "./pages/Approvals";
import NewWorkflow from "./pages/NewWorkflow";


function App() {

  const [activePage, setActivePage] =
    useState("dashboard");

  const renderPage = () => {

    switch (activePage) {

      case "workflows":
        return <Workflows />;

      case "approvals":
        return <Approvals />;

      case "new-workflow":
        return <NewWorkflow />;

      default:
        return <Dashboard />;
    }
  };


  return (
    <div className="app-shell">

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="main-content">

        <Header
          activePage={activePage}
        />

        <div className="page-content">
          {renderPage()}
        </div>

      </main>

    </div>
  );
}


export default App;