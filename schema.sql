-- Create table to store possible food items
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for each item
    name TEXT NOT NULL                    -- Name of the food item
);

-- Insert data into the food_items table
INSERT INTO food_items (name) VALUES
    ('apple'),
    ('milk'),
    ('bread'),
    ('cheese'),
    ('eggs'),
    ('butter'),
    ('carrots'),
    ('tomatoes'),
    ('potatoes'),
    ('yogurt'),
    ('chicken'),
    ('fish'),
    ('rice'),
    ('pasta');

    -- Create table to store the current inventory
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier
    item_name TEXT NOT NULL,              -- Name of the food item
    quantity INTEGER DEFAULT 1            -- Quantity of the item
);