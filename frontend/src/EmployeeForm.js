import React, { useState } from 'react';
import axios from 'axios';

const EmployeeForm = ({ employee, onUpdate }) => {
    const [name, setName] = useState(employee?.name || '');
    const [department, setDepartment] = useState(employee?.department || '');
    const [phone, setPhone] = useState(employee?.phone || '');
    const token = localStorage.getItem('token');

    const isEdit = !!employee;

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isEdit) {
                await axios.put(
                    `/api/employees/${employee.id}`,
                    { phone },
                    { headers: { 'x-access-token': token } }
                );
            } else {
                await axios.post(
                    `/api/employees`,
                    { name, department, phone },
                    { headers: { 'x-access-token': token } }
                );
            }
            onUpdate(); // Close form & refresh
        } catch (error) {
            console.error('Error saving employee:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>{isEdit ? `Update ${employee.name}` : 'Add New Employee'}</h3>
            {!isEdit && (
                <>
                    <label>
                        Name:
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </label>
                    <br />
                    <label>
                        Department:
                        <input
                            type="text"
                            value={department}
                            onChange={(e) => setDepartment(e.target.value)}
                            required
                        />
                    </label>
                    <br />
                </>
            )}
            <label>
                Phone:
                <input
                    type="text"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                />
            </label>
            <br />
            <button type="submit">{isEdit ? 'Update' : 'Add'}</button>
        </form>
    );
};

export default EmployeeForm;
