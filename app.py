from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory product storage and ID tracker
products = []
next_id = 1


@app.route("/products", methods=["POST"])
def create_product():
  global next_id
  data = request.get_json()

  if not data:
    return jsonify({"error": "Invalid or missing JSON payload"}), 400

  # Check for required fields
  if "name" not in data or "price" not in data:
    return jsonify({"error": "Missing required fields: 'name' or 'price'"}), 400

  name = data["name"]
  price = data["price"]

  # Validation logic (contains an intentional bug regarding zero prices)
  if price <= 0:
    return jsonify({"error": "Price must be greater or equal to zero"}), 400

  product = {"id": next_id, "name": name, "price": price}
  products.append(product)
  next_id += 1

  return jsonify(product), 201


@app.route("/products", methods=["GET"])
def get_products():
  return jsonify(products), 200


if __name__ == "__main__":
  app.run(debug=True, port=5000)