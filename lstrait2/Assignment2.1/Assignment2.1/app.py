from flask import Flask
from model.graph.graph import Graph
from view.actor_views import construct_actor_blueprint
from view.movie_views import construct_movie_blueprint


graph_data = Graph('model/data/data.json').to_json()
app = Flask(__name__)
app.register_blueprint(construct_actor_blueprint(graph_data))
app.register_blueprint(construct_movie_blueprint(graph_data))

if __name__ == '__main__':
	app.run()
