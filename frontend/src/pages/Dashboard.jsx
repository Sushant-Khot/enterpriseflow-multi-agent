import {
  Activity,
  CheckCircle2,
  Clock3,
  AlertTriangle,
} from "lucide-react";

import StatCard from "../components/StatCard";
import AgentCard from "../components/AgentCard";
import RequestForm from "../components/RequestForm";


function Dashboard() {

  return (
    <div className="dashboard">

      {/* Statistics */}

      <section className="stats-grid">

        <StatCard
          title="Total Workflows"
          value="128"
          description="+12% from last week"
          icon={Activity}
          type="blue"
        />

        <StatCard
          title="Completed"
          value="94"
          description="73.4% completion rate"
          icon={CheckCircle2}
          type="green"
        />

        <StatCard
          title="Pending Approval"
          value="7"
          description="Requires attention"
          icon={Clock3}
          type="orange"
        />

        <StatCard
          title="Failed"
          value="3"
          description="2.3% failure rate"
          icon={AlertTriangle}
          type="red"
        />

      </section>


      {/* Main grid */}

      <section className="dashboard-grid">

        <div className="request-panel">

          <div className="section-heading">

            <div>
              <span className="section-eyebrow">
                AUTOMATION
              </span>

              <h2>
                Create New Request
              </h2>

              <p>
                Submit a task to the EnterpriseFlow
                AI orchestration system.
              </p>
            </div>

          </div>

          <RequestForm />

        </div>


        <div className="agents-panel">

          <div className="section-heading">

            <div>
              <span className="section-eyebrow">
                AI AGENTS
              </span>

              <h2>
                Agent Network
              </h2>
            </div>

          </div>


          <div className="agents-list">

            <AgentCard
              agent="A5_ORCHESTRATOR"
              name="Orchestrator"
              description="Classifies requests and routes them to specialist agents."
              requests="128"
            />

            <AgentCard
              agent="A1_BLOG"
              name="Blog Review"
              description="Analyzes and reviews enterprise content."
              requests="32"
            />

            <AgentCard
              agent="A2_BACKGROUND"
              name="Background Check"
              description="Checks HR and security information."
              requests="21"
            />

            <AgentCard
              agent="A3_SALARY"
              name="Salary & Incentive"
              description="Calculates salary using deterministic rules."
              requests="45"
            />

            <AgentCard
              agent="A4_SUPPORT"
              name="Support Ticket"
              description="Creates tickets for unmatched requests."
              requests="30"
            />

          </div>

        </div>

      </section>

    </div>
  );
}


export default Dashboard;