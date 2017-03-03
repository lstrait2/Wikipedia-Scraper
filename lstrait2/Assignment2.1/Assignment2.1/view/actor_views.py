from flask import Blueprint, abort, jsonify, request
import urllib
from util import filter_actors_helper


def construct_actor_blueprint(actor_data):
	""" Create blueprint to handle API routing for actors

	:param actor_data: JSON data for actors
	:return: blueprint to handle routing for actor requests
	"""
	# initialize the blueprint
	actor_blueprint = Blueprint('actor_blueprint', __name__)

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['GET'])
	def get_actor(actor_name):
		""" handle GET request for specific actor

		:param actor_name: actor to look-up
		:return: JSON data for requested actor
		"""
		# attempt to lookup actor
		actor = actor_data.get(actor_name)
		if actor is None:
			# custom error handler defined in app.py
			abort(400)
		return jsonify(actor), 200

	@actor_blueprint.route('/api/actors/', methods=['GET'])
	def get_actors():
		""" handle GET request for all actors satisfying query

		:return: JSON for actors satisfying query
		"""
		# parse the querystring
		query = request.query_string
		query = urllib.unquote(query)
		# apply the filter defined in query string
		movies = filter_actors_helper(query, actor_data)
		if movies is None:
			# custom error handler defined in app.py
			abort(400)
		return jsonify(movies), 200

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['PUT'])
	def put_actor(actor_name):
		""" handle PUT request for a specific actor

		:param actor_name: actor to update info for
		:return: JSON with updated info. for actor
		"""
		# lookup the actor
		actor = actor_data.get(actor_name)
		update = request.json
		# if actor doesn't exist or invalid data, throw 400
		if update is None or actor is None:
			abort(400)
		# check all keys are valid before updating anything
		for key in update.keys():
			if key not in actor.keys():
				abort(400)
		# perform the update
		for key in update.keys():
			actor[key] = update[key]
		return jsonify(actor), 200

	@actor_blueprint.route('/api/actors/', methods=['POST'])
	def post_actor():
		""" handle POST request for new actor

		:return: JSON data for newly created actor
		"""
		# grab JSON data to use for new actor
		new_actor = request.json
		# must have valid data
		if new_actor is None:
			abort(400)
		# name key must exist and be unique
		actor_name = new_actor.get("name")
		if actor_name is None or actor_name in actor_data.keys():
			abort(400)
		actor_data[actor_name] = {}
		# add the data to stored JSON list
		for key in new_actor.keys():
			actor_data[actor_name][key] = new_actor[key]
		return jsonify(actor_data[actor_name]), 201

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['DELETE'])
	def delete_actor(actor_name):
		""" handle DELETE request for specific actor

		:param actor_name: name of actor to delete
		:return: JSON indicating if deletion failed or succeeded
		"""
		# attempt to pop actor from JSON list
		actor = actor_data.pop(actor_name, None)
		# if pop failed, actor did not exist
		if actor is None:
			abort(400)
		return jsonify({'status': "Deletion of " + actor_name + " was successful"}), 200

	# return blueprint to main app
	return actor_blueprint

