"use client";

import { useEffect, useState } from "react";

import AdminLayout from "@/app/components/admin-layouts/AdminLayout";

import { useAuth } from "@/src/context/AuthContext";

import { apiFetch } from "@/src/lib/api/client";

import { toast } from "react-hot-toast";

import "./stock-in.css";

interface Product {

    id: number;

    product_name: string;

    sku: string;

    stock: number;

}

interface StockMovement {

    id: number;

    product_id: number;

    movement_type: string;

    quantity: number;

    previous_qty: number;

    current_qty: number;

    reference: string;

    note: string;

    created_at: string;

}

export default function StockInPage() {

    const { user } = useAuth();

    // ------------------------------------
    // Loading
    // ------------------------------------

    const [loading, setLoading] =
        useState(false);

    // ------------------------------------
    // Modal
    // ------------------------------------

    const [showModal, setShowModal] =
        useState(false);

    // ------------------------------------
    // Search
    // ------------------------------------

    const [search, setSearch] =
        useState("");

    // ------------------------------------
    // Products
    // ------------------------------------

    const [products, setProducts] =
        useState<Product[]>([]);

    // ------------------------------------
    // Stock Movements
    // ------------------------------------

    const [movements, setMovements] =
        useState<StockMovement[]>([]);

    // ------------------------------------
    // Selected Product
    // ------------------------------------

    const [selectedProduct, setSelectedProduct] =
        useState<Product | null>(null);

    // ------------------------------------
    // Form
    // ------------------------------------

    const [formData, setFormData] =
        useState({

            product_id: "",

            quantity: "",

            reference: "",

            note: ""

        });

    // ------------------------------------
    // Initial Load
    // ------------------------------------

    useEffect(() => {

        if (user) {

            getProducts();

            getStockMovements();

        }

    }, [user]);

    // ====================================
    // Get Products
    // ====================================

    const getProducts = async () => {

        if (!user) return;

        try {

            const data =
                await apiFetch<Product[]>(

                    `/api/v1/products/${user.tenant_id}/${user.store_id}`

                );

            setProducts(data);

        }

        catch (error) {

            console.log(error);

            toast.error(

                "Failed to Load Products"

            );

        }

    };

    // ====================================
    // Get Stock Movements
    // ====================================

    const getStockMovements = async () => {

        if (!user) return;

        try {

            const data =
                await apiFetch<StockMovement[]>(

                    `/api/v1/stock-movements/${user.tenant_id}/${user.store_id}`

                );

            setMovements(data);

        }

        catch (error) {

            console.log(error);

            toast.error(

                "Failed to Load Stock History"

            );

        }

    };
    // ====================================
// Handle Product Change
// ====================================

const handleProductChange = (

    productId: string

) => {

    setFormData({

        ...formData,

        product_id: productId

    });

    const product = products.find(

        (item) => item.id === Number(productId)

    );

    if (product) {

        setSelectedProduct(product);

    }

    else {

        setSelectedProduct(null);

    }

};


// ====================================
// Create Stock In
// ====================================

const createStockIn = async () => {

    if (!user) return;

    if (!formData.product_id) {

        toast.error(

            "Please Select Product"

        );

        return;

    }

    if (!formData.quantity) {

        toast.error(

            "Please Enter Quantity"

        );

        return;

    }

    setLoading(true);

    try {

       const quantity = Number(formData.quantity);

        await apiFetch(

            "/api/v1/stock-movements/",

            {

                method: "POST",

               body: JSON.stringify({

    tenant_id: user.tenant_id,

    store_id: user.store_id,

    product_id: Number(formData.product_id),

    movement_type: "STOCK_IN",

    quantity,

    reference: formData.reference,

    note: formData.note,

    moved_by: user.id

})

            }

        );

        toast.success(

            "Stock Added Successfully"

        );

        await getProducts();

        await getStockMovements();

        setShowModal(false);

        setSelectedProduct(null);

        setFormData({

            product_id: "",

            quantity: "",

            reference: "",

            note: ""

        });

    }

    catch (error: any) {

        toast.error(

            error.message ||

            "Failed to Add Stock"

        );

    }

    finally {

        setLoading(false);

    }

};

return (

    <AdminLayout>

        <div className="inventory-container">

            {/* Header */}

            <div className="inventory-header">

                <h1>

                    Stock In

                </h1>

                <button

                    className="add-btn"

                    onClick={() =>

                        setShowModal(true)

                    }

                >

                    + Stock In

                </button>

            </div>

            {/* Search */}

            <input

                className="search-box"

                placeholder="Search Product..."

                value={search}

                onChange={(e) =>

                    setSearch(e.target.value)

                }

            />

            {/* Movement History */}

            <div className="table-wrapper">

                <table>

                    <thead>

                        <tr>

                            <th>Product</th>

                            <th>Previous</th>

                            <th>Quantity</th>

                            <th>Current</th>

                            <th>Reference</th>

                            <th>Remarks</th>

                            <th>Date</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            movements

                                .filter((movement) => {

                                    const product = products.find(

                                        (p) =>

                                            p.id ===

                                            movement.product_id

                                    );

                                    return (

                                        product?.product_name

                                            .toLowerCase()

                                            .includes(

                                                search.toLowerCase()

                                            ) ?? false

                                    );

                                })

                                .map((movement) => {

                                    const product = products.find(

                                        (p) =>

                                            p.id ===

                                            movement.product_id

                                    );

                                    return (

                                        <tr

                                            key={movement.id}

                                        >

                                            <td>

                                                {

                                                    product?.product_name

                                                }

                                            </td>

                                            <td>

                                                {

                                                    movement.previous_qty

                                                }

                                            </td>

                                            <td>

                                                +{

                                                    movement.quantity

                                                }

                                            </td>

                                            <td>

                                                {

                                                    movement.current_qty

                                                }

                                            </td>

                                            <td>

                                                {

                                                    movement.reference

                                                }

                                            </td>

                                            <td>

                                                {

                                                    movement.note

                                                }

                                            </td>

                                            <td>

                                                {

                                                    new Date(

                                                        movement.created_at

                                                    ).toLocaleDateString()

                                                }

                                            </td>

                                        </tr>

                                    );

                                })

                        }

                    </tbody>

                </table>

            </div>

            {/* Modal */}

            {

                showModal && (

                    <div className="modal-overlay">

                        <div className="inventory-modal">

                            <h2>

                                Stock In

                            </h2>

                            {/* Product */}

                            <select

                                value={

                                    formData.product_id

                                }

                                onChange={(e) =>

                                    handleProductChange(

                                        e.target.value

                                    )

                                }

                            >

                                <option value="">

                                    Select Product

                                </option>

                                {

                                    products.map(

                                        (product) => (

                                            <option

                                                key={

                                                    product.id

                                                }

                                                value={

                                                    product.id

                                                }

                                            >

                                                {

                                                    product.product_name

                                                }

                                            </option>

                                        )

                                    )

                                }

                            </select>

                            {/* Current Stock */}

                            {

                                selectedProduct && (

                                    <div

                                        className="current-stock"

                                    >

                                        Current Stock :

                                        <strong>

                                            {

                                                selectedProduct.stock

                                            }

                                        </strong>

                                    </div>

                                )

                            }

                            {/* Quantity */}

                            <input

                                type="number"

                                placeholder="Quantity"

                                value={

                                    formData.quantity

                                }

                                onChange={(e) =>

                                    setFormData({

                                        ...formData,

                                        quantity:

                                            e.target.value

                                    })

                                }

                            />

                            {/* Reference */}

                            <input

                                placeholder="Reference"

                                value={

                                    formData.reference

                                }

                                onChange={(e) =>

                                    setFormData({

                                        ...formData,

                                        reference:

                                            e.target.value

                                    })

                                }

                            />

                            {/* Remarks */}

                            <textarea

                                rows={4}

                                placeholder="Remarks"

                                value={

                                    formData.note

                                }

                                onChange={(e) =>

                                    setFormData({

                                        ...formData,

                                        note:

                                            e.target.value

                                    })

                                }

                            />

                            {/* Buttons */}

                            <div

                                className="modal-actions"

                            >

                                <button

                                    onClick={() =>

                                        setShowModal(

                                            false

                                        )

                                    }

                                >

                                    Cancel

                                </button>

                                <button

                                    disabled={

                                        loading

                                    }

                                    onClick={

                                        createStockIn

                                    }

                                >

                                    {

                                        loading

                                            ? "Saving..."

                                            : "Save Stock"

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