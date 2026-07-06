"use client";

import { useEffect, useState } from "react";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { apiFetch } from "@/src/lib/api/client";
import { toast } from "react-hot-toast";

import "./products.css";

// ==============================
// Interfaces
// ==============================

interface Category {

    id: number;

    name: string;

}

interface Brand {

    id: number;

    name: string;

}

interface Product {

    id: number;

    product_name: string;

    sku: string;

    barcode: string;

    purchase_price: number;

    selling_price: number;

    tax: number;

    stock: number;

    minimum_stock: number;

    status: string;

    category_name: string;

    brand_name: string;

    image_url: string;

}

// ==============================
// Component
// ==============================

export default function ProductsPage() {

    const { user } = useAuth();

    // ==============================
    // Modal
    // ==============================

    const [showModal, setShowModal] =
        useState(false);

    // ==============================
    // Loading
    // ==============================

    const [loading, setLoading] =
        useState(false);

    // ==============================
    // Search
    // ==============================

    const [search, setSearch] =
        useState("");

    // ==============================
    // Edit
    // ==============================

    const [editId, setEditId] =
        useState<number | null>(null);

    // ==============================
    // Image Upload
    // ==============================

    const [selectedImage, setSelectedImage] =
        useState<File | null>(null);

    const [imagePreview, setImagePreview] =
        useState("");

    // ==============================
    // Dropdown Data
    // ==============================

    const [categories, setCategories] =
        useState<Category[]>([]);

    const [brands, setBrands] =
        useState<Brand[]>([]);

    // ==============================
    // Product List
    // ==============================

    const [products, setProducts] =
        useState<Product[]>([]);

    // ==============================
    // Form Data
    // ==============================

    const [formData, setFormData] =
        useState({

            category_id: "",

            brand_id: "",

            product_name: "",

            purchase_price: "",

            selling_price: "",

            tax: "",

            stock: "",

            minimum_stock: "",

            unit: "",

            description: "",

            status: "Active"

        });

    // ==============================
    // Load Initial Data
    // ==============================

    useEffect(() => {

        if (user) {

            getCategories();

            getBrands();

            getProducts();

        }

    }, [user]);

    // ==============================
    // Get Categories
    // ==============================

    const getCategories = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<Category[]>(

                `/api/v1/product-categories/${user.tenant_id}/${user.store_id}`

            );

            setCategories(data);

        }

        catch (error) {

            console.log(error);

            toast.error("Failed to load categories");

        }

    };

    // ==============================
    // Get Brands
    // ==============================

    const getBrands = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<Brand[]>(

                `/api/v1/brands/${user.tenant_id}/${user.store_id}`

            );

            setBrands(data);

        }

        catch (error) {

            console.log(error);

            toast.error("Failed to load brands");

        }

    };

    // ==============================
    // Get Products
    // ==============================

    const getProducts = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<Product[]>(

                `/api/v1/products/${user.tenant_id}/${user.store_id}`

            );

            setProducts(data);

        }

        catch (error) {

            console.log(error);

            toast.error("Failed to load products");

        }

    };

  // ======================================
// Handle Image Selection
// ======================================

const handleImageChange = (

    e: React.ChangeEvent<HTMLInputElement>

) => {

    const file = e.target.files?.[0];

    if (!file) return;

    setSelectedImage(file);

    setImagePreview(

        URL.createObjectURL(file)

    );

};

// ======================================
// Create Product
// ======================================

