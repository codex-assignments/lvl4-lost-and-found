from flask import Flask, request
from lost_items import lost_items
app=Flask(__name__)

def find_item_by_id(item_id):
        for item in lost_items:
                if item["id"] == item_id:
                        return item
        return None

def get_next_id():
        if len(lost_items) == 0:
                return 1
        highest_id = 0
        for item in lost_items:
                if item["id"]>highest_id:
                        highest_id=item["id"]
        return highest_id + 1

@app.route("/")
def home():
        return {
                "message": "Campus Lost and Found!",
                "routes": ["GET '/' -- Returns docs","GET '/lost-items' --Returns all lost items", "POST '/get-items' -- Adds new item"]
        }

@app.route("/lost-items")
def get_lost_items():
        return lost_items

@app.route("/lost-items/<int:item_id>")
def get_lost_item_by_id(item_id):
        item = find_item_by_id(item_id)
        if item is None: 
                return {"error": "Item not found."}, 404
        return item, 200

# ?isClaimed = true
@app.route("/lost-items/search")
def search_lost_items():
        search_text = request.args.get("name", "")
        if search_text == "":
                search_text = request.args.get("isClaimed", "")
        results = []
        for item in lost_items: 
                if search_text.lower() in item["name"].lower() or search_text.lower() in str(item["isClaimed"]).lower():
                        results.append(item)
                return results
        if len(results) == 0:
                return {"message": "No found items match the search term."}

        
@app.route("/lost-items", methods=["POST"], strict_slashes=False)
def create_lost_item():
        body = request.get_json() or {}

        if "name" not in body:
                return {"error": "Name is required field"}, 400
        new_item = {
                "id": get_next_id(),
                "name": body["name"],
                "isClaimed": False
        }
        lost_items.append(new_item)
        return new_item, 201
