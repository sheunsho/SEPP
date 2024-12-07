// src/App.js
import React from 'react';
import './App.css';
import InventoryManagement from './components/inventoryManagement';  // Correct import based on lowercase "i"

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Inventory Management</h1>
        <InventoryManagement />  {/* Use your InventoryManagement component here */}
      </header>
    </div>
  );
}

export default App;
