
import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { Link } from "react-router-dom";

export default function EmployeeList() {
  const { authFetch, logout } = useContext(AuthContext);
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const load = (q = "") => {
    setLoading(true);
    const qs = q ? `?search=${encodeURIComponent(q)}` : "";
    authFetch(`/api/employees${qs}`)
      .then(async res => {
        if (res.status === 401) {
          logout();
          return [];
        }
        if (!res.ok) return [];
        try { return await res.json(); } catch { return []; }
      })
      .then(data => { setEmployees(data); setLoading(false); });
  };

  useEffect(() => { load(); }, []); // initial load

  return (
    <div style={{ marginTop: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Employees</h2>
        <button onClick={logout}>Logout</button>
      </div>

      {/* Search */}
      <form onSubmit={e => { e.preventDefault(); load(search); }}>
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search" />
        <button>Search</button>
        <Link to="/employees/add" style={{ marginLeft: 10 }}>+ Add employee</Link>
      </form>

      {/* Results */}
      {loading ? <p>Loading…</p> : employees.length === 0 ?
        <p>No employees found.</p> :
        <table style={{ marginTop: 10 }}>
          <thead><tr><th>Name</th><th>Department</th></tr></thead>
          <tbody>
            {employees.map(e => <tr key={e.id}><td>{e.name}</td><td>{e.department}</td></tr>)}
          </tbody>
        </table>
      }
    </div>
  );
}
