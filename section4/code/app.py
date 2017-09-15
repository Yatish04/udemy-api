from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required # this is a decorator

from security import authenticate, identity


# setup
app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity)
# creates a new endpoint: /auth
# send a username and password
# then it sends info to authenticate function
# find the correct user object using username
# compare pwd
# if match, return the user, and /auth end point returns a JW token
# wich can then be used to identify authenticated user


# initialize data
items = []


# class for item
class Item(Resource):

	# get the item by unique name
	@jwt_required() # need authentication for this action
	def get(self, name):
		# next function will return the next item in the list
		# if noting in there, will return None (default value)

		# python3
		# item = next(filter(lambda x: x["name"] == name, items), None) 
		# return {"item": item}, 200 if item else 404

		# python2
		item = filter(lambda x: x["name"] == name, items)
		if len(item) == 1:
			return {"item": item[0]}, 200
		else:
			return {"item": None}, 404

	# create a new item
	def post(self, name):
		# if there is a match, return a message

		# python3
		# if next(filter(lambda x: x["name"] == name, items), None):
		# 	return {"message": "An item with name '{0}' already exists.".format(name)}, 400

		# python2
		item = filter(lambda x: x["name"] == name, items)
		if item != []:
			return {"message": "An item with name '{0}' already exists.".format(name)}, 400

		data = request.get_json()
		item = {
			"name": name,
			"price": data["price"]
		}
		items.append(item)
		return item, 201 # code for creating

	# delete the item by unique name
	def delete(self, name):
		global items # this items created is the global variable we created before
		items = list(filter(lambda x: x["name"] != name, items))
		return {"message": "Item '{0}' deleted.".format(name)}

	# create or update item
	def put(self, name):
		data = request.get_json()

		# python3
		# item = next(filter(lambda x: x["name"] == name, items), None)
		# if item is None:
		# 	item = {
		# 		"name": name,
		# 		"price": data["price"]
		# 	}
		# 	items.append(item)
		# else:
		# 	item.update(data) # update the dictionary
		# return item 

		# python2
		item = filter(lambda x: x["name"] == name, items)
		if len(item) == 0:
			item = {
				"name": name,
				"price": data["price"]
			}
			items.append(item)
		else:
			item = item[0]
			item.update(data)
		return item



# class for items
class Items(Resource):

	# get all items
	def get(self):
		return jsonify({"items": items})


# add resources
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")

# run
app.run(port=5000, debug=True)
