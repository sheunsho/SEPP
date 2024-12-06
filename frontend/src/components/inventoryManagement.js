// src/components/inventoryManagement.js
import React, { useState, useEffect } from 'react';

const InventoryManagement = () => {
  const [inventory, setInventory] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemQuantity, setNewItemQuantity] = useState(1);

  // Fetch inventory from the backend
  const fetchInventory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/inventory');
      if (response.ok) {
        const data = await response.json();
        setInventory(data);
      } else {
        console.error("Error fetching inventory:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching inventory", error);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  // Add item to inventory
  const addToInventory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/inventory', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          item_name: newItemName,
          quantity: newItemQuantity,
        }),
      });

      if (response.ok) {
        const addedItem = await response.json();
        setInventory([...inventory, addedItem]);
        setNewItemName('');
        setNewItemQuantity(1);
      } else {
        console.error("Error adding item to inventory:", response.statusText);
      }
    } catch (error) {
      console.error("Error adding item to inventory", error);
    }
  };

  // Remove item from inventory
  const removeFromInventory = async (itemName) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/inventory/${itemName}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setInventory(inventory.filter(item => item.item_name !== itemName));
      } else {
        console.error("Error removing item from inventory:", response.statusText);
      }
    } catch (error) {
      console.error("Error removing item from inventory", error);
    }
  };

  return (
    <div className="inventory-management">
      <h1>Inventory Management</h1>

      <div className="add-item">
        <input
          type="text"
          value={newItemName}
          placeholder="Enter item name"
          onChange={(e) => setNewItemName(e.target.value)}
        />
        <input
          type="number"
          value={newItemQuantity}
          min="1"
          onChange={(e) => setNewItemQuantity(parseInt(e.target.value))}
        />
        <button onClick={addToInventory}>Add to Inventory</button>
      </div>

      <div className="inventory-list">
        <h2>Current Inventory</h2>
        <ul>
          {inventory.map((item) => (
            <li key={item.item_name}>
              {item.item_name} - Quantity: {item.quantity}
              <button onClick={() => removeFromInventory(item.item_name)}>Remove</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default InventoryManagement;  // Ensure you use 'default' export
