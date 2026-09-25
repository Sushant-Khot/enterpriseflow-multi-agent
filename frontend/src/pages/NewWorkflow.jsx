import { useState } from "react";

import AgentSelector from "../components/AgentSelector";

import BlogReviewForm from "../components/BlogReviewForm";

import BackgroundCheckForm
  from "../components/BackgroundCheckForm";

import SalaryForm
  from "../components/SalaryForm";

import SupportForm
  from "../components/SupportForm";

import WorkflowResult
  from "../components/WorkflowResult";

import {
  sendChatRequest,
} from "../services/api";


export default function NewWorkflow() {

  const [selectedAgent, setSelectedAgent] =
    useState("A1_BLOG");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [result, setResult] =
    useState(null);


  const handleSubmit = async (
    payload
  ) => {

    try {

      setLoading(true);
      setError("");
      setResult(null);

      const response =
        await sendChatRequest(
          payload
        );


      if (
        response.metadata?.approval_id
      ) {

        sessionStorage.setItem(
          "latest_approval_id",
          response.metadata.approval_id
        );

      }


      setResult(response);

    } catch (error) {

      setError(
        error.message ||
        "Workflow execution failed."
      );

    } finally {

      setLoading(false);

    }
  };


  const renderForm = () => {

    switch (selectedAgent) {

      case "A1_BLOG":

        return (
          <BlogReviewForm
            onSubmit={handleSubmit}
            loading={loading}
          />
        );


      case "A2_BACKGROUND":

        return (
          <BackgroundCheckForm
            onSubmit={handleSubmit}
            loading={loading}
          />
        );


      case "A3_SALARY":

        return (
          <SalaryForm
            onSubmit={handleSubmit}
            loading={loading}
          />
        );


      case "A4_SUPPORT":

        return (
          <SupportForm
            onSubmit={handleSubmit}
            loading={loading}
          />
        );


      default:

        return null;
    }
  };


  return (
    <div className="page">

      <div className="page-header">

        <div>

          <h1>
            New Workflow
          </h1>

          <p>
            Start a specialized enterprise
            automation workflow.
          </p>

        </div>

      </div>


      <section className="workflow-builder">

        <div className="workflow-builder-section">

          <div className="section-header">

            <div>

              <h2>
                Select Agent
              </h2>

              <p>
                Choose the workflow you want
                EnterpriseFlow AI to execute.
              </p>

            </div>

          </div>


          <AgentSelector
            selectedAgent={
              selectedAgent
            }
            onSelect={(agent) => {

              setSelectedAgent(agent);
              setResult(null);
              setError("");

            }}
          />

        </div>


        <div className="workflow-form-container">

          {renderForm()}

        </div>


        {error && (

          <div className="error-banner">

            {error}

          </div>

        )}


        {result && (

          <WorkflowResult
            result={result}
          />

        )}

      </section>

    </div>
  );
}