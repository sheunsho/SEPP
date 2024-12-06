from flask import Flask, jsonify, request
from flask_cors import CORS
from cloud.database import fetch_inventory, add_to_inventory, remove_from_inventory, initialize_database

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize the database
initialize_database()

# Fetch inventory
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    try:
        inventory = fetch_inventory()
        return jsonify(inventory), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add an item to the inventory
@app.route('/api/inventory', methods=['POST'])
def add_item():
    try:
        data = request.json
        item_name = data.get('item_name')
        quantity = data.get('quantity', 1)
        if not item_name:
            return jsonify({"error": "Item name is required"}), 400
        add_to_inventory(item_name, quantity)
        return jsonify({"item_name": item_name, "quantity": quantity}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Remove an item from the inventory
@app.route('/api/inventory/<item_name>', methods=['DELETE'])
def delete_item(item_name):
    try:
        remove_from_inventory(item_name)
        return jsonify({"message": f"{item_name} removed from inventory"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
