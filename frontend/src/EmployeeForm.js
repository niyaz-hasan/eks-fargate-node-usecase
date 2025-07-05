import React, { useState } from 'react';
import axios from 'axios';

const EmployeeForm = ({ employee, onUpdate }) => {
    const [phone, setPhone] = useState(employee.phone);
    const token = localStorage.getItem('token');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.put(
                `/api/employees/${employee.id}`,
                { phone },
                { headers: { 'x-access-token': token } }
            );
            onUpdate();
        } catch (error) {
            console.error('Error updating employee:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Update {employee.name}</h3>
            <label>
                Phone:
                <input
                    type="text"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                />
            </label>
            <button type="submit">Update</button>
        </form>
    );
};

export default EmployeeForm;