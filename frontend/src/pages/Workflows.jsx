import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import WorkflowTable from "../components/WorkflowTable";
import { getWorkflows } from "../services/api";


export default function Workflows() {

  const [workflows, setWorkflows] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const loadWorkflows = async () => {

    try {

      setLoading(true);
      setError("");

      const data = await getWorkflows();

      setWorkflows(
        data.workflows || []
      );

    } catch (err) {

      setError(
        err.message ||
        "Unable to load workflows."
      );

    } finally {

      setLoading(false);

    }
  };


  useEffect(() => {

    loadWorkflows();

  }, []);


  return (
    <div className="page">

      <div className="page-header">

        <div>
          <h1>Workflows</h1>

          <p>
            Monitor and inspect enterprise
            automation workflows.
          </p>
        </div>


        <button
          className="secondary-button"
          onClick={loadWorkflows}
          disabled={loading}
        >

          <RefreshCw size={16} />

          {loading
            ? "Refreshing..."
            : "Refresh"}

        </button>

      </div>


      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}


      {loading ? (

        <div className="loading-state">
          Loading workflows...
        </div>

      ) : workflows.length === 0 ? (

        <div className="empty-state">

          <h3>No workflows yet</h3>

          <p>
            Send a request from the dashboard
            to create your first workflow.
          </p>

        </div>

      ) : (

        <WorkflowTable
          workflows={workflows}
        />

      )}

    </div>
  );
}