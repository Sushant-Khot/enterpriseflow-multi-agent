const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000/api/v1";


export async function sendChatRequest(data) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));

    throw new Error(
      error.detail || "Failed to send request."
    );
  }

  return response.json();
}


export async function getWorkflows() {
  const response = await fetch(
    `${API_URL}/workflows`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch workflows."
    );
  }

  return response.json();
}


export async function getWorkflow(workflowId) {
  const response = await fetch(
    `${API_URL}/workflows/${workflowId}`
  );

  if (!response.ok) {
    throw new Error(
      "Workflow not found."
    );
  }

  return response.json();
}


export async function getWorkflowState(
  workflowId
) {
  const response = await fetch(
    `${API_URL}/workflows/${workflowId}/state`
  );

  if (!response.ok) {
    const error =
      await response.json()
        .catch(() => ({}));

    throw new Error(
      error.detail ||
      "Failed to fetch workflow state."
    );
  }

  return response.json();
}


export async function getApproval(approvalId) {
  const response = await fetch(
    `${API_URL}/approvals/${approvalId}`
  );

  if (!response.ok) {
    throw new Error(
      "Approval not found."
    );
  }

  return response.json();
}


export async function submitApproval(
  approvalId,
  data
) {
  const response = await fetch(
    `${API_URL}/approvals/${approvalId}`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {

    const error =
      await response.json()
        .catch(() => ({}));

    throw new Error(
      error.detail ||
      "Failed to submit approval."
    );
  }

  return response.json();
}