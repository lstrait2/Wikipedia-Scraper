from flask import Blueprint, abort, jsonify, request
from util import filter_movies_helper
import urllib

def construct_movie_blueprint(movie_data):
	""" Create blueprint to handle API routing for movies

	:param movie_data: JSON data for movies
	:return: blueprint to handle movie routing for app
	"""

	# initialize the blueprint
	movie_blueprint = Blueprint('movie_blueprint', __name__)

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['GET'])
	def get_movie(movie_name):
		""" handle GET request for a specific movie

		:param movie_name: name of movie to lookup
		:return: JSON data for movie, or 400 Error if lookup fails
		"""
		movie = movie_data.get(movie_name)
		# check that movie is in data set
		if movie is None:
			# custom error handler defined in app.py
			abort(400)
		return jsonify(movie), 200

	@movie_blueprint .route('/api/movies/', methods=['GET'])
	def get_movies():
		""" handle GET request for all movies meeting filter criteria

		:return: JSON data for all movies remaining after filter application
		"""
		# get raw text of query_string
		query = request.query_string
		query = urllib.unquote(query)
		# apply filter defined by query string
		movies = filter_movies_helper(query, movie_data)
		if movies is None:
			# custom error handler defined in app.py
			abort(400)
		return jsonify(movies), 200

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['PUT'])
	def put_movie(movie_name):
		""" handle PUT request to update specific movie

		:param movie_name: name of movie to update
		:return: the new JSON data for given movie
		"""
		# look up selected movie
		movie = movie_data.get(movie_name)
		# grab data to update
		update = request.json
		if update is None or movie is None:
			# custom error handler defined in app.py
			abort(400)
		# check all keys in update data are valid before updating anything
		for key in update.keys():
			if key not in movie.keys():
				# custom error handler defined in app.py
				abort(400)
		# perform the update
		for key in update.keys():
			movie[key] = update[key]
		return jsonify(movie), 200

	@movie_blueprint .route('/api/movies/', methods=['POST'])
	def post_movie():
		""" handle POST request to add new movie to data

		:return: JSON representation of new movie
		"""
		# grab JSON data for movie to add
		new_movie = request.json
		if new_movie is None:
			# custom error handler defined in app.py
			abort(400)
		# name key must exist and be unique
		movie_name = new_movie.get("name")
		# if name already exists cannot add this movie.
		if movie_name is None or movie_name in movie_data.keys():
			abort(400)
		movie_data[movie_name] = {}
		# add the new data to stored JSON
		for key in new_movie.keys():
			movie_data[movie_name][key] = new_movie[key]
		# use 201 HTTP code for created
		return jsonify(movie_data[movie_name]), 201

	@movie_blueprint .route('/api/movies/<string:movie_name>', methods=['DELETE'])
	def delete_movie(movie_name):
		""" handle DELETE request for specific movie

		:param movie_name: movie to delete
		:return: JSON indicating if delete was successful or not
		"""
		# attempt to pop the specified movie from data
		movie = movie_data.pop(movie_name, None)
		# if pop failed, movie not found
		if movie is None:
			# custom error handler in app.py
			abort(400)
		return jsonify({'status': "Deletion of " + movie_name + " was successful"}), 200

	# return blueprint to
	return movie_blueprint

