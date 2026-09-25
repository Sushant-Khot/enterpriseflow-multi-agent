import { useState } from "react";


export default function BackgroundCheckForm({
  onSubmit,
  loading,
  currentRole = "EMPLOYEE",
}) {

  const [userId, setUserId] =
    useState("EMP001");

  const [userRole, setUserRole] =
    useState(currentRole);

  const [fullName, setFullName] =
    useState("");

  const [dateOfBirth, setDateOfBirth] =
    useState("");

  const [governmentId, setGovernmentId] =
    useState("");

  const [address, setAddress] =
    useState("");

  const [employmentHistory, setEmploymentHistory] =
    useState("");

  const [educationVerification, setEducationVerification] =
    useState("");


  const handleSubmit = (event) => {

    event.preventDefault();

    onSubmit({

      message:
        "Perform a background information check.",

      user_id: userId,

      user_role: userRole,

      context: {

        employee_data: {

          full_name: fullName,

          date_of_birth: dateOfBirth,

          government_id: governmentId,

          address: address,

          employment_history:
            employmentHistory,

          education_verification:
            educationVerification,
        },
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
          Background Check
        </h3>

        <p>
          Check whether required employee
          background information is available.
        </p>

      </div>


      <div className="form-grid">

        <div className="form-group">

          <label>
            User ID
          </label>

          <input
            value={userId}
            onChange={(event) =>
              setUserId(event.target.value)
            }
          />

        </div>


        <div className="form-group">

          <label>
            Role
          </label>

          <select
            value={userRole}
            onChange={(event) =>
              setUserRole(event.target.value)
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


        <div className="form-group">

          <label>
            Full Name
          </label>

          <input
            value={fullName}
            onChange={(event) =>
              setFullName(event.target.value)
            }
            required
          />

        </div>


        <div className="form-group">

          <label>
            Date of Birth
          </label>

          <input
            type="date"
            value={dateOfBirth}
            onChange={(event) =>
              setDateOfBirth(
                event.target.value
              )
            }
            required
          />

        </div>


        <div className="form-group">

          <label>
            Government ID
          </label>

          <input
            value={governmentId}
            onChange={(event) =>
              setGovernmentId(
                event.target.value
              )
            }
            required
          />

        </div>

      </div>


      <div className="form-group">

        <label>
          Address
        </label>

        <textarea
          value={address}
          onChange={(event) =>
            setAddress(event.target.value)
          }
          rows={3}
          required
        />

      </div>


      <div className="form-group">

        <label>
          Employment History
        </label>

        <textarea
          value={employmentHistory}
          onChange={(event) =>
            setEmploymentHistory(
              event.target.value
            )
          }
          rows={4}
          required
        />

      </div>


      <div className="form-group">

        <label>
          Education Verification
        </label>

        <textarea
          value={educationVerification}
          onChange={(event) =>
            setEducationVerification(
              event.target.value
            )
          }
          rows={4}
          required
        />

      </div>


      <button
        type="submit"
        className="primary-button"
        disabled={loading}
      >

        {loading
          ? "Checking..."
          : "Run Background Check"}

      </button>

    </form>
  );
}