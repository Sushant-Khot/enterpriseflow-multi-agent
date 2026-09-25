import {
  Bell,
  Search,
} from "lucide-react";


function Header({
  activePage,
}) {

  const titles = {
    dashboard: "Dashboard",
    workflows: "Workflow Monitor",
    approvals: "Approval Center",
    "new-workflow": "New Workflow",
  };


  return (
    <header className="top-header">

      <div>

        <h1>
          {titles[activePage] ||
            "Dashboard"}
        </h1>

        <p>
          Monitor and manage enterprise
          AI workflows
        </p>

      </div>


      <div className="header-actions">

        <button className="icon-button">
          <Search size={19} />
        </button>

        <button className="icon-button">
          <Bell size={19} />

          <span className="notification-dot" />
        </button>


        <div className="user-profile">

          <div className="avatar">
            SK
          </div>

          <div>
            <strong>
              Admin User
            </strong>

            <span>
              Administrator
            </span>
          </div>

        </div>

      </div>

    </header>
  );
}


export default Header;