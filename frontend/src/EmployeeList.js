import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
`;

const Th = styled.th`
  background-color: #f5f5f5;
  padding: 12px;
  text-align: left;
`;

const Td = styled.td`
  padding: 12px;
  border-bottom: 1px solid #ddd;
`;

const Input = styled.input`
  padding: 10px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 20px;
`;

const Loading = styled.div`
  padding: 20px;
  text-align: center;
`;

function EmployeeList({ employees, loading, searchTerm, setSearchTerm }) {
  return (
    <div>
      <h1>Employee Directory</h1>
      <Input
        type="text"
        placeholder="Search by name or department..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {loading ? (
        <Loading>Loading employees...</Loading>
      ) : (
        <Table>
          <thead>
            <tr>
              <Th>Name</Th>
              <Th>Email</Th>
              <Th>Department</Th>
              <Th>Phone</Th>
              <Th>Actions</Th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <Td>{employee.name}</Td>
                <Td>{employee.email}</Td>
                <Td>{employee.department}</Td>
                <Td>{employee.phone}</Td>
                <Td>
                  <Link to={`/edit/${employee.id}`}>Edit</Link>
                </Td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

export default EmployeeList;