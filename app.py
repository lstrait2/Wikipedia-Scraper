from flask import Flask, jsonify
from model.graph.graph import Graph
from view.actor_views import construct_actor_blueprint
from view.movie_views import construct_movie_blueprint


# initialize graph data
graph_data = Graph('model/data/data.json').to_json()
# initialize flask app
app = Flask(__name__)
# registers routes for movie and actor
app.register_blueprint(construct_actor_blueprint(graph_data[0]))
app.register_blueprint(construct_movie_blueprint(graph_data[1]))


@app.errorhandler(400)
def detailed_error_400(error):
	""" Custom Error Handler when 400 is thrown

	:param error: the details of error that was thrown
	:return: Error to user in JSON format
	"""
	return jsonify({'status': "Bad request. Make sure you are providing valid parameters"}), 400

if __name__ == '__main__':
	app.run()
