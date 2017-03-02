from flask import Flask, abort, jsonify, request
from model.graph.graph import Graph
import urllib
app = Flask(__name__)


#TODO: seperate into actor and movie classes

@app.route('/api/actors/<string:actor_name>', methods=['GET'])
def get_actor(actor_name):
	actor = graph_data[0].get(actor_name)
	if actor is None:
		#TODO: more detailed error message
		abort(400)
	return jsonify(actor), 200


@app.route('/api/movies/<string:movie_name>', methods=['GET'])
def get_movie(movie_name):
	movie = graph_data[1].get(movie_name)
	if movie is None:
		#TODO: more detailed error message
		abort(400)
	return jsonify(movie), 200

@app.route('/api/actors/', methods=['GET'])
def get_actors():
	query = request.query_string
	query = urllib.unquote(query)
	#TODO: move this method out into util
	if '&' in query:
		return query.split('&')[0]
	elif '|' in query:
		return query.split('|')[0]
	else:
		return query


@app.route('/api/movies/', methods=['GET'])
def get_movies():
	query = request.query_string
	query = urllib.unquote(query)
	#TODO: move this method out into util
	#TODO: recursively split on booleans, keep filtering (make copy each time)
	if '&' in query:
		return query.split('&')[0]
	elif '|' in query:
		return query.split('|')[0]
	else:
		return query


@app.route('/api/actors/<string:actor_name>', methods=['PUT'])
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


@app.route('/api/movies/<string:movie_name>', methods=['PUT'])
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


@app.route('/api/actors/', methods=['POST'])
def post_actor():
	new_actor = request.json
	if new_actor is None:
		abort(400)
	# name key must exist and be unique
	actor_name = new_actor.get("name")
	if actor_name is None or actor_name in graph_data[0].keys():
		abort(400)
	graph_data[0][actor_name] = {}
	#TODO: check all keys are valid for type
	for key in new_actor.keys():
		graph_data[0][actor_name][key] = new_actor[key]
	return jsonify(graph_data[0][actor_name]), 201


@app.route('/api/movies/', methods=['POST'])
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

@app.route('/api/actors/<string:actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
	actor = graph_data[0].pop(actor_name, None)
	if actor is None:
		# TODO: more detailed error message
		abort(400)
	return 'Deleting of ' + actor_name + ' was successful!', 200

@app.route('/api/movies/<string:movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
	movie = graph_data[1].pop(movie_name, None)
	if movie is None:
		# TODO: more detailed error message
		abort(400)
	return 'Deleting of ' + movie_name + ' was successful!', 200


if __name__ == '__main__':
	graph_data = Graph('model/data/data.json').to_json()
	app.run()
