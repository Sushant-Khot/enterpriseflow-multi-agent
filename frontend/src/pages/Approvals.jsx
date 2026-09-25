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
            approvalId
          );

        setApproval(data);

      } catch (error) {

        console.error(
          "Failed to load approval:",
          error
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


      {loading && (
        <div className="loading-state">
          Loading approvals...
        </div>
      )}


      {!loading && !approval && (

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


      {!loading && approval && (

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