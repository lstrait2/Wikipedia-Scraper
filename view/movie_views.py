from flask import Blueprint, abort, jsonify, request
from util import apply_filter_movies, filter_movies_helper
import urllib

def construct_movie_blueprint(graph_data):

	movie_blueprint = Blueprint('movie_blueprint', __name__)

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['GET'])
	def get_movie(movie_name):
		movie = graph_data[1].get(movie_name)
		if movie is None:
			#TODO: more detailed error message
			abort(400)
		return jsonify(movie), 200

	@movie_blueprint .route('/api/movies/', methods=['GET'])
	def get_movies():
		query = request.query_string
		query = urllib.unquote(query)
		movies = filter_movies_helper(query, graph_data[1])
		if movies is None:
			#TODO: more detailed error message
			abort(400)
		return jsonify(movies), 200

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['PUT'])
	def put_movie(movie_name):
		movie = graph_data[1].get(movie_name)
		update = request.json
		if update is None or movie is None:
			abort(400)
		# check all keys are valid before updating anything
		for key in update.keys():
			if key not in movie.keys():
				abort(400)
		for key in update.keys():
			movie[key] = update[key]
		return jsonify(movie), 200

	@movie_blueprint .route('/api/movies/', methods=['POST'])
	def post_movie():
		new_movie = request.json
		if new_movie is None:
			abort(400)
		# name key must exist and be unique
		movie_name = new_movie.get("name")
		if new_movie is None or movie_name in graph_data[1].keys():
			abort(400)
		graph_data[1][movie_name] = {}
		#TODO: check all keys are valid for type
		for key in new_movie.keys():
			graph_data[1][movie_name][key] = new_movie[key]
		return jsonify(graph_data[1][movie_name]), 201

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['DELETE'])
	def delete_movie(movie_name):
		movie = graph_data[1].pop(movie_name, None)
		if movie is None:
			# TODO: more detailed error message
			abort(400)
		return 'Deleting of ' + movie_name + ' was successful!', 200

	return movie_blueprint

