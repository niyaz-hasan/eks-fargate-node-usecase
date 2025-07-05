import React, { useState } from 'react';
import EmployeeList from './EmployeeList';
import EmployeeForm from './EmployeeForm';

function App() {
    const [selectedEmployee, setSelectedEmployee] = useState(null);
    const [addingNew, setAddingNew] = useState(false);

    const handleFormClose = () => {
        setSelectedEmployee(null);
        setAddingNew(false);
    };

    return (
        <div className="App">
            <h1>Employee Directory</h1>
            <button onClick={() => setAddingNew(true)}>Add Employee</button>
            <EmployeeList onSelectEmployee={setSelectedEmployee} />
            {(selectedEmployee || addingNew) && (
                <EmployeeForm
                    employee={selectedEmployee}
                    onUpdate={handleFormClose}
                />
            )}
        </div>
    );
}

export default App;
