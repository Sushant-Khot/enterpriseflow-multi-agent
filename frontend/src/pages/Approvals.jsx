import {
  useEffect,
  useState,
} from "react";

import ApprovalCard from "../components/ApprovalCard";

import {
  getApproval,
} from "../services/api";


export default function Approvals() {

  const [
    approval,
    setApproval,
  ] = useState(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  /*
   * Temporary development behavior:
   *
   * We obtain the approval ID from
   * sessionStorage after a chat request.
   *
   * Later this will become:
   *
   * GET /approvals
   *
   * backed by DynamoDB.
   */

  const loadApproval =
    async () => {

      try {
        setError("");

        const approvalId =
          sessionStorage.getItem(
            "latest_approval_id"
          );

        if (!approvalId) {
          setLoading(false);
          return;
        }

        const data =
          await getApproval(
            approvalId,
            "HR001",
            "HR_ADMIN"
          );

        setApproval(data);

      } catch (err) {

        console.error(
          "Failed to load approval:",
          err
        );

        setError(
          "Unable to load approval. Please check that the backend is running."
        );

      } finally {

        setLoading(false);

      }
    };


  useEffect(() => {

    loadApproval();

  }, []);


  const handleCompleted =
    async (result) => {

      if (result?.status !== "PENDING") {
        sessionStorage.removeItem(
          "latest_approval_id"
        );
        setApproval(null);
        return;
      }

      await loadApproval();

    };


  return (
    <div className="page">

      <div className="page-header">

        <div>

          <h1>
            Approval Center
          </h1>

          <p>
            Review and approve pending
            agent actions.
          </p>

        </div>

      </div>


      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}


      {loading && (
        <div className="loading-state">
          Loading approvals...
        </div>
      )}


      {!loading && !error && !approval && (

        <div className="empty-state">

          <h3>
            No pending approvals
          </h3>

          <p>
            When A1 requires human review,
            the approval will appear here.
          </p>

        </div>

      )}


      {!loading && !error && approval && (

        <ApprovalCard
          approval={approval}
          onCompleted={
            handleCompleted
          }
        />

      )}

    </div>
  );
}