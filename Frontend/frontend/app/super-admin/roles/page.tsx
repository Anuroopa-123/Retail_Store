"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./roles.css";
import toast from "react-hot-toast";
import {
  FaEdit,
  FaTrash,
  FaExclamationTriangle
} from "react-icons/fa";

interface Role {
  id: number;
  name: string;
  slug: string;
}

interface Tenant {
  id: number;
  name: string;
}

export default function RolesPage() {

  const [roles, setRoles] =
    useState<Role[]>([]);

    const [showDeleteModal, setShowDeleteModal] =
  useState(false);

const [selectedRoleId, setSelectedRoleId] =
  useState<number | null>(null);

  const [tenants, setTenants] =
    useState<Tenant[]>([]);

  const [tenantId, setTenantId] =
    useState<number>(0);

  const [roleName, setRoleName] =
    useState("");

  const [showModal, setShowModal] =
    useState(false);

  const [editingRoleId, setEditingRoleId] =
    useState<number | null>(null);

  const loadRoles = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/roles/"
      );

      const data =
        await response.json();

      setRoles(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (error) {

      console.error(
        "Roles Error:",
        error
      );
    }
  };

  const loadTenants = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/tenants/"
      );

      const data =
        await response.json();

      if (
        Array.isArray(data)
      ) {

        setTenants(data);

        if (
          data.length > 0
        ) {

          setTenantId(
            data[0].id
          );
        }
      }

    } catch (error) {

      console.error(
        "Tenants Error:",
        error
      );
    }
  };

  useEffect(() => {

    const init = async () => {

      await loadRoles();

      await loadTenants();
    };

    init();

  }, []);

  const createRole = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/roles/create",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            tenant_id: tenantId,
            name: roleName
          })
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        toast.error(
  result.detail ||
  "Failed to create role"
);

        return;
      }
      toast.success(
  "Role created successfully"
);

      setRoleName("");

      setShowModal(false);

      loadRoles();

    } catch (error) {

      console.error(error);
    }
  };

  const updateRole = async () => {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/roles/${editingRoleId}`,
        {
          method: "PUT",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            name: roleName
          })
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        alert(
          result.detail ||
          "Failed to update role"
        );

        return;
      }
      toast.success(
  "Role updated successfully"
);

      setRoleName("");

      setEditingRoleId(null);

      setShowModal(false);

      loadRoles();

    } catch (error) {

      console.error(error);
    }
  };

  const deleteRole = async () => {

  if (!selectedRoleId) {
    return;
  }

  try {

    const response =
      await fetch(
        `http://127.0.0.1:8000/api/v1/roles/${selectedRoleId}`,
        {
          method: "DELETE"
        }
      );

    if (!response.ok) {

      toast.error(
        "Failed to delete role"
      );

      return;
    }

    toast.success(
      "Role deleted successfully"
    );

    setShowDeleteModal(false);

    setSelectedRoleId(null);

    loadRoles();

  } catch (error) {

    console.error(error);

    toast.error(
      "Something went wrong"
    );
  }
};

  return (

    <Layout>

      <div className="roles-page">

        <div className="page-header">

          <h1>
            Roles Management
          </h1>

          <button
            className="add-role-btn"
            onClick={() => {

              setEditingRoleId(null);

              setRoleName("");

              setShowModal(true);
            }}
          >
            + Add Role
          </button>

        </div>

        {showModal && (

          <div className="modal-overlay">

            <div className="modal">

              <h2>

                {editingRoleId
                  ? "Edit Role"
                  : "Add Role"}

              </h2>

              {!editingRoleId && (

                <select
                  value={tenantId}
                  onChange={(e) =>
                    setTenantId(
                      Number(
                        e.target.value
                      )
                    )
                  }
                  style={{
                    width: "100%",
                    padding: "12px",
                    marginBottom: "12px"
                  }}
                >

                  {tenants.map(
                    (tenant) => (

                      <option
                        key={tenant.id}
                        value={tenant.id}
                      >
                        {tenant.name}
                      </option>

                    )
                  )}

                </select>

              )}

              <input
                placeholder="Role Name"
                value={roleName}
                onChange={(e) =>
                  setRoleName(
                    e.target.value
                  )
                }
              />

              <div className="modal-actions">

                <button
                  className="cancel-btn"
                  onClick={() => {

                    setShowModal(false);

                    setEditingRoleId(null);
                  }}
                >
                  Cancel
                </button>

                <button
                  className="save-btn"
                  onClick={
                    editingRoleId
                      ? updateRole
                      : createRole
                  }
                >
                  Save
                </button>

              </div>

            </div>

          </div>

        )}
        {showDeleteModal && (

  <div className="modal-overlay">

    <div className="delete-modal">

   <div className="delete-icon warning">
  <FaExclamationTriangle />
</div>

      <h2>
        Delete Role?
      </h2>

      <p>
        Are you sure you want to
        delete this role?
      </p>

      <div className="delete-actions">

        <button
          className="cancel-btn"
          onClick={() => {

            setShowDeleteModal(
              false
            );

            setSelectedRoleId(
              null
            );
          }}
        >
          Cancel
        </button>

        <button
          className="confirm-delete-btn"
          onClick={deleteRole}
        >
          Yes, Delete
        </button>

      </div>

    </div>

  </div>

)}

        <div className="roles-table">

          <table>

            <thead>

              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Slug</th>
                <th>Actions</th>
              </tr>

            </thead>

            <tbody>

              {roles.length > 0 ? (

                roles.map((role) => (

                  <tr
                    key={role.id}
                  >

                    <td>
                      {role.id}
                    </td>

                    <td>
                      {role.name}
                    </td>

                    <td>
                      {role.slug}
                    </td>

                  <td>

  <button
    className="edit-btn"
    onClick={() => {

      setEditingRoleId(
        role.id
      );

      setRoleName(
        role.name
      );

      setShowModal(true);
    }}
  >
    <FaEdit />
    <span>Edit</span>
  </button>

  <button
    className="delete-btn"
  onClick={() => {

  setSelectedRoleId(
    role.id
  );

  setShowDeleteModal(true);
}}
  >
    <FaTrash />
    <span>Delete</span>
  </button>

</td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan={4}
                    className="no-data"
                  >
                    No Roles Found
                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

    </Layout>
  );
}