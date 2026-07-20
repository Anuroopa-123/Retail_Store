"use client";

import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";

import AdminLayout from "@/app/components/admin-layouts/AdminLayout";
import { useAuth } from "@/src/context/AuthContext";
import { apiFetch } from "@/src/lib/api/client";

import "./transfer.css";

// =========================================
// Interfaces
// =========================================

interface Store {

    id: number;

    store_name: string;

}

interface Product {

    id: number;

    product_name: string;

    stock: number;

}

interface StockMovement {

    id: number;

    product_id: number;

    store_id: number;

    destination_store_id?: number;

    movement_type: string;

    quantity: number;

    previous_qty: number;

    current_qty: number;

    reference: string;

    note: string;

    created_at: string;

}

// =========================================
// Transfer Page
// =========================================

export default function TransferPage() {

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
    // Stores
    // =========================================

    const [stores, setStores] =

        useState<Store[]>([]);

    // =========================================
    // Products
    // =========================================

    const [products, setProducts] =

        useState<Product[]>([]);

    // =========================================
    // Transfer History
    // =========================================

    const [transfers, setTransfers] =

        useState<StockMovement[]>([]);

    // =========================================
    // Selected Product
    // =========================================

    const [selectedProduct, setSelectedProduct] =

        useState<Product | null>(null);

    // =========================================
    // Form
    // =========================================

    const [formData, setFormData] =

        useState({

            source_store: "",

            destination_store: "",

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

            getStores();

            getProducts();

            getTransferHistory();

        }

    }, [user]);

    // =========================================
    // Get Stores
    // =========================================

    const getStores = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<Store[]>(

                `/api/v1/stores/${user.tenant_id}`

            );

            setStores(data);

        }

        catch (error: any) {

            console.log(error);

            toast.error(

                "Unable to load stores"

            );

        }

    };

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
    // Get Transfer History
    // =========================================

    const getTransferHistory = async () => {

        if (!user) return;

        try {

            const data = await apiFetch<StockMovement[]>(

                `/api/v1/stock-movements/${user.tenant_id}/${user.store_id}`

            );

            setTransfers(

                data.filter(

                    item =>

                        item.movement_type === "TRANSFER"

                )

            );

        }

        catch (error: any) {

            console.log(error);

            toast.error(

                "Unable to load transfer history"

            );

        }

    };
    // =========================================
// Handle Source Store Change
// =========================================

