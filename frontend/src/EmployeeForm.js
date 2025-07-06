
import React, { useState, useContext } from "react";
import { AuthContext } from "./AuthContext";
import { useNavigate } from "react-router-dom";

export default function EmployeeForm() {
  const { authFetch } = useContext(AuthContext);
  const nav = useNavigate();
  const [name, setName] = useState("");
  const [department, setDept] = useState("");
  const [err, setErr] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setErr("");
    const res = await authFetch("/api/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, department })
    });
    if (!res.ok) {
      setErr("Failed to add employee");
      return;
    }
    nav("/employees");  // back to list
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" required />
      <input value={department} onChange={e => setDept(e.target.value)} placeholder="Department" required />
      <button>Add</button>
    </form>
  );
}
