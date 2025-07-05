import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EmployeeList = ({ onSelectEmployee }) => {
    const [employees, setEmployees] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [searchDept, setSearchDept] = useState('');

    // A placeholder for a real login flow
    const token = localStorage.getItem('token'); 

    const fetchEmployees = async () => {
        try {
            const response = await axios.get('/api/employees', {
                headers: { 'x-access-token': token },
                params: { name: searchTerm, department: searchDept },
            });
            setEmployees(response.data);
        } catch (error) {
            console.error('Error fetching employees:', error);
        }
    };

    useEffect(() => {
        if (token) {
            fetchEmployees();
        }
    }, [searchTerm, searchDept, token]);

    return (
        <div>
            <input
                type="text"
                placeholder="Search by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <input
                type="text"
                placeholder="Search by department..."
                value={searchDept}
                onChange={(e) => setSearchDept(e.target.value)}
            />
            <ul>
                {employees.map((employee) => (
                    <li key={employee.id} onClick={() => onSelectEmployee(employee)}>
                        {employee.name} - {employee.department}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default EmployeeList;