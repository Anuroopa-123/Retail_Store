"use client";

import Link from "next/link";

import AdminLayout from "@/app/components/admin-layouts/AdminLayout";

import {

    FaArrowDown,

    FaArrowUp,

    FaExchangeAlt,

    FaTruck,

    FaExclamationTriangle,

    FaChartBar

} from "react-icons/fa";

import "./inventory.css";

export default function InventoryPage() {

    const menus = [

        {

            title: "Stock In",

            icon: <FaArrowDown />,

            path: "/admin/inventory/stock-in",

            color: "#16a34a"

        },

        {

            title: "Stock Out",

            icon: <FaArrowUp />,

            path: "/admin/inventory/stock-out",

            color: "#dc2626"

        },

        {

            title: "Adjustment",

            icon: <FaExchangeAlt />,

            path: "/admin/inventory/adjustment",

            color: "#2563eb"

        },

        {

            title: "Transfer",

            icon: <FaTruck />,

            path: "/admin/inventory/transfer",

            color: "#7c3aed"

        },

        {

            title: "Low Stock",

            icon: <FaExclamationTriangle />,

            path: "/admin/inventory/low-stock",

            color: "#ea580c"

        },

        {

            title: "Inventory Report",

            icon: <FaChartBar />,

            path: "/admin/inventory/report",

            color: "#0f766e"

        }

    ];

    return (

        <AdminLayout>

            <div className="inventory-dashboard">

                <div className="inventory-title">

                    <h1>

                        Inventory Management

                    </h1>

                    <p>

                        Manage your inventory operations from one place.

                    </p>

                </div>

                <div className="inventory-grid">

                    {

                        menus.map((menu) => (

                            <Link

                                key={menu.path}

                                href={menu.path}

                                className="inventory-card"

                            >

                                <div

                                    className="inventory-icon"

                                    style={{

                                        background: menu.color

                                    }}

                                >

                                    {menu.icon}

                                </div>

                                <h3>

                                    {menu.title}

                                </h3>

                            </Link>

                        ))

                    }

                </div>

            </div>

        </AdminLayout>

    );

}