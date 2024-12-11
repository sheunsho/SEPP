// src/App.js
import React, { useEffect, useState } from 'react';
import './App.css';
import InventoryManagement from './components/inventoryManagement';
import RecipeSuggestions from './components/RecipeSuggestions';
import Simulation from './components/Simulation';

function App() {
  const [inventory, setInventory] = useState([]);

  // Function to fetch inventory
  const fetchInventory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/inventory');
      if (response.ok) {
        const data = await response.json();
        setInventory(data); // Update state
      } else {
        console.error('Error fetching inventory:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching inventory:', error);
    }
  };

  useEffect(() => {
    fetchInventory(); // Fetch inventory on app load
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Inventory Management</h1>
        <InventoryManagement inventory={inventory} fetchInventory={fetchInventory} />

        <h1>Recipe Suggestions</h1>
        <RecipeSuggestions />

        <h1>Image Recognition Simulation</h1>
        <Simulation refreshInventory={fetchInventory} />
      </header>
    </div>
  );
}

export default App;
