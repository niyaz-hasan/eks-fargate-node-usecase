import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";

export default function Login() {
    const nav = useNavigate();
    const { login } = useContext(AuthContext);

    const [username, setUser] = useState("");
    const [password, setPass] = useState("");
    const [err, setErr] = useState("");

    async function submit(e) {
        e.preventDefault();
        const ok = await login(username, password);
        if (ok) nav("/employees");
        else setErr("Invalid credentials");
    }

    return (
        <>
            <form onSubmit={submit} style={{ marginTop: 50 }}>
                {err && <p style={{ color: "red" }}>{err}</p>}

                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUser(e.target.value)}
                    required
                />
                <input
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPass(e.target.value)}
                    required
                />
                <button>Log in</button>
            </form>

            {/* ↓↓↓  the missing part  ↓↓↓ */}
            <p style={{ marginTop: 10 }}>
                New user? <Link to="/register">Create an account</Link>
            </p>
        </>
    );
}
