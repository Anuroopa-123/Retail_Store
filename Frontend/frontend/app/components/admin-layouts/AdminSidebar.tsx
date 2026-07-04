"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  FaTachometerAlt,
  FaUsers,
  FaClipboardCheck,
  FaMoneyCheckAlt,
  FaBoxOpen,
  FaUserFriends,
  FaChartBar
} from "react-icons/fa";

export default function AdminSidebar() {

  const pathname = usePathname();

  const menus = [
    {
      name: "Dashboard",
      icon: <FaTachometerAlt />,
      path: "/admin/dashboard"
    },
    {
  name: "Departments",
  icon: <FaUsers />,
  path: "/admin/departments"
},
    {
      name: "Employees",
      icon: <FaUsers />,
      path: "/admin/employees"
    },
    {
      name: "Attendance",
      icon: <FaClipboardCheck />,
      path: "/admin/attendance"
    },
      {
      name: "Inventory",
      icon: <FaClipboardCheck />,
      path: "/admin/inventory"
    },
    {
      name: "Payroll",
      icon: <FaMoneyCheckAlt />,
      path: "/admin/payroll"
    },
    {
      name: "Products-Categories",
      icon: <FaBoxOpen />,
      path: "/admin/product-categories"
    },
      {
      name: "Brands",
      icon: <FaUserFriends />,
      path: "/admin/brands"
    },
     {
      name: "Products",
      icon: <FaBoxOpen />,
      path: "/admin/product"
    },
    {
      name: "Customers",
      icon: <FaUserFriends />,
      path: "/admin/customers"
    },
    {
      name: "Billing",
      icon: <FaChartBar />,
      path: "/admin/billing"
    },
    {
name:"Profile",
icon:<FaUserFriends/>,
path:"/admin/admin-profile"
}
  ];

  return (
    <aside className="admin-sidebar">

      <div className="sidebar-logo">
        Retail Admin
      </div>

      {menus.map((menu) => (

        <Link
          key={menu.path}
          href={menu.path}
          className={
            pathname === menu.path
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >
          {menu.icon}
          <span>{menu.name}</span>
        </Link>

      ))}

    </aside>
  );
}