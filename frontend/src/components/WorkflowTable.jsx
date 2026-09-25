import {
  CheckCircle2,
  Clock3,
  AlertCircle,
  Eye,
} from "lucide-react";


function StatusBadge({ status }) {

  const normalized =
    status?.toUpperCase() || "UNKNOWN";


  let className = "status-badge";


  if (
    normalized.includes("COMPLETED")
  ) {
    className += " status-success";
  }

  else if (
    normalized.includes("WAITING") ||
    normalized.includes("PENDING") ||
    normalized.includes("ACTION")
  ) {
    className += " status-warning";
  }

  else if (
    normalized.includes("FAILED")
  ) {
    className += " status-danger";
  }


  return (
    <span className={className}>

      {normalized.includes("COMPLETED") && (
        <CheckCircle2 size={14} />
      )}

      {(
        normalized.includes("WAITING") ||
        normalized.includes("PENDING") ||
        normalized.includes("ACTION")
      ) && (
        <Clock3 size={14} />
      )}

      {normalized.includes("FAILED") && (
        <AlertCircle size={14} />
      )}

      {normalized}

    </span>
  );
}


export default function WorkflowTable({
  workflows = [],
}) {

  return (
    <div className="table-card">

      <div className="table-header">

        <div>
          <h3>Recent Workflows</h3>

          <p>
            Live workflow execution history
          </p>
        </div>

      </div>


      <div className="table-wrapper">

        <table>

          <thead>

            <tr>

              <th>Workflow</th>

              <th>Intent</th>

              <th>Agent</th>

              <th>Status</th>

              <th>Confidence</th>

              <th>Action</th>

            </tr>

          </thead>


          <tbody>

            {workflows.map((workflow) => (

              <tr
                key={workflow.workflow_id}
              >

                <td>
                  <strong>
                    {workflow.workflow_id}
                  </strong>
                </td>


                <td>
                  {workflow.intent || "-"}
                </td>


                <td>
                  {workflow.selected_agent || "-"}
                </td>


                <td>
                  <StatusBadge
                    status={
                      workflow.status
                    }
                  />
                </td>


                <td>

                  {workflow.confidence != null
                    ? `${(
                        workflow.confidence * 100
                      ).toFixed(0)}%`
                    : "-"}

                </td>


                <td>

                  <button
                    className="icon-button"
                    title="View workflow"
                  >

                    <Eye size={16} />

                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}