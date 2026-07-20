"use client";

import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";

import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { apiFetch } from "@/src/lib/api/client";

import "./adjustment.css";

// =========================================
// Interfaces
// =========================================

// interface Product {

//     id: number;

//     product_name: string;

//     stock: number;

// }

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
// Adjustment Page
// =========================================

export default function AdjustmentPage() {

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
    // Adjustment History
    // =========================================

    const [adjustments, setAdjustments] =

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

            physical_stock: "",

            difference: "",

            reference: "",

            note: ""

        });

    // =========================================
    // Load Data
    // =========================================

    useEffect(() => {

        if (user) {

            getProducts();

            getAdjustmentHistory();

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

            toast.error(

                "Unable to load products"

            );

        }

    };

    // =========================================
    // Get Adjustment History
    // =========================================

    const getAdjustmentHistory = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<StockMovement[]>(

                `/api/v1/stock-movements/${user.tenant_id}/${user.store_id}`

            );

            setAdjustments(

                data.filter(

                    item =>

                        item.movement_type === "ADJUSTMENT"

                )

            );

        }

        catch (error: any) {

            console.log(error);

            toast.error(

                "Unable to load adjustment history"

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

        product_id: productId,

        physical_stock: "",

        difference: ""

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
// Physical Stock Change
// =========================================

const handlePhysicalStockChange = (

    value: string

) => {

    if (!selectedProduct) return;

    const physicalStock =

        Number(value);

    const difference =

        physicalStock -

        selectedProduct.stock;

    setFormData({

        ...formData,

        physical_stock: value,

        difference:

            difference.toString()

    });

};

// =========================================
// Create Adjustment
// =========================================

const createAdjustment = async () => {

    if (!user) return;

    if (!selectedProduct) {

        toast.error(

            "Please select a product"

        );

        return;

    }

    const physicalStock =

        Number(formData.physical_stock);

    const previousQty =

        selectedProduct.stock;

    const currentQty =

        physicalStock;

    const difference =

        currentQty - previousQty;

    if (physicalStock < 0) {

        toast.error(

            "Invalid stock quantity"

        );

        return;

    }

    try {

        setLoading(true);

        // ---------------------------------------
        // Save Stock Movement
        // ---------------------------------------

        await apiFetch(

            "/api/v1/stock-movements/",

            {

                method: "POST",

                body: JSON.stringify({

                    tenant_id:

                        user.tenant_id,

                    store_id:

                        user.store_id,

                    product_id:

                        selectedProduct.id,

                    movement_type:

                        "ADJUSTMENT",

                    quantity:

                        Math.abs(

                            difference

                        ),

                    current_qty:

                        currentQty,

                    reference:

                        formData.reference,

                    note:

                        formData.note,

                    moved_by:

                        user.id

                })

            }

        );

        // ---------------------------------------
        // Update Product Stock
        // ---------------------------------------

        // await apiFetch(

        //     `/api/v1/products/${selectedProduct.id}`,

        //     {

        //         method: "PUT",

        //         body: JSON.stringify({

        //             stock:

        //                 currentQty

        //         })

        //     }

        // );

        toast.success(

            "Stock Adjusted Successfully"

        );

        // ---------------------------------------
        // Reload
        // ---------------------------------------

        getProducts();

        getAdjustmentHistory();

        // ---------------------------------------
        // Reset
        // ---------------------------------------

        setFormData({

            product_id: "",

            physical_stock: "",

            difference: "",

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

            "Unable to save adjustment"

        );

    }

    finally {

        setLoading(false);

    }

};

   return (

    <AdminLayout>

        <div className="stock-page">

            {/* ===================================== */}
            {/* Header */}
            {/* ===================================== */}

            <div className="stock-header">

                <h2>

                    Stock Adjustment

                </h2>

                <button

                    className="add-btn"

                    onClick={() =>

                        setShowModal(true)

                    }

                >

                    + New Adjustment

                </button>

            </div>

            {/* ===================================== */}
            {/* Search */}
            {/* ===================================== */}

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

            {/* ===================================== */}
            {/* History Table */}
            {/* ===================================== */}

            <table className="stock-table">

                <thead>

                    <tr>

                        <th>

                            Product

                        </th>

                        <th>

                            Previous

                        </th>

                        <th>

                            Current

                        </th>

                        <th>

                            Difference

                        </th>

                        <th>

                            Reference

                        </th>

                        <th>

                            Remarks

                        </th>

                        <th>

                            Date

                        </th>

                    </tr>

                </thead>

                <tbody>

                    {

                        adjustments

                        .filter((item) => {

                            const product =

                                products.find(

                                    p =>

                                        p.id ===

                                        item.product_id

                                );

                            return product?.product_name

                                ?.toLowerCase()

                                .includes(

                                    search.toLowerCase()

                                );

                        })

                        .map((item) => {

                            const product =

                                products.find(

                                    p =>

                                        p.id ===

                                        item.product_id

                                );

                            const difference =

                                item.current_qty -

                                item.previous_qty;

                            return (

                                <tr

                                    key={item.id}

                                >

                                    <td>

                                        {

                                            product?.product_name

                                        }

                                    </td>

                                    <td>

                                        {

                                            item.previous_qty

                                        }

                                    </td>

                                    <td>

                                        {

                                            item.current_qty

                                        }

                                    </td>

                                    <td>

                                        <span

                                            className={

                                                difference >= 0

                                                ?

                                                "increase-badge"

                                                :

                                                "decrease-badge"

                                            }

                                        >

                                            {

                                                difference > 0

                                                ?

                                                `+${difference}`

                                                :

                                                difference

                                            }

                                        </span>

                                    </td>

                                    <td>

                                        {

                                            item.reference

                                        }

                                    </td>

                                    <td>

                                        {

                                            item.note

                                        }

                                    </td>

                                    <td>

                                        {

                                            new Date(

                                                item.created_at

                                            )

                                            .toLocaleString()

                                        }

                                    </td>

                                </tr>

                            );

                        })

                    }

                </tbody>

            </table>

            {/* ===================================== */}
            {/* Modal */}
            {/* ===================================== */}

            {

                showModal && (

                    <div className="modal-overlay">

                        <div className="modal">

                            <h3>

                                Stock Adjustment

                            </h3>

                            {/* Product */}

                            <label>

                                Product

                            </label>

                            <select

                                value={

                                    formData.product_id

                                }

                                onChange={(e)=>

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

                                        (product)=>(

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

                            {/* Physical Stock */}

                            <label>

                                Physical Stock

                            </label>

                            <input

                                type="number"

                                value={

                                    formData.physical_stock

                                }

                                onChange={(e)=>

                                    handlePhysicalStockChange(

                                        e.target.value

                                    )

                                }

                            />

                            {/* Difference */}

                            {

                                formData.difference !== "" && (

                                    <div className="difference-box">

                                        Difference :

                                        <strong>

                                            {

                                                Number(

                                                    formData.difference

                                                ) > 0

                                                ?

                                                ` +${formData.difference}`

                                                :

                                                ` ${formData.difference}`

                                            }

                                        </strong>

                                    </div>

                                )

                            }

                            {/* Reference */}

                            <label>

                                Reference

                            </label>

                            <input

                                type="text"

                                value={

                                    formData.reference

                                }

                                onChange={(e)=>

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

                                onChange={(e)=>

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

                                    onClick={()=>

                                        setShowModal(false)

                                    }

                                >

                                    Cancel

                                </button>

                                <button

                                    className="save-btn"

                                    disabled={loading}

                                    onClick={

                                        createAdjustment

                                    }

                                >

                                    {

                                        loading

                                        ?

                                        "Saving..."

                                        :

                                        "Save"

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