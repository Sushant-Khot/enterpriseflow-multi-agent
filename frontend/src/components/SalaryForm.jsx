import { useState } from "react";


export default function SalaryForm({
  onSubmit,
  loading,
  currentRole = "EMPLOYEE",
}) {

  const [userId, setUserId] =
    useState("EMP001");

  const [userRole, setUserRole] =
    useState(currentRole);

  const [baseSalary, setBaseSalary] =
    useState("");

  const [allowance, setAllowance] =
    useState("");

  const [deduction, setDeduction] =
    useState("");

  const [performanceScore, setPerformanceScore] =
    useState("");


  const handleSubmit = (event) => {

    event.preventDefault();

    onSubmit({

      message:
        "Calculate monthly salary and performance incentive.",

      user_id: userId,

      user_role: userRole,

      context: {

        employee_data: {

          employee_id:
            userId,

          base_salary:
            Number(baseSalary),

          allowance:
            Number(allowance),

          deduction:
            Number(deduction),

          performance_score:
            Number(performanceScore),
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
          Salary & Incentive
        </h3>

        <p>
          Calculate monthly salary using the
          configured performance incentive rules.
        </p>

      </div>


      <div className="form-grid">

        <div className="form-group">

          <label>
            Employee ID
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
            Base Salary
          </label>

          <input
            type="number"
            min="0"
            value={baseSalary}
            onChange={(event) =>
              setBaseSalary(
                event.target.value
              )
            }
            required
          />

        </div>


        <div className="form-group">

          <label>
            Allowance
          </label>

          <input
            type="number"
            min="0"
            value={allowance}
            onChange={(event) =>
              setAllowance(
                event.target.value
              )
            }
            required
          />

        </div>


        <div className="form-group">

          <label>
            Deduction
          </label>

          <input
            type="number"
            min="0"
            value={deduction}
            onChange={(event) =>
              setDeduction(
                event.target.value
              )
            }
            required
          />

        </div>


        <div className="form-group">

          <label>
            Performance Score
          </label>

          <input
            type="number"
            min="0"
            max="100"
            value={performanceScore}
            onChange={(event) =>
              setPerformanceScore(
                event.target.value
              )
            }
            required
          />

        </div>

      </div>


      <button
        type="submit"
        className="primary-button"
        disabled={loading}
      >

        {loading
          ? "Calculating..."
          : "Calculate Salary"}

      </button>

    </form>
  );
}