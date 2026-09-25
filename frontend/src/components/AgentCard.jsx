import {
  FileText,
  ShieldCheck,
  Wallet,
  Headphones,
  Network,
} from "lucide-react";


const icons = {
  A1_BLOG: FileText,
  A2_BACKGROUND: ShieldCheck,
  A3_SALARY: Wallet,
  A4_SUPPORT: Headphones,
  A5_ORCHESTRATOR: Network,
};


function AgentCard({
  agent,
  name,
  description,
  status = "Active",
  requests,
}) {

  const Icon =
    icons[agent] || Network;


  return (
    <div className="agent-card">

      <div className="agent-header">

        <div className="agent-icon">
          <Icon size={20} />
        </div>

        <span className="agent-status">
          <span />
          {status}
        </span>

      </div>


      <div className="agent-body">

        <span className="agent-id">
          {agent}
        </span>

        <h3>
          {name}
        </h3>

        <p>
          {description}
        </p>

      </div>


      <div className="agent-footer">

        <span>
          Requests
        </span>

        <strong>
          {requests}
        </strong>

      </div>

    </div>
  );
}


export default AgentCard;