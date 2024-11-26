-- Create table to store the current inventory
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier
    item_name TEXT NOT NULL,              -- Name of the detected item
    quantity INTEGER DEFAULT 1            -- Quantity of the item
);
