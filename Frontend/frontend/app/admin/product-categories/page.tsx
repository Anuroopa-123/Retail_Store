"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { toast } from "react-hot-toast";

import "./product-categories.css";

interface ProductCategory {

    id: number;

    name: string;

    description: string;

    status: string;

    tenant_id: number;

    store_id: number;

}

export default function ProductCategoriesPage() {

    const { user } = useAuth();

    const [showModal, setShowModal] =
        useState(false);

    const [loading, setLoading] =
        useState(false);
const [editModal, setEditModal] =
useState(false);

const [selectedId, setSelectedId] =
useState<number | null>(null);

const [editData, setEditData] =
useState({

    name: "",

    description: "",

    status: "Active"

});
    const [search, setSearch] =
        useState("");

    const [categories, setCategories] =
        useState<ProductCategory[]>([]);

    const [formData, setFormData] =
        useState({

            name: "",

            description: "",

            status: "Active"

        });

    useEffect(() => {

        if (user) {

            getCategories();

        }

    }, [user]);

    const getCategories = async () => {

        if (!user) return;

        try {

            const response =
                await fetch(

                    `http://127.0.0.1:8000/api/v1/product-categories/${user.tenant_id}/${user.store_id}`

                );

            const data =
                await response.json();

            setCategories(data);

        }

        catch (error) {

            console.log(error);

        }

    };

    const createCategory = async () => {

        if (!user) return;

        setLoading(true);

        try {

            const response =
                await fetch(

                    "http://127.0.0.1:8000/api/v1/product-categories/",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type": "application/json"

                        },

                        body: JSON.stringify({

                            ...formData,

                            tenant_id: user.tenant_id,

                            store_id: user.store_id,

                            created_by: user.id

                        })

                    }

                );

            const result =
                await response.json();

            if (response.ok) {

                toast.success(

                    "Category Added Successfully"

                );

                setFormData({

                    name: "",

                    description: "",

                    status: "Active"

                });

                setShowModal(false);

                getCategories();

            }

            else {

                toast.error(

                    result.detail || "Failed"

                );

            }

        }

        catch (error) {

            console.log(error);

            toast.error(

                "Something Went Wrong"

            );

        }

        finally {

            setLoading(false);

        }

    };
    const openEdit = (category: ProductCategory) => {

    setSelectedId(category.id);

    setEditData({

        name: category.name,

        description: category.description,

        status: category.status

    });

    setEditModal(true);

};
const updateCategory = async () => {

    if(!selectedId) return;

    try{

        const response = await fetch(

            `http://127.0.0.1:8000/api/v1/product-categories/${selectedId}`,

            {

                method:"PUT",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify(editData)

            }

        );

        const result = await response.json();

        if(response.ok){

            toast.success("Category Updated");

            setEditModal(false);

            getCategories();

        }

        else{

            toast.error(result.detail);

        }

    }

    catch(error){

        console.log(error);

    }

};
const deleteCategory = async (

    id:number

) => {

    const confirmDelete =

    window.confirm(

        "Delete this category?"

    );

    if(!confirmDelete){

        return;

    }

    try{

        const response = await fetch(

            `http://127.0.0.1:8000/api/v1/product-categories/${id}`,

            {

                method:"DELETE"

            }

        );

        if(response.ok){

            toast.success(

                "Category Deleted"

            );

            getCategories();

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
    const filteredCategories = categories.filter((item) =>

    item.name
        .toLowerCase()
        .includes(search.toLowerCase())

);

    return (

        <AdminLayout>

            <div className="category-container">

                <div className="category-header">

                    <h1>

                        Product Categories

                    </h1>

                    <button

                        className="add-btn"

                        onClick={() =>
                            setShowModal(true)
                        }

                    >

                        + Add Category

                    </button>

                </div>

                <input

                    className="search-box"

                    placeholder="Search Category..."

                    value={search}

                    onChange={(e) =>
                        setSearch(e.target.value)
                    }

                />

            <table className="category-table">

<thead>

<tr>

{/* <th>ID</th> */}

<th>Category</th>

<th>Description</th>

<th>Status</th>

<th>Actions</th>

</tr>

</thead>

<tbody>

{

filteredCategories.length===0 ?

(

<tr>

<td colSpan={5}>

No Categories Found

</td>

</tr>

)

:

(

filteredCategories.map((item)=>(

<tr key={item.id}>

{/* <td>

{item.id}

</td> */}

<td>

{item.name}

</td>

<td>

{item.description}

</td>

<td>

<span

className={

item.status==="Active"

?

"status-active"

:

"status-inactive"

}

>

{item.status}

</span>

</td>

<td>

<button

className="edit-btn"

onClick={()=>

openEdit(item)

}

>

Edit

</button>

<button

className="delete-btn"

onClick={()=>

deleteCategory(item.id)

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

                            <div className="category-modal">

                                <h2>

                                    Add Product Category

                                </h2>

                                <input

                                    placeholder="Category Name"

                                    value={formData.name}

                                    onChange={(e) =>

                                        setFormData({

                                            ...formData,

                                            name: e.target.value

                                        })

                                    }

                                />

                                <textarea

                                    placeholder="Description"

                                    rows={4}

                                    value={formData.description}

                                    onChange={(e) =>

                                        setFormData({

                                            ...formData,

                                            description: e.target.value

                                        })

                                    }

                                />

                                <select

                                    value={formData.status}

                                    onChange={(e) =>

                                        setFormData({

                                            ...formData,

                                            status: e.target.value

                                        })

                                    }

                                >

                                    <option value="Active">

                                        Active

                                    </option>

                                    <option value="Inactive">

                                        Inactive

                                    </option>

                                </select>

                                <div className="modal-actions">

                                    <button

                                        onClick={() =>

                                            setShowModal(false)

                                        }

                                    >

                                        Cancel

                                    </button>

                                    <button

                                        onClick={createCategory}

                                        disabled={loading}

                                    >

                                        {

                                            loading

                                                ?

                                                "Saving..."

                                                :

                                                "Save Category"

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

<div className="category-modal">

<h2>

Edit Category

</h2>

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

onClick={updateCategory}

>

Update Category

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