const createProduct = async () => {

    if (!user) return;

    setLoading(true);

    try {

        let imageUrl = "";

        // ---------------------------------
        // Upload Product Image
        // ---------------------------------

        if (selectedImage) {

            const uploadData = new FormData();

            uploadData.append(

                "file",

                selectedImage

            );

            const token =

                localStorage.getItem(

                    "access_token"

                );

            const uploadResponse = await fetch(

                `${process.env.NEXT_PUBLIC_API_URL}/api/v1/product-upload/`,

                {

                    method: "POST",

                    headers: {

                        ...(token
                            ? {
                                Authorization:
                                    `Bearer ${token}`
                            }
                            : {})

                    },

                    body: uploadData

                }

            );

            if (!uploadResponse.ok) {

                throw new Error(

                    "Image Upload Failed"

                );

            }

            const uploadResult =

                await uploadResponse.json();

            imageUrl =

                uploadResult.image_url;

        }

        // ---------------------------------
        // Save Product
        // ---------------------------------

        await apiFetch(

            "/api/v1/products/",

            {

                method: "POST",

                body: JSON.stringify({

                    tenant_id:

                        user.tenant_id,

                    store_id:

                        user.store_id,

                    category_id:

                        Number(

                            formData.category_id

                        ),

                    brand_id:

                        Number(

                            formData.brand_id

                        ),

                    product_name:

                        formData.product_name,

                    purchase_price:

                        Number(

                            formData.purchase_price

                        ),

                    selling_price:

                        Number(

                            formData.selling_price

                        ),

                    tax:

                        Number(

                            formData.tax

                        ),

                    stock:

                        Number(

                            formData.stock

                        ),

                    minimum_stock:

                        Number(

                            formData.minimum_stock

                        ),

                    unit:

                        formData.unit,

                    description:

                        formData.description,

                    image_url:

                        imageUrl,

                    status:

                        formData.status,

                    created_by:

                        user.id

                })

            }

        );

        toast.success(

            "Product Added Successfully"

        );

        // ---------------------------------
        // Reset Form
        // ---------------------------------

        setFormData({

            category_id: "",

            brand_id: "",

            product_name: "",

            purchase_price: "",

            selling_price: "",

            tax: "",

            stock: "",

            minimum_stock: "",

            unit: "",

            description: "",

            status: "Active"

        });

        setSelectedImage(null);

        setImagePreview("");

        setEditId(null);

        setShowModal(false);

        await getProducts();

    }

    catch (error: any) {

        console.log(error);

        toast.error(

            error.message ||

            "Something went wrong"

        );

    }

    finally {

        setLoading(false);

    }

};

  return (

    <AdminLayout>

        <div className="product-container">

            {/* ===========================
                Header
            =========================== */}

            <div className="product-header">

                <h1>

                    Product Management

                </h1>

                <button

                    className="add-btn"

                    onClick={() => {

                        setEditId(null);

                        setShowModal(true);

                    }}

                >

                    + Add Product

                </button>

            </div>

            {/* ===========================
                Search Box
            =========================== */}

            <input

                type="text"

                className="search-box"

                placeholder="Search Product..."

                value={search}

                onChange={(e) =>

                    setSearch(

                        e.target.value

                    )

                }

            />

            {/* ===========================
                Product Table
            =========================== */}

            <table className="product-table">

                <thead>

                    <tr>

                        <th>Image</th>

                        <th>Product</th>

                        <th>Category</th>

                        <th>Brand</th>

                        <th>SKU</th>

                        <th>Barcode</th>

                        <th>Purchase Price</th>

                        <th>Selling Price</th>

                        <th>GST</th>

                        <th>Stock</th>

                        <th>Status</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        products

                        .filter((product) =>

                            product.product_name

                            .toLowerCase()

                            .includes(

                                search.toLowerCase()

                            )

                        )

                        .map((product) => (

                            <tr

                                key={product.id}

                            >

                                {/* Image */}

                                <td>

                                    {

                                        product.image_url ?

                                        (

                                            <img

                                                src={`${process.env.NEXT_PUBLIC_API_URL}${product.image_url}`}

                                                alt={product.product_name}

                                                className="table-image"

                                            />

                                        )

                                        :

                                        (

                                            <div className="no-image">

                                                No Image

                                            </div>

                                        )

                                    }

                                </td>

                                {/* Product */}

                                <td>

                                    {product.product_name}

                                </td>

                                {/* Category */}

                                <td>

                                    {product.category_name}

                                </td>

                                {/* Brand */}

                                <td>

                                    {product.brand_name}

                                </td>

                                {/* SKU */}

                                <td>

                                    {product.sku}

                                </td>

                                {/* Barcode */}

                                <td>

                                    {product.barcode}

                                </td>

                                {/* Purchase */}

                                <td>

                                    ₹

                                    {

                                        Number(

                                            product.purchase_price

                                        ).toFixed(2)

                                    }

                                </td>

                                {/* Selling */}

                                <td>

                                    ₹

                                    {

                                        Number(

                                            product.selling_price

                                        ).toFixed(2)

                                    }

                                </td>

                                {/* GST */}

                                <td>

                                    {product.tax}%

                                </td>

                                {/* Stock */}

                                <td>

                                    {product.stock}

                                </td>

                                {/* Status */}

                                <td>

                                    <span

                                        className={

                                            product.status === "Active"

                                            ?

                                            "status-active"

                                            :

                                            "status-inactive"

                                        }

                                    >

                                        {product.status}

                                    </span>

                                </td>

                                {/* Actions */}

                                <td>

                                    <button

                                        className="edit-btn"

                                        onClick={() => {

                                            setEditId(

                                                product.id

                                            );

                                            setShowModal(

                                                true

                                            );

                                        }}

                                    >

                                        Edit

                                    </button>

                                    <button

                                        className="delete-btn"

                                        onClick={() => {

                                            // Delete API

                                            // will be added later

                                        }}

                                    >

                                        Delete

                                    </button>

                                </td>

                            </tr>

                        ))

                    }

                    {

                        products.length === 0 && (

                            <tr>

                                <td

                                    colSpan={12}

                                    style={{

                                        textAlign: "center",

                                        padding: "30px"

                                    }}

                                >

                                    No Products Found

                                </td>

                            </tr>

                        )

                    }

                </tbody>

            </table>

          {
    showModal && (

        <div className="modal-overlay">

            <div className="product-modal">

                <h2>

                    {

                        editId

                            ?

                            "Edit Product"

                            :

                            "Add Product"

                    }

                </h2>

                {/* Category */}

                <select

                    value={formData.category_id}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            category_id: e.target.value

                        })

                    }

                >

                    <option value="">

                        Select Category

                    </option>

                    {

                        categories.map((category) => (

                            <option

                                key={category.id}

                                value={category.id}

                            >

                                {category.name}

                            </option>

                        ))

                    }

                </select>

                {/* Brand */}

                <select

                    value={formData.brand_id}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            brand_id: e.target.value

                        })

                    }

                >

                    <option value="">

                        Select Brand

                    </option>

                    {

                        brands.map((brand) => (

                            <option

                                key={brand.id}

                                value={brand.id}

                            >

                                {brand.name}

                            </option>

                        ))

                    }

                </select>

                {/* Product Name */}

                <input

                    type="text"

                    placeholder="Product Name"

                    value={formData.product_name}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            product_name: e.target.value

                        })

                    }

                />

                {/* Image Upload */}

                <input

                    type="file"

                    accept="image/*"

                    onChange={handleImageChange}

                />

                {

                    imagePreview && (

                        <img

                            src={imagePreview}

                            className="image-preview"

                            alt="Preview"

                        />

                    )

                }

                {/* Purchase Price */}

                <input

                    type="number"

                    placeholder="Purchase Price"

                    value={formData.purchase_price}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            purchase_price: e.target.value

                        })

                    }

                />

                {/* Selling Price */}

                <input

                    type="number"

                    placeholder="Selling Price"

                    value={formData.selling_price}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            selling_price: e.target.value

                        })

                    }

                />

                {/* GST */}

                <input

                    type="number"

                    placeholder="GST (%)"

                    value={formData.tax}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            tax: e.target.value

                        })

                    }

                />

                {/* Stock */}

                <input

                    type="number"

                    placeholder="Initial Stock"

                    value={formData.stock}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            stock: e.target.value

                        })

                    }

                />

                {/* Minimum Stock */}

                <input

                    type="number"

                    placeholder="Minimum Stock"

                    value={formData.minimum_stock}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            minimum_stock: e.target.value

                        })

                    }

                />

                {/* Unit */}

                <input

                    type="text"

                    placeholder="Unit (Kg, Box, Bottle...)"

                    value={formData.unit}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            unit: e.target.value

                        })

                    }

                />

                {/* Description */}

                <textarea

                    rows={4}

                    placeholder="Description"

                    value={formData.description}

                    onChange={(e) =>

                        setFormData({

                            ...formData,

                            description: e.target.value

                        })

                    }

                />

                {/* Status */}

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

                {/* Buttons */}

                <div className="modal-actions">

                    <button

                        className="cancel-btn"

                        onClick={() => {

                            setShowModal(false);

                            setEditId(null);

                        }}

                    >

                        Cancel

                    </button>

                    <button

                        className="save-btn"

                        onClick={createProduct}

                        disabled={loading}

                    >

                        {

                            loading

                                ?

                                "Saving..."

                                :

                                editId

                                    ?

                                    "Update Product"

                                    :

                                    "Save Product"

                        }

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