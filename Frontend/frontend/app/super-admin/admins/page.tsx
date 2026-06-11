"use client";

import { useEffect, useState, useRef } from "react";
import Layout from "@/app/components/layout/Layout";
import "./admins.css";
import toast from "react-hot-toast";
import { FaEye, FaEyeSlash } from "react-icons/fa";

interface Tenant { id: number; name: string; }
interface Store  { id: number; name: string; }
interface Admin  { id: number; name: string; email: string; status: string; }

/* ─── Custom Dropdown ─── */
interface DropdownProps {
  options: { id: number; name: string }[];
  value: string;
  onChange: (val: string) => void;
  placeholder: string;
  icon: string;
}

function CustomDropdown({ options, value, onChange, placeholder, icon }: DropdownProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const selected = options.find((o) => String(o.id) === value);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div className={`custom-select ${open ? "open" : ""}`} ref={ref}>
      {/* Trigger */}
      <button
        type="button"
        className="custom-select__trigger"
        onClick={() => setOpen((o) => !o)}
      >
        <span className="custom-select__icon">{icon}</span>
        <span className={`custom-select__value ${!selected ? "placeholder" : ""}`}>
          {selected ? selected.name : placeholder}
        </span>
        <span className="custom-select__arrow">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </span>
      </button>

      {/* Dropdown panel */}
      <div className="custom-select__panel">
        <div className="custom-select__panel-inner">
          {/* Search inside dropdown */}
          <div className="custom-select__search-wrap">
            <span className="custom-select__search-icon">🔍</span>
            <SearchableList
              options={options}
              selected={value}
              onSelect={(id) => { onChange(id); setOpen(false); }}
              placeholder={placeholder}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function SearchableList({
  options, selected, onSelect, placeholder,
}: {
  options: { id: number; name: string }[];
  selected: string;
  onSelect: (id: string) => void;
  placeholder: string;
}) {
  const [query, setQuery] = useState("");
  const filtered = options.filter((o) =>
    o.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <>
      <input
        className="custom-select__search"
        placeholder={`Search ${placeholder.replace("Select ", "")}…`}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoFocus
      />
      <ul className="custom-select__list">
        {filtered.length === 0 ? (
          <li className="custom-select__empty">No results found</li>
        ) : (
          filtered.map((o, i) => (
            <li
              key={o.id}
              className={`custom-select__item ${String(o.id) === selected ? "active" : ""}`}
              style={{ animationDelay: `${i * 30}ms` }}
              onClick={() => onSelect(String(o.id))}
            >
              <span className="item-dot" />
              {o.name}
              {String(o.id) === selected && <span className="item-check">✓</span>}
            </li>
          ))
        )}
      </ul>
    </>
  );
}

/* ─── Main Page ─── */
export default function AdminPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [stores,  setStores]  = useState<Store[]>([]);
  const [admins,  setAdmins]  = useState<Admin[]>([]);
  const [tenantId, setTenantId] = useState("");
  const [storeId,  setStoreId]  = useState("");
  const [name,     setName]     = useState("");
  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const loadAdmins = async () => {
    try {
      const r = await fetch("http://127.0.0.1:8000/api/v1/admins/");
      const d = await r.json();
      setAdmins(Array.isArray(d) ? d : []);
    } catch { setAdmins([]); }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const [tr, sr] = await Promise.all([
          fetch("http://127.0.0.1:8000/api/v1/tenants/"),
          fetch("http://127.0.0.1:8000/api/v1/stores/"),
        ]);
        const [td, sd] = await Promise.all([tr.json(), sr.json()]);
        setTenants(Array.isArray(td) ? td : []);
        setStores(Array.isArray(sd) ? sd : []);
        await loadAdmins();
      } catch (e) { console.error(e); }
    };
    init();
  }, []);

  const createAdmin = async () => {
    if (!tenantId || !name || !email || !password) {
      toast.error("Please fill all fields");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/admins/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tenant_id: Number(tenantId),
          store_id:  Number(storeId),
          name, email, password,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        toast.error(err.detail || "Failed to create admin");
        return;
      }
      toast.success("Admin created successfully!");
      setTenantId(""); setStoreId(""); setName(""); setEmail(""); setPassword("");
      await loadAdmins();
    } catch { toast.error("Something went wrong"); }
    finally { setLoading(false); }
  };

  return (
    <Layout title="Admin Management">
        <div className="admin-page">
      <div className="page-header">
        <div className="page-header-left">
          <h1>Tenant Admins</h1>
          <p>{admins.length} admin{admins.length !== 1 ? "s" : ""} across your network</p>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-tile" data-icon="👤">
          <span className="tile-value">{admins.length}</span>
          <span className="tile-label">Total Admins</span>
        </div>
        <div className="stat-tile" data-icon="✅">
          <span className="tile-value">{admins.filter(a => a.status === "active").length}</span>
          <span className="tile-label">Active</span>
          <span className="tile-change up">↑ Online</span>
        </div>
        <div className="stat-tile" data-icon="⏳">
          <span className="tile-value">{admins.filter(a => a.status === "pending").length}</span>
          <span className="tile-label">Pending</span>
        </div>
      </div>

      {/* Form card */}
      <div className="admin-form-card">
        <div className="admin-form-header">
          <span className="admin-form-title">Create New Admin</span>
          <span className="admin-form-sub">Assign an admin to a tenant and store</span>
        </div>

        <div className="admin-form-body">
          <div className="form-row">
            {/* Tenant dropdown */}
            <div className="field-group">
              <label>Tenant</label>
              <CustomDropdown
                options={tenants}
                value={tenantId}
                onChange={setTenantId}
                placeholder="Select Tenant"
                icon="🏢"
              />
            </div>

            {/* Store dropdown */}
            <div className="field-group">
              <label>Store</label>
              <CustomDropdown
                options={stores}
                value={storeId}
                onChange={setStoreId}
                placeholder="Select Store"
                icon="🏪"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="field-group">
              <label>Full Name</label>
              <div className="input-with-icon">
                <span className="input-prefix">👤</span>
                <input
                  placeholder="e.g. Priya Sharma"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </div>

            <div className="field-group">
              <label>Email Address</label>
              <div className="input-with-icon">
                <span className="input-prefix">✉️</span>
                <input
                  type="email"
                  placeholder="admin@store.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="form-row form-row--half">
            <div className="field-group">
              <label>Password</label>
              <div className="input-with-icon password-wrap">
                <span className="input-prefix">🔒</span>
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="eye-toggle"
                  onClick={() => setShowPassword((s) => !s)}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
            </div>
          </div>

          <div className="admin-form-footer">
            <button
              className="btn-secondary"
              onClick={() => { setTenantId(""); setStoreId(""); setName(""); setEmail(""); setPassword(""); }}
            >
              Reset
            </button>
            <button className="btn-primary" onClick={createAdmin} disabled={loading}>
              {loading ? "Creating…" : "Create Admin →"}
            </button>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {admins.length === 0 ? (
              <tr>
                <td colSpan={4}>
                  <div className="empty-state">
                    <span className="empty-icon">👥</span>
                    <span className="empty-text">No admins yet. Create your first one above!</span>
                  </div>
                </td>
              </tr>
            ) : (
              admins.map((admin, i) => (
                <tr key={admin.id}>
                  <td style={{ color: "var(--muted)" }}>{i + 1}</td>
                  <td style={{ color: "var(--ivory)", fontWeight: 500 }}>{admin.name}</td>
                  <td>{admin.email}</td>
                  <td>
                    <span className={`badge badge-${admin.status === "active" ? "active" : admin.status === "pending" ? "pending" : "inactive"}`}>
                      {admin.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      </div>
    </Layout>
    
  );
}