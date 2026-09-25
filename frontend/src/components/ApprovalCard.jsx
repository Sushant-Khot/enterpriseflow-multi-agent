import {
  CheckCircle2,
  RotateCcw,
} from "lucide-react";

import { useState } from "react";

import {
  submitApproval,
} from "../services/api";


export default function ApprovalCard({
  approval,
  onCompleted,
}) {

  const [feedback, setFeedback] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleSubmit = async (
    approved
  ) => {

    try {

      setLoading(true);
      setError("");

      const result =
        await submitApproval(
          approval.approval_id,
          {
            approved,
            feedback,
            user_id: "HR001",
            user_role: "HR_ADMIN",
          }
        );

      if (onCompleted) {
        onCompleted(result);
      }

    } catch (err) {

      setError(
        err.message ||
        "Approval failed."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="approval-card">

      <div className="approval-card-header">

        <div>

          <h3>
            Blog Review Approval
          </h3>

          <p>
            {approval.approval_id}
          </p>

        </div>

        <span className="status-badge status-warning">
          {approval.status || "PENDING"}
        </span>

      </div>


      <div className="approval-details">

        <div>
          <strong>
            Workflow
          </strong>

          <span>
            {approval.workflow_id}
          </span>
        </div>


        <div>
          <strong>
            Iteration
          </strong>

          <span>
            {approval.iteration || 1}
          </span>
        </div>

      </div>


      <div className="approval-review">

        <h4>
          Agent Review
        </h4>

        <pre>
          {approval.review}
        </pre>

      </div>


      <div className="approval-feedback">

        <label>
          Reviewer Feedback
        </label>

        <textarea
          value={feedback}
          onChange={(event) =>
            setFeedback(
              event.target.value
            )
          }
          placeholder="Enter feedback if revision is required..."
          rows={4}
        />

      </div>


      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}


      <div className="approval-actions">

        <button
          className="approve-button"
          disabled={loading}
          onClick={() =>
            handleSubmit(true)
          }
        >

          <CheckCircle2 size={17} />

          {loading
            ? "Processing..."
            : "Approve"}

        </button>


        <button
          className="revision-button"
          disabled={loading}
          onClick={() =>
            handleSubmit(false)
          }
        >

          <RotateCcw size={17} />

          Request Revision

        </button>

      </div>

    </div>
  );
}