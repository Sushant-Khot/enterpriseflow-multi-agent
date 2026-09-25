import {
  LayoutDashboard,
  Workflow,
  ShieldCheck,
  PlusCircle,
  Bot,
  Settings,
  Activity,
} from "lucide-react";


function Sidebar({
  activePage,
  setActivePage,
}) {

  const menuItems = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      id: "workflows",
      label: "Workflows",
      icon: Workflow,
    },
    {
      id: "approvals",
      label: "Approvals",
      icon: ShieldCheck,
    },
    {
      id: "new-workflow",
      label: "New Workflow",
      icon: PlusCircle,
    },
  ];


  return (
    <aside className="sidebar">

      <div className="brand">

        <div className="brand-icon">
          <Bot size={22} />
        </div>

        <div>
          <h2>EnterpriseFlow</h2>
          <span>AI Platform</span>
        </div>

      </div>


      <div className="sidebar-section">

        <span className="sidebar-label">
          PLATFORM
        </span>

        <nav>

          {menuItems.map((item) => {

            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`nav-item ${
                  activePage === item.id
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  setActivePage(item.id)
                }
              >

                <Icon size={19} />

                <span>
                  {item.label}
                </span>

              </button>
            );

          })}

        </nav>

      </div>


      <div className="sidebar-bottom">

        <div className="system-status">

          <div className="status-dot" />

          <div>
            <strong>System Online</strong>
            <span>All services operational</span>
          </div>

        </div>


        <button className="nav-item">

          <Settings size={19} />

          <span>
            Settings
          </span>

        </button>

      </div>

    </aside>
  );
}


export default Sidebar;