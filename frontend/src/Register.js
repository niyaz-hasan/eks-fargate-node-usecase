import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import React, { useState, useContext } from "react";


export default function Register() {
    const { register, login } = useContext(AuthContext);
    const nav = useNavigate();

    const [form, set] = useState({ username: "", password: "" });
    const [err, setErr] = useState("");

    const handle = (e) => set({ ...form, [e.target.name]: e.target.value });

    const submit = async (e) => {
        e.preventDefault();
        const ok = await register(form.username, form.password);
        if (!ok) return setErr("User already exists");

        /* auto-login, then go to the list */
        await login(form.username, form.password);
        nav("/employees");
    };

    return (
        <form onSubmit={submit} style={{ marginTop: 50 }}>
            {err && <p style={{ color: "red" }}>{err}</p>}

            <input
                name="username"
                placeholder="Username"
                onChange={handle}
                required
            />
            <input
                name="password"
                type="password"
                placeholder="Password"
                onChange={handle}
                required
            />
            <button>Register</button>{" "}
            <Link to="/">Back to login</Link>
        </form>
    );
}
