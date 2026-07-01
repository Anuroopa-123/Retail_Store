"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import "./employees.css";
import { useAuth } from "@/src/context/AuthContext";
import { toast } from "react-hot-toast/headless";

interface Department {
  id: number;
  name: string;
}

export default function EmployeesPage() {
     const { user } = useAuth();

  const [showModal, setShowModal] =
    useState(false);

  const [departments, setDepartments] =
    useState<Department[]>([]);

 const [formData, setFormData] =
useState({

  name: "",

  email: "",

  password: "",

  gender: "",

  phone: "",

  department_id: "",

  joining_date: ""
});

 useEffect(() => {

  if(user){
    getDepartments();
  }

}, [user]);

const getDepartments =
async () => {

  if(!user){
    return;
  }

  try {

    const response =
      await fetch(

`http://127.0.0.1:8000/api/v1/departments/tenant/${user.tenant_id}/store/${user.store_id}`

      );

    const data =
      await response.json();

    setDepartments(data);

  } catch(error){

    console.log(error);

  }
};

  const createEmployee =
    async () => {

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/api/v1/employees/",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json"
              },

            body: JSON.stringify({

  ...formData,

  tenant_id:
    user?.tenant_id,

  store_id:
    user?.store_id,

  department_id:
    Number(
      formData.department_id
    )
})
            }
          );

        if(response.ok){

        const result = await response.json();

console.log(result);

if(response.ok){

    toast.success("Employee Created Successfully");

}else{

    toast.error(result.detail);
}

          setShowModal(false);

        }

      } catch(error){

        console.log(error);

      }

    };

  return (

    <AdminLayout>

      <div className="employee-container">

        <div className="employee-header">

          <h1 className="employee-title">
            Employee Management
          </h1>

          <button
            className="add-btn"
            onClick={() =>
              setShowModal(true)
            }
          >
            + Add Employee
          </button>

        </div>

        <input
          className="search-box"
          placeholder="Search Employee..."
        />

        {showModal && (

          <div className="modal-overlay">

            <div className="employee-modal">

              <h2>
                Add Employee
              </h2>

              {/* <input
                placeholder="Employee Code"
                value={
                  formData.employee_code
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    employee_code:
                      e.target.value
                  })
                }
              /> */}

              <input
                placeholder="Employee Name"
                value={
                  formData.name
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    name:
                      e.target.value
                  })
                }
              />

              <input
                placeholder="Email"
                value={
                  formData.email
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    email:
                      e.target.value
                  })
                }
              />

              <input
                placeholder="Phone"
                value={
                  formData.phone
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    phone:
                      e.target.value
                  })
                }
              />

              <select
                value={
                  formData.gender
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    gender:
                      e.target.value
                  })
                }
              >
                <option value="">
                  Select Gender
                </option>

                <option value="Male">
                  Male
                </option>

                <option value="Female">
                  Female
                </option>
              </select>

              <select
                value={
                  formData.department_id
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    department_id:
                      e.target.value
                  })
                }
              >

                <option value="">
                  Select Department
                </option>

                {departments.map(
                  (dept) => (

                  <option
                    key={dept.id}
                    value={dept.id}
                  >
                    {dept.name}
                  </option>

                ))}

              </select>

              <input
                type="date"
                value={
                  formData.joining_date
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    joining_date:
                      e.target.value
                  })
                }
              />

              <input
                type="password"
                placeholder="Password"
                value={
                  formData.password
                }
                onChange={(e)=>
                  setFormData({
                    ...formData,
                    password:
                      e.target.value
                  })
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
                    createEmployee
                  }
                >
                  Save Employee
                </button>

              </div>

            </div>

          </div>

        )}

      </div>

    </AdminLayout>

  );
}