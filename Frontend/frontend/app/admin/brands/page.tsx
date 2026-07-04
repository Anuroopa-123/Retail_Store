"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { toast } from "react-hot-toast";

import "./brands.css";

interface Category {

    id: number;

    name: string;

}

interface Brand {

    id: number;

    category_id: number;

    category_name: string;

    name: string;

    description: string;

    logo_url: string;

    status: string;

}

export default function BrandsPage() {

    const { user } = useAuth();

    const [loading, setLoading] =
        useState(false);

    const [showModal, setShowModal] =
        useState(false);

    const [editModal, setEditModal] =
        useState(false);

    const [selectedId, setSelectedId] =
        useState<number | null>(null);

    const [search, setSearch] =
        useState("");

    const [categories, setCategories] =
        useState<Category[]>([]);

    const [brands, setBrands] =
        useState<Brand[]>([]);

    const [formData, setFormData] =
        useState({

            category_id: "",

            name: "",

            description: "",

            logo_url: "",

            status: "Active"

        });

    const [editData, setEditData] =
        useState({

            category_id: "",

            name: "",

            description: "",

            logo_url: "",

            status: "Active"

        });

    useEffect(() => {

        if(user){

            getCategories();

            getBrands();

        }

    },[user]);

    // =====================================
    // Get Categories
    // =====================================

    const getCategories = async () => {

        if(!user) return;

        try{

            const response = await fetch(

`http://127.0.0.1:8000/api/v1/product-categories/${user.tenant_id}/${user.store_id}`

            );

            const data = await response.json();

            setCategories(data);

        }

        catch(error){

            console.log(error);

        }

    };

    // =====================================
    // Get Brands
    // =====================================

    const getBrands = async () => {

        if(!user) return;

        try{

            const response = await fetch(

`http://127.0.0.1:8000/api/v1/brands/${user.tenant_id}/${user.store_id}`

            );

            const data = await response.json();

            setBrands(data);

        }

        catch(error){

            console.log(error);

        }

    };

    // =====================================
    // Create Brand
    // =====================================

    const createBrand = async () => {

        if(!user) return;

        setLoading(true);

        try{

            const response = await fetch(

                "http://127.0.0.1:8000/api/v1/brands/",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"

                    },

                    body:JSON.stringify({

                        ...formData,

                        tenant_id:user.tenant_id,

                        store_id:user.store_id,

                        category_id:Number(

                            formData.category_id

                        ),

                        created_by:user.id

                    })

                }

            );

            const result = await response.json();

            if(response.ok){

                toast.success(

                    "Brand Added Successfully"

                );

                setFormData({

                    category_id:"",

                    name:"",

                    description:"",

                    logo_url:"",

                    status:"Active"

                });

                setShowModal(false);

                getBrands();

            }

            else{

                toast.error(

                    result.detail ||

                    "Failed"

                );

            }

        }

        catch(error){

            console.log(error);

            toast.error(

                "Something Went Wrong"

            );

        }

        finally{

            setLoading(false);

        }

    };
    // =====================================
// Search Filter
// =====================================

const filteredBrands = brands.filter((item) =>
    item.name
        .toLowerCase()
        .includes(search.toLowerCase())
);

// =====================================
// Open Edit Modal
// =====================================

const openEdit = (brand: Brand) => {

    setSelectedId(brand.id);

    setEditData({

        category_id: String(brand.category_id),

        name: brand.name,

        description: brand.description || "",

        logo_url: brand.logo_url || "",

        status: brand.status

    });

    setEditModal(true);

};

// =====================================
// Update Brand
// =====================================

const updateBrand = async () => {

    if(!selectedId) return;

    try{

        const response = await fetch(

            `http://127.0.0.1:8000/api/v1/brands/${selectedId}`,

            {

                method:"PUT",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify({

                    ...editData,

                    category_id:Number(

                        editData.category_id

                    )

                })

            }

        );

        const result = await response.json();

        if(response.ok){

            toast.success(

                "Brand Updated Successfully"

            );

            setEditModal(false);

            getBrands();

        }

        else{

            toast.error(

                result.detail

            );

        }

    }

    catch(error){

        console.log(error);

    }

};

// =====================================
// Delete Brand
// =====================================

