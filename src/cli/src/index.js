import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import InventoryManagement from './InventoryManagement'; // Import the InventoryManagement component

ReactDOM.render(
  <React.StrictMode>
    <InventoryManagement /> {/* Use the InventoryManagement component here */}
  </React.StrictMode>,
  document.getElementById('root')
);
