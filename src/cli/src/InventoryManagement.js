import React, { useState, useEffect } from 'react';

const InventoryManagement = () => {
  const [inventory, setInventory] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemQuantity, setNewItemQuantity] = useState(1);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      const response = await fetch('/api/inventory');
      const data = await response.json();
      setInventory(data);
    } catch (error) {
      console.error("Error fetching inventory", error);
    }
  };

  const addToInventory = async () => {
    if (!newItemName || newItemQuantity <= 0) {
      alert("Please enter a valid item name and quantity.");
      return;
    }

    try {
      const response = await fetch('/api/inventory', {
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
        setInventory((prevInventory) => [...prevInventory, addedItem]);
        setNewItemName('');
        setNewItemQuantity(1);
      }
    } catch (error) {
      console.error("Error adding item to inventory", error);
    }
  };

  const removeFromInventory = async (itemName) => {
    try {
      const response = await fetch(`/api/inventory/${itemName}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setInventory((prevInventory) =>
          prevInventory.filter((item) => item.item_name !== itemName)
        );
      }
    } catch (error) {
      console.error("Error removing item from inventory", error);
    }
  };

  const updateInventoryItem = async (itemName, newQuantity) => {
    if (newQuantity < 1) {
      alert("Quantity must be greater than 0.");
      return;
    }

    try {
      const response = await fetch(`/api/inventory/${itemName}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          quantity: newQuantity,
        }),
      });

      if (response.ok) {
        const updatedItem = await response.json();
        setInventory((prevInventory) =>
          prevInventory.map((item) =>
            item.item_name === itemName ? { ...item, quantity: updatedItem.quantity } : item
          )
        );
      }
    } catch (error) {
      console.error("Error updating item in inventory", error);
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
              <button onClick={() => updateInventoryItem(item.item_name, item.quantity + 1)}>Increase Quantity</button>
              <button
                onClick={() => item.quantity > 1 && updateInventoryItem(item.item_name, item.quantity - 1)}
                disabled={item.quantity <= 1}
              >
                Decrease Quantity
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default InventoryManagement;