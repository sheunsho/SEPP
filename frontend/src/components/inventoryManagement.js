import React, { useState, useEffect } from 'react';

const InventoryManagement = () => {
  const [inventory, setInventory] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemQuantity, setNewItemQuantity] = useState(1);
  const [recipes, setRecipes] = useState([]); // State for recipes
  const [loadingRecipes, setLoadingRecipes] = useState(false);
  const [recipeError, setRecipeError] = useState(null);

  // Fetch inventory when the component mounts
  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/inventory');
      const data = await response.json();
      setInventory(data);
    } catch (error) {
      console.error("Error fetching inventory", error);
    }
  };

  const fetchRecipes = async () => {
    setLoadingRecipes(true);
    setRecipeError(null);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/recipes');
      if (!response.ok) throw new Error('Failed to fetch recipes');
      const data = await response.json();
      setRecipes(data.suggested_recipes);
    } catch (error) {
      console.error("Error fetching recipes:", error);
      setRecipeError("Failed to fetch recipes. Please try again.");
    } finally {
      setLoadingRecipes(false);
    }
  };

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
      }
    } catch (error) {
      console.error("Error adding item to inventory", error);
    }
  };

  const removeFromInventory = async (itemName) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/inventory/${itemName}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setInventory(inventory.filter((item) => item.item_name !== itemName));
      }
    } catch (error) {
      console.error("Error removing item from inventory", error);
    }
  };

  const startSimulation = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_folder: 'src/camera/images' }), // Adjust path as needed
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Simulation results:', data);
        fetchInventory(); // Refresh the inventory after simulation
      } else {
        console.error('Simulation failed:', response.statusText);
      }
    } catch (error) {
      console.error("Error starting simulation:", error);
    }
  };

  return (
    <div className="inventory-management">
      <h1>Inventory Management</h1>

      {/* Add Item Section */}
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

      {/* Inventory List */}
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

      {/* Simulation Section */}
      <div className="simulation">
        <h2>Image Recognition Simulation</h2>
        <button onClick={startSimulation}>Run Simulation</button>
      </div>

      {/* Recipe Suggestions Section */}
      <div className="recipe-suggestions">
        <h2>Recipe Suggestions</h2>
        <button onClick={fetchRecipes}>Get Recipe Suggestions</button>
        {loadingRecipes && <p>Loading...</p>}
        {recipeError && <p>Error: {recipeError}</p>}
        <ul>
          {recipes.map((recipe, index) => (
            <li key={index}>{recipe}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default InventoryManagement;
