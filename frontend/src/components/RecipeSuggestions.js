// src/components/RecipeSuggestions.js
import React, { useState, useEffect } from 'react';

const RecipeSuggestions = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipes = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://127.0.0.1:5000/api/recipes');
        if (!response.ok) throw new Error('Failed to fetch recipes');
        const data = await response.json();
        setRecipes(data.suggested_recipes);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div>
      <h2>Suggested Recipes</h2>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {recipes.length === 0 && !loading && !error && <p>No recipes available based on current inventory.</p>}
      <ul>
        {recipes.map((recipe, index) => (
          <li key={index}>{recipe}</li>
        ))}
      </ul>
    </div>
  );
};

export default RecipeSuggestions;
