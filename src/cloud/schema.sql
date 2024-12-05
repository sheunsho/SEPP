-- Create table to store possible food items
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for each item
    item_name TEXT NOT NULL UNIQUE             -- Ensures each name is unique
);

-- Create table to store the current inventory
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier
    item_name TEXT NOT NULL,              -- Name of the food item
    quantity INTEGER DEFAULT 1            -- Quantity of the item
);

-- Create table to store recipes - ABDOULAHI 
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    ingredients TEXT NOT NULL
);

-- Sample food items - ABDOULAHI
INSERT OR IGNORE INTO food_items (item_name) VALUES ('apple'), ('milk'), ('bread');

-- Sample recipes - ABDOULAHI
INSERT INTO recipes (recipe_name, ingredients) VALUES 
    ('Apple Pie', 'apple,flour,sugar'),
    ('Milkshake', 'milk,banana,ice cream');

-- Sample inventory - ABDOULAHI
INSERT INTO inventory (item_name, quantity) VALUES 
    ('apple', 5),
    ('milk', 2);


-- Insert data into the food_items table only if not already present
INSERT OR IGNORE INTO food_items (item_name) VALUES
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