const handleSourceStoreChange = async (

    storeId: string

) => {

    setFormData({

        ...formData,

        source_store: storeId,

        product_id: ""

    });

    setSelectedProduct(null);

    if (!user || !storeId) return;

    try {

        const data = await apiFetch<Product[]>(

            `/api/v1/products/${user.tenant_id}/${storeId}`

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
// Handle Destination Store Change
// =========================================

const handleDestinationStoreChange = (

    storeId: string

) => {

    setFormData({

        ...formData,

        destination_store: storeId

    });

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

    setSelectedProduct(

        product || null

    );

};

// =========================================
// Create Transfer
// =========================================

const createTransfer = async () => {

    if (!user) return;

    if (

        !formData.source_store ||

        !formData.destination_store ||

        !formData.product_id

    ) {

        toast.error(

            "Please complete all required fields"

        );

        return;

    }

    if (

        formData.source_store ===

        formData.destination_store

    ) {

        toast.error(

            "Source and Destination stores cannot be the same"

        );

        return;

    }

    if (!selectedProduct) {

        toast.error(

            "Please select a product"

        );

        return;

    }

    const quantity =

        Number(formData.quantity);

    if (

        quantity <= 0

    ) {

        toast.error(

            "Enter valid quantity"

        );

        return;

    }

    if (

        quantity >

        selectedProduct.stock

    ) {

        toast.error(

            "Insufficient Stock"

        );

        return;

    }

    try {

        setLoading(true);

        await apiFetch(

            "/api/v1/stock-movements/",

            {

                method: "POST",

                body: JSON.stringify({

                    tenant_id:

                        user.tenant_id,

                    store_id:

                        Number(

                            formData.source_store

                        ),

                    destination_store_id:

                        Number(

                            formData.destination_store

                        ),

                    product_id:

                        Number(

                            formData.product_id

                        ),

                    movement_type:

                        "TRANSFER",

                    quantity,

                    reference:

                        formData.reference,

                    note:

                        formData.note,

                    moved_by:

                        user.id

                })

            }

        );

        toast.success(

            "Stock transferred successfully"

        );

        getTransferHistory();

        if (user) {

            const products = await apiFetch<Product[]>(

                `/api/v1/products/${user.tenant_id}/${formData.source_store}`

            );

            setProducts(products);

        }

        setFormData({

            source_store: "",

            destination_store: "",

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

            "Unable to transfer stock"

        );

    }

    finally {

        setLoading(false);

    }

};
    // =========================================
    // Filter Transfer History
    // =========================================

    const filteredTransfers = transfers.filter((item) => {

        const keyword = search.toLowerCase();

        return (
            item.reference?.toLowerCase().includes(keyword) ||
            item.note?.toLowerCase().includes(keyword) ||
            item.movement_type.toLowerCase().includes(keyword)
        );

    });

    // =========================================
    // UI
    // =========================================

    return (

        <AdminLayout>

            <div className="transfer-page">

                {/* ================= Header ================= */}

                <div className="transfer-header">

                    <div>

                        <h2>Stock Transfer</h2>

                        <p>

                            Transfer products between stores.

                        </p>

                    </div>

                    <button

                        className="primary-btn"

                        onClick={() => setShowModal(true)}

                    >

                        + New Transfer

                    </button>

                </div>

                {/* ================= Search ================= */}

                <div className="transfer-toolbar">

                    <input

                        type="text"

                        placeholder="Search Transfer..."

                        value={search}

                        onChange={(e) =>

                            setSearch(e.target.value)

                        }

                        className="search-input"

                    />

                </div>

                {/* ================= Table ================= */}

                <div className="table-wrapper">

                    <table className="transfer-table">

                        <thead>

                            <tr>

                                <th>ID</th>

                                <th>Product</th>

                                <th>From Store</th>

                                <th>To Store</th>

                                <th>Quantity</th>

                                <th>Reference</th>

                                <th>Remarks</th>

                                <th>Date</th>

                            </tr>

                        </thead>

                        <tbody>

                            {filteredTransfers.length === 0 ? (

                                <tr>

                                    <td

                                        colSpan={8}

                                        className="no-data"

                                    >

                                        No Transfer History Found

                                    </td>

                                </tr>

                            ) : (

                                filteredTransfers.map((item) => (

                                    <tr key={item.id}>

                                        <td>

                                            {item.id}

                                        </td>

                                        <td>

                                            {

                                                products.find(

                                                    p =>

                                                        p.id === item.product_id

                                                )?.product_name ||

                                                item.product_id

                                            }

                                        </td>

                                        <td>

                                            {

                                                stores.find(

                                                    s =>

                                                        s.id === item.store_id

                                                )?.store_name ||

                                                item.store_id

                                            }

                                        </td>

                                        <td>

                                            {

                                                stores.find(

                                                    s =>

                                                        s.id === item.destination_store_id

                                                )?.store_name ||

                                                "-"

                                            }

                                        </td>

                                        <td>

                                            {item.quantity}

                                        </td>

                                        <td>

                                            {item.reference || "-"}

                                        </td>

                                        <td>

                                            {item.note || "-"}

                                        </td>

                                        <td>

                                            {

                                                new Date(

                                                    item.created_at

                                                ).toLocaleDateString()

                                            }

                                        </td>

                                    </tr>

                                ))

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

        </AdminLayout>

    );

}