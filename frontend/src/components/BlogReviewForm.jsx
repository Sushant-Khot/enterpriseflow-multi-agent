import { useState } from "react";


export default function BlogReviewForm({
  onSubmit,
  loading,
}) {

  const [userId, setUserId] =
    useState("EMP001");

  const [content, setContent] =
    useState("");


  const handleSubmit = (event) => {

    event.preventDefault();

    if (!content.trim()) {
      return;
    }

    onSubmit({
      message:
        "Please review the following blog content.",
      
      user_id: userId,

      user_role: "EMPLOYEE",

      context: {
        blog_content: content.trim(),
      },
    });
  };


  return (
    <form
      className="specialist-form"
      onSubmit={handleSubmit}
    >

      <div className="form-section">

        <h3>
          Blog Review
        </h3>

        <p>
          Submit blog content for A1 analysis
          and quality review.
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
          placeholder="EMP001"
          required
        />

      </div>


      <div className="form-group">

        <label>
          Blog Content
        </label>

        <textarea
          value={content}
          onChange={(event) =>
            setContent(event.target.value)
          }
          placeholder="Paste the blog content here..."
          rows={12}
          required
        />

      </div>


      <button
        type="submit"
        className="primary-button"
        disabled={loading}
      >

        {loading
          ? "Reviewing..."
          : "Start Blog Review"}

      </button>

    </form>
  );
}