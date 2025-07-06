import React, { useContext } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { AuthContext } from "./AuthContext";
import Login from "./Login";
import Register from "./Register";
import EmployeeList from "./EmployeeList";
import EmployeeForm from "./EmployeeForm";

/* ----- Guards ---------------------------------------------------- */
const PrivateRoute = ({ children }) => {
  const { token } = useContext(AuthContext);
  return token ? children : <Navigate to="/" replace />;
};
const AuthWrapper = ({ children }) => {
  const { token } = useContext(AuthContext);
  return token ? <Navigate to="/employees" replace /> : children;
};

/* ----- Router ---------------------------------------------------- */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthWrapper><Login /></AuthWrapper>} />
        <Route path="/register" element={<AuthWrapper><Register /></AuthWrapper>} />

        <Route
          path="/employees"
          element={<PrivateRoute><EmployeeList /></PrivateRoute>}
        />
        <Route
          path="/employees/add"
          element={<PrivateRoute><EmployeeForm /></PrivateRoute>}
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
