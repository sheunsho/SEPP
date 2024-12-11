// src/components/Simulation.js
import React from 'react';

const Simulation = ({ refreshInventory }) => {
  const startSimulation = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_folder: 'src/camera/images' }), // Ensure path matches backend
      });
      if (!response.ok) throw new Error('Failed to start simulation');

      const data = await response.json();
      console.log('Simulation results:', data);

      alert(`Simulation complete! Detected items: ${data.detected_items.join(', ')}`);

      // Call the parent component's refreshInventory function to update inventory
      if (refreshInventory) {
        refreshInventory();
      }
    } catch (error) {
      console.error('Error starting simulation:', error);
      alert('Simulation failed. Check the console for more details.');
    }
  };

  return (
    <div>
      <h2>Image Recognition Simulation</h2>
      <button onClick={startSimulation}>Run Simulation</button>
    </div>
  );
};

export default Simulation;