const deleteBrand = async (

    id:number

) => {

    const confirmDelete =

    window.confirm(

        "Delete this Brand?"

    );

    if(!confirmDelete){

        return;

    }

    try{

        const response = await fetch(

            `http://127.0.0.1:8000/api/v1/brands/${id}`,

            {

                method:"DELETE"

            }

        );

        if(response.ok){

            toast.success(

                "Brand Deleted"

            );

            getBrands();

        }

        else{

            toast.error(

                "Delete Failed"

            );

        }

    }

    catch(error){

        console.log(error);

    }

};

    return(

        <AdminLayout>

            <div className="brand-container">

                <div className="brand-header">

                    <h1>

                        Brand Management

                    </h1>

                    <button

                        className="add-btn"

                        onClick={()=>

                            setShowModal(true)

                        }

                    >

                        + Add Brand

                    </button>

                </div>

                <input

                    className="search-box"

                    placeholder="Search Brand..."

                    value={search}

                    onChange={(e)=>

                        setSearch(

                            e.target.value

                        )

                    }

                />

              <table className="brand-table">

    <thead>

        <tr>

            <th>Brand</th>

            <th>Category</th>

            <th>Description</th>

            <th>Status</th>

            <th>Actions</th>

        </tr>

    </thead>

    <tbody>

        {

            filteredBrands.length===0 ?

            (

                <tr>

                    <td colSpan={5}>

                        No Brands Found

                    </td>

                </tr>

            )

            :

            (

                filteredBrands.map((brand)=>(

                    <tr key={brand.id}>

                        <td>

                            {brand.name}

                        </td>

                        <td>

                            {brand.category_name}

                        </td>

                        <td>

                            {brand.description}

                        </td>

                        <td>

                            <span

                                className={

                                    brand.status==="Active"

                                    ?

                                    "status-active"

                                    :

                                    "status-inactive"

                                }

                            >

                                {brand.status}

                            </span>

                        </td>

                        <td>

                            <button

                                className="edit-btn"

                                onClick={()=>

                                    openEdit(brand)

                                }

                            >

                                Edit

                            </button>

                            <button

                                className="delete-btn"

                                onClick={()=>

                                    deleteBrand(brand.id)

                                }

                            >

                                Delete

                            </button>

                        </td>

                    </tr>

                ))

            )

        }

    </tbody>

</table>

                {

                    showModal && (

                        <div className="modal-overlay">

                            <div className="brand-modal">

                                <h2>

                                    Add Brand

                                </h2>

                                <select

                                    value={formData.category_id}

                                    onChange={(e)=>

                                        setFormData({

                                            ...formData,

                                            category_id:e.target.value

                                        })

                                    }

                                >

                                    <option value="">

                                        Select Category

                                    </option>

                                    {

                                        categories.map((cat)=>(

                                            <option

                                                key={cat.id}

                                                value={cat.id}

                                            >

                                                {cat.name}

                                            </option>

                                        ))

                                    }

                                </select>

                                <input

                                    placeholder="Brand Name"

                                    value={formData.name}

                                    onChange={(e)=>

                                        setFormData({

                                            ...formData,

                                            name:e.target.value

                                        })

                                    }

                                />

                                <textarea

                                    rows={4}

                                    placeholder="Description"

                                    value={formData.description}

                                    onChange={(e)=>

                                        setFormData({

                                            ...formData,

                                            description:e.target.value

                                        })

                                    }

                                />

                                <input

                                    placeholder="Logo URL"

                                    value={formData.logo_url}

                                    onChange={(e)=>

                                        setFormData({

                                            ...formData,

                                            logo_url:e.target.value

                                        })

                                    }

                                />

                                <select

                                    value={formData.status}

                                    onChange={(e)=>

                                        setFormData({

                                            ...formData,

                                            status:e.target.value

                                        })

                                    }

                                >

                                    <option>

                                        Active

                                    </option>

                                    <option>

                                        Inactive

                                    </option>

                                </select>

                                <div className="modal-actions">

                                    <button

                                        onClick={()=>

                                            setShowModal(false)

                                        }

                                    >

                                        Cancel

                                    </button>

                                    <button

                                        onClick={createBrand}

                                        disabled={loading}

                                    >

                                        {

                                            loading

                                            ?

                                            "Saving..."

                                            :

                                            "Save Brand"

                                        }

                                    </button>

                                </div>

                            </div>

                        </div>

                    )

                }
                {

editModal && (

<div className="modal-overlay">

<div className="brand-modal">

<h2>

Edit Brand

</h2>

<select

value={editData.category_id}

onChange={(e)=>

setEditData({

...editData,

category_id:e.target.value

})

}

>

<option value="">

Select Category

</option>

{

categories.map((cat)=>(

<option

key={cat.id}

value={cat.id}

>

{cat.name}

</option>

))

}

</select>

<input

value={editData.name}

onChange={(e)=>

setEditData({

...editData,

name:e.target.value

})

}

/>

<textarea

rows={4}

value={editData.description}

onChange={(e)=>

setEditData({

...editData,

description:e.target.value

})

}

/>

<input

placeholder="Logo URL"

value={editData.logo_url}

onChange={(e)=>

setEditData({

...editData,

logo_url:e.target.value

})

}

/>

<select

value={editData.status}

onChange={(e)=>

setEditData({

...editData,

status:e.target.value

})

}

>

<option>

Active

</option>

<option>

Inactive

</option>

</select>

<div className="modal-actions">

<button

onClick={()=>

setEditModal(false)

}

>

Cancel

</button>

<button

onClick={updateBrand}

>

Update Brand

</button>

</div>

</div>

</div>

)

}

            </div>

        </AdminLayout>

    );

}