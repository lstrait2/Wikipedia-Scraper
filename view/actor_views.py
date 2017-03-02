from flask import Blueprint, abort, jsonify, request
import urllib
from util import filter_actors_helper


def construct_actor_blueprint(graph_data):

	actor_blueprint = Blueprint('actor_blueprint', __name__)

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['GET'])
	def get_actor(actor_name):
		actor = graph_data[0].get(actor_name)
		if actor is None:
			#TODO: more detailed error message
			abort(400)
		return jsonify(actor), 200

	@actor_blueprint.route('/api/actors/', methods=['GET'])
	def get_actors():
		query = request.query_string
		query = urllib.unquote(query)
		movies = filter_actors_helper(query, graph_data[0])
		if movies is None:
			# TODO: more detailed error message
			abort(400)
		return jsonify(movies), 200

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['PUT'])
	def put_actor(actor_name):
		actor = graph_data[0].get(actor_name)
		update = request.json
		if update is None or actor is None:
			abort(400)
		# check all keys are valid before updating anything
		for key in update.keys():
			if key not in actor.keys():
				abort(400)
		for key in update.keys():
			actor[key] = update[key]
		return jsonify(actor), 200

	@actor_blueprint.route('/api/actors/', methods=['POST'])
	def post_actor():
		new_actor = request.json
		if new_actor is None:
			abort(400)
		# name key must exist and be unique
		actor_name = new_actor.get("name")
		if actor_name is None or actor_name in graph_data[0].keys():
			abort(400)
		graph_data[0][actor_name] = {}
		# TODO: check all keys are valid for type
		for key in new_actor.keys():
			graph_data[0][actor_name][key] = new_actor[key]
		return jsonify(graph_data[0][actor_name]), 201

	@actor_blueprint.route('/api/actors/<string:actor_name>', methods=['DELETE'])
	def delete_actor(actor_name):
		actor = graph_data[0].pop(actor_name, None)
		if actor is None:
			# TODO: more detailed error message
			abort(400)
		return 'Deleting of ' + actor_name + ' was successful!', 200


	return actor_blueprint

