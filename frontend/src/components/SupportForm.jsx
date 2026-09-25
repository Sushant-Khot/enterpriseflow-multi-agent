import { useState } from "react";


export default function SupportForm({
  onSubmit,
  loading,
}) {

  const [userId, setUserId] =
    useState("EMP001");

  const [issue, setIssue] =
    useState("");


  const handleSubmit = (event) => {

    event.preventDefault();

    if (!issue.trim()) {
      return;
    }

    onSubmit({

      message:
        issue.trim(),

      user_id: userId,

      user_role: "EMPLOYEE",

      context: {},
    });
  };


  return (
    <form
      className="specialist-form"
      onSubmit={handleSubmit}
    >

      <div className="form-section">

        <h3>
          Support Ticket
        </h3>

        <p>
          Submit an enterprise support request.
          Unmatched requests can be converted
          into support tickets by A4.
        </p>

      </div>


      <div className="form-group">

        <label>
          User ID
        </label>

        <input
          value={userId}
          onChange={(event) =>
            setUserId(event.target.value)
          }
          required
        />

      </div>


      <div className="form-group">

        <label>
          Describe the Issue
        </label>

        <textarea
          value={issue}
          onChange={(event) =>
            setIssue(event.target.value)
          }
          placeholder="Describe your problem..."
          rows={8}
          required
        />

      </div>


      <button
        type="submit"
        className="primary-button"
        disabled={loading}
      >

        {loading
          ? "Creating..."
          : "Create Support Request"}

      </button>

    </form>
  );
}