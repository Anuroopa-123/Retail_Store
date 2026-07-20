"use client";

import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";

import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { apiFetch } from "@/src/lib/api/client";

import "./stock-out.css";

// =========================================
// Interfaces
// =========================================

interface Product {

    id: number;

    product_name: string;

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

// =========================================
// Page
// =========================================

export default function StockOutPage() {

    const { user } = useAuth();

    // =========================================
    // Modal
    // =========================================

    const [showModal, setShowModal] =

        useState(false);

    // =========================================
    // Loading
    // =========================================

    const [loading, setLoading] =

        useState(false);

    // =========================================
    // Search
    // =========================================

    const [search, setSearch] =

        useState("");

    // =========================================
    // Products
    // =========================================

    const [products, setProducts] =

        useState<Product[]>([]);

    // =========================================
    // Movement History
    // =========================================

    const [movements, setMovements] =

        useState<StockMovement[]>([]);

    // =========================================
    // Selected Product
    // =========================================

    const [selectedProduct, setSelectedProduct] =

        useState<Product | null>(null);

    // =========================================
    // Form Data
    // =========================================

    const [formData, setFormData] =

        useState({

            product_id: "",

            quantity: "",

            reference: "",

            note: ""

        });

    // =========================================
    // Load Data
    // =========================================

    useEffect(() => {

        if (user) {

            getProducts();

            getStockMovements();

        }

    }, [user]);

    // =========================================
    // Get Products
    // =========================================

    const getProducts = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<Product[]>(

                `/api/v1/products/${user.tenant_id}/${user.store_id}`

            );

            setProducts(data);

        }

        catch (error: any) {

            console.log(error);

            toast.error("Unable to load products");

        }

    };

    // =========================================
    // Get Stock Movements
    // =========================================

    const getStockMovements = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<StockMovement[]>(

                `/api/v1/stock-movements/${user.tenant_id}/${user.store_id}`

            );

            setMovements(

                data.filter(

                    item =>

                        item.movement_type === "STOCK_OUT"

                )

            );

        }

        catch (error: any) {

            console.log(error);

            toast.error(

                "Unable to load movement history"

            );

        }

    };

  // =========================================
// Handle Product Change
// =========================================

const handleProductChange = (

    productId: string

) => {

    setFormData({

        ...formData,

        product_id: productId

    });

    const product = products.find(

        item =>

            item.id === Number(productId)

    );

    if (product) {

        setSelectedProduct(product);

    }

};

// =========================================
// Create Stock Out
// =========================================

const createStockOut = async () => {

    if (!user) return;

    if (!selectedProduct) {

        toast.error(

            "Please select a product"

        );

        return;

    }

    const quantity =

        Number(formData.quantity);

    // const previousQty =

    //     selectedProduct.stock;

    // ---------------------------------
    // Validation
    // ---------------------------------

    if (quantity <= 0) {

        toast.error(

            "Enter valid quantity"

        );

        return;

    }

   if (quantity > (selectedProduct?.stock ?? 0)) {

        toast.error(

            "Insufficient stock available"

        );

        return;

    }

    // const currentQty =

    //     previousQty - quantity;

    try {

        setLoading(true);

        // ---------------------------------
        // Save Stock Movement
        // ---------------------------------

        await apiFetch(

            "/api/v1/stock-movements/",

            {

                method: "POST",

              body: JSON.stringify({

    tenant_id: user.tenant_id,

    store_id: user.store_id,

    product_id: selectedProduct.id,

    movement_type: "STOCK_OUT",

    quantity,

    reference: formData.reference,

    note: formData.note,

    moved_by: user.id

})

            }

        );

        // ---------------------------------
        // Update Product Stock
        // ---------------------------------

        // await apiFetch(

        //     `/api/v1/products/${selectedProduct.id}`,

        //     {

        //         method: "PUT",

        //         body: JSON.stringify({

        //             stock: currentQty

        //         })

        //     }

        // );

        toast.success(

            "Stock Out Saved Successfully"

        );

        // ---------------------------------
        // Refresh Data
        // ---------------------------------

        getProducts();

        getStockMovements();

        // ---------------------------------
        // Reset Form
        // ---------------------------------

        setFormData({

            product_id: "",

            quantity: "",

            reference: "",

            note: ""

        });

        setSelectedProduct(null);

        setShowModal(false);

    }

    catch (error: any) {

        console.log(error);

        toast.error(

            error.message ||

            "Unable to save stock out"

        );

    }

    finally {

        setLoading(false);

    }

};

   return (

    <AdminLayout>

        <div className="stock-page">

            {/* ======================================= */}
            {/* Header */}
            {/* ======================================= */}

            <div className="stock-header">

                <h2>

                    Stock Out

                </h2>

                <button

                    className="add-btn"

                    onClick={() =>

                        setShowModal(true)

                    }

                >

                    + Stock Out

                </button>

            </div>

            {/* ======================================= */}
            {/* Search */}
            {/* ======================================= */}

            <div className="search-box">

                <input

                    type="text"

                    placeholder="Search Product..."

                    value={search}

                    onChange={(e) =>

                        setSearch(e.target.value)

                    }

                />

            </div>

            {/* ======================================= */}
            {/* Movement History */}
            {/* ======================================= */}

            <table className="stock-table">

                <thead>

                    <tr>

                        <th>Product</th>

                        <th>Previous</th>

                        <th>Out Qty</th>

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

                            const product =

                                products.find(

                                    p =>

                                        p.id === movement.product_id

                                );

                            return product?.product_name

                                ?.toLowerCase()

                                .includes(

                                    search.toLowerCase()

                                );

                        })

                        .map((movement) => {

                            const product =

                                products.find(

                                    p =>

                                        p.id === movement.product_id

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

                                        <span className="stock-out-badge">

                                            -

                                            {

                                                movement.quantity

                                            }

                                        </span>

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

                                            ).toLocaleString()

                                        }

                                    </td>

                                </tr>

                            );

                        })

                    }

                </tbody>

            </table>

            {/* ======================================= */}
            {/* Modal */}
            {/* ======================================= */}

            {

                showModal && (

                    <div className="modal-overlay">

                        <div className="modal">

                            <h3>

                                Stock Out

                            </h3>

                            {/* Product */}

                            <label>

                                Product

                            </label>

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

                                    <div className="current-stock">

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

                            <label>

                                Quantity

                            </label>

                            <input

                                type="number"

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

                            <label>

                                Reference

                            </label>

                            <input

                                type="text"

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

                            <label>

                                Remarks

                            </label>

                            <textarea

                                rows={4}

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

                            <div className="modal-buttons">

                                <button

                                    className="cancel-btn"

                                    onClick={() =>

                                        setShowModal(false)

                                    }

                                >

                                    Cancel

                                </button>

                                <button

                                    className="save-btn"

                                    disabled={loading}

                                    onClick={

                                        createStockOut

                                    }

                                >

                                    {

                                        loading

                                            ? "Saving..."

                                            : "Save"

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