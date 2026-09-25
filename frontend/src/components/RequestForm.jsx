import { useState } from "react";

import {
  Send,
  Loader2,
} from "lucide-react";

import { sendChatRequest } from "../services/api";


function RequestForm() {

  const [message, setMessage] =
    useState("");

  const [userId, setUserId] =
    useState("EMP001");

  const [role, setRole] =
    useState("EMPLOYEE");

  const [loading, setLoading] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");


  async function handleSubmit(event) {

    event.preventDefault();

    if (!message.trim()) {
      setError(
        "Please enter a request."
      );

      return;
    }

    setLoading(true);
    setError("");
    setResult(null);


    try {

      const data =
        await sendChatRequest({
          message,
          user_id: userId,
          user_role: role,
          context: {},
        });

      if (data.metadata?.approval_id) {
        sessionStorage.setItem(
          "latest_approval_id",
          data.metadata.approval_id
        );
      }

      setResult(data);

      setMessage("");

    } catch (err) {

      setError(
        err.message ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <form
      className="request-form"
      onSubmit={handleSubmit}
    >

      <div className="form-row">

        <div className="form-group">

          <label>
            User ID
          </label>

          <input
            value={userId}
            onChange={(e) =>
              setUserId(e.target.value)
            }
            placeholder="EMP001"
          />

        </div>


        <div className="form-group">

          <label>
            Role
          </label>

          <select
            value={role}
            onChange={(e) =>
              setRole(e.target.value)
            }
          >

            <option value="EMPLOYEE">
              Employee
            </option>

            <option value="HR_ADMIN">
              HR
            </option>

            <option value="SUPPORT_ADMIN">
              Administrator
            </option>

          </select>

        </div>

      </div>


      <div className="form-group">

        <label>
          Request
        </label>

        <textarea
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          placeholder="Describe what you want EnterpriseFlow AI to do..."
          rows={7}
        />

      </div>


      {error && (
        <div className="form-error">
          {error}
        </div>
      )}


      <button
        className="primary-button"
        disabled={loading}
        type="submit"
      >

        {loading ? (
          <>
            <Loader2
              size={18}
              className="spin"
            />

            Processing...
          </>
        ) : (
          <>
            <Send size={18} />

            Submit Request
          </>
        )}

      </button>


      {result && (

        (() => {
          const response =
            result.response ?? result.message ?? "Request processed successfully.";

          const status =
            (result.status || "COMPLETED").toUpperCase();

          let statusLabel;

          if (status === "COMPLETED") {
            statusLabel = "Workflow completed";
          } else if (status === "WAITING_FOR_APPROVAL") {
            statusLabel = "Waiting for human approval";
          } else if (status === "SECURITY_BLOCKED") {
            statusLabel = "Request blocked by security";
          } else if (status === "FAILED") {
            statusLabel = "Workflow failed";
          } else {
            statusLabel = status.replaceAll("_", " ");
          }

          return (

        <div className="result-panel">

          <div className="result-header">
            <span>
              {statusLabel}
            </span>

            <span className="result-badge">
              {result.status ||
                "COMPLETED"}
            </span>
          </div>


          <div className="result-response">
            {typeof response === "string"
              ? response
              : JSON.stringify(response, null, 2)}
          </div>

          {status === "WAITING_FOR_APPROVAL" && (
            <div className="result-response">
              Open Approvals to complete human approval.
            </div>
          )}

        </div>

          );
        })()

      )}

    </form>
  );
}


export default RequestForm;