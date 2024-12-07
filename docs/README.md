# **Student Smart Homes Smart Fridge Inventory and Recipe Management System**

## **Overview**

Student Smart Homes (SSH) Smart Fridge   system is a backend and frontend system that allows users to manage inventory, simulate detection of items, and find recipes based on available ingredients. The backend is built with Flask and SQLite, and the frontend is implemented using React.

---

## **Features**

### **Backend**
- **Inventory Management:**
  - **Add Items:** Add new items to the inventory or update the quantity of existing items.
  - **Remove Items:** Reduce the quantity of an item or completely remove it if the quantity reaches zero.
  - **View Inventory:** Retrieve the current list of inventory items and their quantities.
- **Simulation:**
  - Detect items from images using a simulation powered by MobileNetV2.
  - Automatically add detected items to the inventory.
- **Recipe Finder:**
  - Retrieve recipes that can be made using ingredients available in the inventory.
  - Populate the database with sample recipes.
- **Deduplication:**
  - Merge duplicate inventory entries into a single entry with the total quantity.

### **Frontend**
- **Inventory Management Interface:**
  - View all inventory items.
  - Add new items with a specified quantity.
  - Remove items, reducing their quantity or completely deleting them if their quantity reaches zero.
- **Simulation Interface:**
  - Trigger the backend simulation process to detect items from an image folder and add them to the inventory.
- **Recipe Finder Interface:**
  - Fetch a recipe based on the current inventory.
  - Display the recipe name and required ingredients.

---

## **Setup**

### **Backend**
- Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- Run the backend:
    ```bash
    python app.py
    ```
- Populate the database with sample recipes (optional):
    ```bash
    python src/cloud/database.py --populate-recipes
    ```
    
### **Frontend**
- Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
- Install dependencies:
    ```bash
    npm install
    ```
- Start the frontend server:
    ```bash
    npm start
    ```

---

## **API Endpoints**

### **Inventory**
- **GET /api/inventory:** Retrieve all inventory items.
- **POST /api/inventory:** Add or update an inventory item.
    - **Payload:**
      ```json
      {
        "item_name": "apple",
        "quantity": 5
      }
      ```
- **DELETE /api/inventory/<item_name>:** Remove an item or reduce its quantity.
    - **Query Parameters:**
      - `quantity` (optional, default is 1)

### **Simulation**
- **POST /api/simulate:** Run the simulation to detect items from images.
    - **Payload:**
      ```json
      {
        "image_folder": "src/camera/images"
      }
      ```

### **Recipe Finder**
- **GET /api/recipe:** Retrieve a random recipe that can be made with the current inventory.

---

## **Usage**

### **Inventory Management**
- Add new items or update existing ones using the "Add to Inventory" button.
- Remove items using the "Remove" button next to each inventory entry.

### **Simulation**
- Click the "Run Simulation" button to trigger the backend simulation.
- Detected items will automatically be added to the inventory.

### **Recipe Finder**
- Click the "Get Recipe" button to retrieve a recipe that can be made with the current inventory.
- If no recipe can be made, an error message will be displayed.

---

## **Sample Recipes**

Here are the sample recipes preloaded into the database:
- **Pasta:** Ingredients - pasta, tomato sauce, cheese
- **Sandwich:** Ingredients - bread, lettuce, tomato, cheese
- **Salad:** Ingredients - lettuce, tomato, cucumber, olive oil
- **Omelette:** Ingredients - egg, milk, cheese
- **Grilled Cheese:** Ingredients - bread, cheese, butter

---

## **Database Schema**

### **Tables**
- **inventory:**
  - `item_name` (TEXT, primary key)
  - `quantity` (INTEGER)
- **recipes:**
  - `recipe_name` (TEXT, primary key)
  - `ingredients` (TEXT)

---

## **Known Issues**
- Duplicate inventory entries might appear if the deduplication script is not run.
- The simulation assumes a predefined set of valid food keywords and manual mappings.

---

## **Future Improvements**
- Add user authentication to secure inventory and recipe management.
- Allow users to customize and add their own recipes via the frontend.
- Enhance simulation to work with a wider variety of food items and improve accuracy.
