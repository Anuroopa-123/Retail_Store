"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import "./departments.css";
import toast from "react-hot-toast";

interface Department {
  id: number;
  name: string;
  status: string;
}

export default function DepartmentsPage() {

  const { user } = useAuth();

  const [showModal, setShowModal] =
    useState(false);

  const [name, setName] =
    useState("");

  const [departments, setDepartments] =
    useState<Department[]>([]);

  useEffect(() => {

    getDepartments();

  }, []);

  const getDepartments =
    async () => {

      try {

        if (
          !user?.tenant_id ||
          !user?.store_id
        ) {
          return;
        }

        const response =
          await fetch(
            `http://127.0.0.1:8000/api/v1/departments/tenant/${user.tenant_id}/store/${user.store_id}`
          );

        const data =
          await response.json();

        setDepartments(data);

      } catch (error) {

        console.log(error);

      }

    };

  useEffect(() => {

    if (user) {

      getDepartments();

    }

  }, [user]);

const createDepartment = async () => {

  console.log("User Data", user);

  if (
    !user?.tenant_id ||
    !user?.store_id ||
    !user?.id
  ) {

    alert(
      "User information not loaded"
    );

    return;
  }

  const payload = {

    name,

    tenant_id:
      user.tenant_id,

    store_id:
      user.store_id,

    created_by:
      user.id
  };

  console.log(payload);

  const response =
    await fetch(
      "http://127.0.0.1:8000/api/v1/departments/",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body:
          JSON.stringify(
            payload
          )
      }
    );

  const result =
    await response.json();

  console.log(result);

  if(response.ok){

   toast.success(
  "Department Created Successfully"
);

    setShowModal(false);

    setName("");

    getDepartments();

  } else {

    alert(
      JSON.stringify(
        result
      )
    );
  }
};
console.log("USER =", user);
  return (

    <AdminLayout>

      <div className="department-container">

        <div className="department-header">

          <h1>
            Department Management
          </h1>

          <button
            className="add-btn"
            onClick={() =>
              setShowModal(true)
            }
          >
            + Add Department
          </button>

        </div>

        {/* Modal */}

        {showModal && (

          <div className="modal-overlay">

            <div className="employee-modal">

              <h2>
                Add Department
              </h2>

              <input
                placeholder="Department Name"
                value={name}
                onChange={(e) =>
                  setName(
                    e.target.value
                  )
                }
              />

              <div
                className="modal-actions"
              >

                <button
                  onClick={() =>
                    setShowModal(false)
                  }
                >
                  Cancel
                </button>

                <button
                  onClick={
                    createDepartment
                  }
                >
                  Save
                </button>

              </div>

            </div>

          </div>

        )}

        {/* Department Table */}

        <div className="table-container">

          <table>

            <thead>

              <tr>

                <th>ID</th>

                <th>
                  Department Name
                </th>

                <th>
                  Status
                </th>

              </tr>

            </thead>

            <tbody>

              {departments.length === 0 ? (

                <tr>

                  <td
                    colSpan={3}
                    style={{
                      textAlign:
                        "center"
                    }}
                  >
                    No Departments Found
                  </td>

                </tr>

              ) : (

                departments.map(
                  (
                    department
                  ) => (

                    <tr
                      key={
                        department.id
                      }
                    >

                      <td>
                        {
                          department.id
                        }
                      </td>

                      <td>
                        {
                          department.name
                        }
                      </td>

                      <td>

                        <span
                          className="status-badge"
                        >
                          {
                            department.status
                          }
                        </span>

                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

    </AdminLayout>

  );
}