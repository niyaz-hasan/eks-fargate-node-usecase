import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import EmployeeList from './EmployeeList';
import EmployeeForm from './EmployeeForm';
import Navbar from './Navbar';
import { searchEmployees, updateEmployee } from './api';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

function App() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchEmployees();
  }, [searchTerm]);

  const fetchEmployees = async () => {
    setLoading(true);
    try {
      const data = await searchEmployees(searchTerm);
      setEmployees(data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateEmployee = async (id, updatedData) => {
    try {
      await updateEmployee(id, updatedData);
      fetchEmployees();
    } catch (error) {
      console.error('Error updating employee:', error);
    }
  };

  return (
    <Router>
      <Navbar />
      <Container>
        <ToastContainer position="top-right" autoClose={3000} />
        <Routes>
          <Route
            path="/"
            element={
              <EmployeeList
                employees={employees}
                loading={loading}
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
              />
            }
          />
          <Route
            path="/edit/:id"
            element={
              <EmployeeForm
                employees={employees}
                onUpdate={handleUpdateEmployee}
              />
            }
          />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;