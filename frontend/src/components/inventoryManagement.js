import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

const InventoryManagement = () => {
  const [inventory, setInventory] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemQuantity, setNewItemQuantity] = useState(1);
  const [recipe, setRecipe] = useState(null); // For storing recipe details
  const [recipeError, setRecipeError] = useState(''); // For error messages
  const [simulationStatus, setSimulationStatus] = useState(''); // For simulation status

  // Fetch inventory from the backend
  const fetchInventory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/inventory`);
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

  // Fetch a recipe from the backend
  const fetchRecipe = async () => {
    try {
      setRecipeError('');
      setRecipe(null); // Reset previous recipe
      const response = await fetch(`${API_BASE_URL}/recipe`);
      if (response.ok) {
        const data = await response.json();
        setRecipe(data);
      } else {
        const errorData = await response.json();
        setRecipeError(errorData.error || 'Error fetching recipe');
      }
    } catch (error) {
      console.error("Error fetching recipe", error);
      setRecipeError('Error fetching recipe');
    }
  };

  // Run simulation
  const runSimulation = async () => {
    try {
      setSimulationStatus('Running simulation...');
      const response = await fetch(`${API_BASE_URL}/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_folder: 'src/camera/images', // Replace with your actual image folder path
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Simulation result:', data);
        setSimulationStatus('Simulation completed successfully!');
        fetchInventory(); // Refresh inventory after simulation
      } else {
        console.error("Error running simulation:", response.statusText);
        setSimulationStatus('Error running simulation.');
      }
    } catch (error) {
      console.error("Error running simulation", error);
      setSimulationStatus('Error running simulation.');
    }
  };

  // Add item to inventory
  const addToInventory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/inventory`, {
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
      const response = await fetch(`${API_BASE_URL}/inventory/${itemName}`, {
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

      <div className="simulation">
        <h2>Simulation</h2>
        <button onClick={runSimulation}>Run Simulation</button>
        <p>{simulationStatus}</p>
      </div>

      <div className="recipe-section">
        <h2>Recipe Finder</h2>
        <button onClick={fetchRecipe}>Get Recipe</button>
        {recipeError && <p style={{ color: 'red' }}>{recipeError}</p>}
        {recipe && (
          <div>
            <h3>Recipe: {recipe.recipe_name}</h3>
            <p>Ingredients: {recipe.ingredients.join(', ')}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default InventoryManagement;
