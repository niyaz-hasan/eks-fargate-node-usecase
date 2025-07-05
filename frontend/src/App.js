import React, { useState } from 'react';
import EmployeeList from './EmployeeList';
import EmployeeForm from './EmployeeForm';

function App() {
    const [selectedEmployee, setSelectedEmployee] = useState(null);

    return (
        <div className="App">
            <h1>Employee Directory</h1>
            <EmployeeList onSelectEmployee={setSelectedEmployee} />
            {selectedEmployee && (
                <EmployeeForm
                    employee={selectedEmployee}
                    onUpdate={() => setSelectedEmployee(null)}
                />
            )}
        </div>
    );
}

export default App;