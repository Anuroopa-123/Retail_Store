"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import toast from "react-hot-toast";
import { apiFetch } from "@/src/lib/api/client";

import "./admin-profile.css";

export default function ProfilePage() {

  const { user } = useAuth();

  const [loading, setLoading] =
    useState(false);

  const [profile, setProfile] =
    useState({

      phone: "",

      gender: "",

      dob: "",

      address: "",

      city: "",

      state: "",

      country: "",

      pincode: "",

      photo: ""

    });

  useEffect(() => {

    if(user){

      getProfile();

    }

  },[user]);

 const getProfile = async () => {

  try {

    const data = await apiFetch<any>(
      "/api/v1/admin/profile/"
    );

    setProfile({

      phone: data.phone || "",

      gender: data.gender || "",

      dob: data.dob || "",

      address: data.address || "",

      city: data.city || "",

      state: data.state || "",

      country: data.country || "",

      pincode: data.pincode || "",

      photo: data.photo || ""

    });

  } catch (error) {

    console.log(error);

  }

};

  const updateProfile = async () => {

  setLoading(true);

  try {

    await apiFetch(

      "/api/v1/admin/profile/",

      {

        method: "PUT",

        body: JSON.stringify(profile)

      }

    );

    toast.success(
      "Profile Updated Successfully"
    );

  } catch (error: any) {

    console.log(error);

    toast.error(
      error.message || "Something went wrong"
    );

  } finally {

    setLoading(false);

  }

};

  return(

    <AdminLayout>

      <div className="profile-container">

        <div className="profile-card">

          <h1>

            My Profile

          </h1>

          <div className="profile-photo">

            <img

              src={
                profile.photo ||

                "/images/profile.png"
              }

              alt="Profile"

            />

          </div>

          <div className="profile-grid">

            <div>

              <label>

                Full Name

              </label>

              <input

                value={user?.name || ""}

                disabled

              />

            </div>

            <div>

              <label>

                Email

              </label>

              <input

                value={user?.email || ""}

                disabled

              />

            </div>

            <div>

              <label>

                Phone

              </label>

              <input

                value={profile.phone}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    phone:e.target.value

                  })

                }

              />

            </div>

            <div>

              <label>

                Gender

              </label>

              <select

                value={profile.gender}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    gender:e.target.value

                  })

                }

              >

                <option value="">

                  Select

                </option>

                <option>

                  Male

                </option>

                <option>

                  Female

                </option>

              </select>

            </div>

            <div>

              <label>

                Date Of Birth

              </label>

              <input

                type="date"

                value={profile.dob}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    dob:e.target.value

                  })

                }

              />

            </div>

            <div>

              <label>

                Pincode

              </label>

              <input

                value={profile.pincode}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    pincode:e.target.value

                  })

                }

              />

            </div>

            <div>

              <label>

                City

              </label>

              <input

                value={profile.city}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    city:e.target.value

                  })

                }

              />

            </div>

            <div>

              <label>

                State

              </label>

              <input

                value={profile.state}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    state:e.target.value

                  })

                }

              />

            </div>

            <div>

              <label>

                Country

              </label>

              <input

                value={profile.country}

                onChange={(e)=>

                  setProfile({

                    ...profile,

                    country:e.target.value

                  })

                }

              />

            </div>

          </div>

          <div>

            <label>

              Address

            </label>

            <textarea

              rows={4}

              value={profile.address}

              onChange={(e)=>

                setProfile({

                  ...profile,

                  address:e.target.value

                })

              }

            />

          </div>

          <button

            className="save-btn"

            onClick={updateProfile}

            disabled={loading}

          >

            {

              loading ?

              "Updating..."

              :

              "Update Profile"

            }

          </button>

        </div>

      </div>

    </AdminLayout>

  );

}