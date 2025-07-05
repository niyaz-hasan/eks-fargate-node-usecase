import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { toast } from 'react-toastify';

const Form = styled.form`
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
`;

const FormGroup = styled.div`
  margin-bottom: 15px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const Button = styled.button`
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;

  &:hover {
    background-color: #45a049;
  }
`;

function EmployeeForm({ employees, onUpdate }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    department: '',
    phone: ''
  });

  useEffect(() => {
    if (id) {
      const employee = employees.find(emp => emp.id === parseInt(id));
      if (employee) {
        setFormData({
          name: employee.name,
          email: employee.email,
          department: employee.department,
          phone: employee.phone
        });
      }
    }
  }, [id, employees]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdate(id, formData);
    toast.success('Employee updated successfully!');
    navigate('/');
  };

  return (
    <Form onSubmit={handleSubmit}>
      <h2>Edit Employee</h2>
      <FormGroup>
        <Label>Name</Label>
        <Input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </FormGroup>
      <FormGroup>
        <Label>Email</Label>
        <Input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </FormGroup>
      <FormGroup>
        <Label>Department</Label>
        <Input
          type="text"
          name="department"
          value={formData.department}
          onChange={handleChange}
          required
        />
      </FormGroup>
      <FormGroup>
        <Label>Phone</Label>
        <Input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          required
        />
      </FormGroup>
      <Button type="submit">Update</Button>
      <Button type="button" onClick={() => navigate('/')}>
        Cancel
      </Button>
    </Form>
  );
}

export default EmployeeForm;