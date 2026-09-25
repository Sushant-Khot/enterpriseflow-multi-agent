import {
  FileText,
  ShieldCheck,
  WalletCards,
  Headphones,
} from "lucide-react";


const agents = [
  {
    id: "A1_BLOG",
    title: "Blog Review",
    description:
      "Analyze and review blog content.",
    icon: FileText,
  },

  {
    id: "A2_BACKGROUND",
    title: "Background Check",
    description:
      "Validate employee background information.",
    icon: ShieldCheck,
  },

  {
    id: "A3_SALARY",
    title: "Salary & Incentive",
    description:
      "Calculate salary and performance incentives.",
    icon: WalletCards,
  },

  {
    id: "A4_SUPPORT",
    title: "Support Ticket",
    description:
      "Create and manage enterprise support requests.",
    icon: Headphones,
  },
];


export default function AgentSelector({
  selectedAgent,
  onSelect,
}) {

  return (
    <div className="agent-selector">

      {agents.map((agent) => {

        const Icon = agent.icon;

        const selected =
          selectedAgent === agent.id;

        return (
          <button
            key={agent.id}
            type="button"
            className={
              `agent-selector-card ${
                selected
                  ? "agent-selector-card-active"
                  : ""
              }`
            }
            onClick={() =>
              onSelect(agent.id)
            }
          >

            <div className="agent-selector-icon">
              <Icon size={22} />
            </div>

            <div className="agent-selector-content">

              <strong>
                {agent.title}
              </strong>

              <span>
                {agent.description}
              </span>

            </div>

          </button>
        );
      })}

    </div>
  );
}