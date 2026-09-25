import {
  CheckCircle2,
  Clock3,
  XCircle,
} from "lucide-react";


export default function WorkflowResult({
  result,
}) {

  if (!result) {
    return null;
  }


  const status =
    result.status?.toUpperCase();


  const isCompleted =
    status?.includes("COMPLETED");


  const isWaiting =
    status?.includes("WAITING");

  const response =
    result.response ?? result.message ?? "";

  const responseText =
    typeof response === "string"
      ? response
      : JSON.stringify(response, null, 2);


  return (
    <div className="workflow-result">

      <div className="workflow-result-header">

        <div>

          <span className="result-label">
            Workflow Result
          </span>

          <h3>
            {result.workflow_id}
          </h3>

        </div>


        <div className="result-status">

          {isCompleted && (
            <CheckCircle2 size={18} />
          )}

          {isWaiting && (
            <Clock3 size={18} />
          )}

          {!isCompleted &&
            !isWaiting && (
              <XCircle size={18} />
            )}

          {status}

        </div>

      </div>


      <div className="result-response">

        <pre>
          {responseText || "Request processed successfully."}
        </pre>

      </div>


      {result.metadata && (

        <div className="result-metadata">

          <div>
            <span>
              Intent
            </span>

            <strong>
              {result.metadata.intent ||
                "-"}
            </strong>
          </div>


          <div>
            <span>
              Agent
            </span>

            <strong>
              {result.metadata
                .selected_agent ||
                "-"}
            </strong>
          </div>


          <div>
            <span>
              Confidence
            </span>

            <strong>
              {result.metadata
                .confidence != null
                ? `${(
                    result.metadata
                      .confidence * 100
                  ).toFixed(0)}%`
                : "-"}
            </strong>
          </div>

        </div>

      )}

    </div>
  );
}