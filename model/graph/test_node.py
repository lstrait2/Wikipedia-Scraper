import json
import unittest
from nodes import ActorNode 
from nodes import MovieNode

class GraphTests(unittest.TestCase):

	def setUp(self):
		# create nodes from JSON (stored in dict)
		self.actor = {'name': 'Lance', 'age': 22, 'movies': ['movie1'], 'total_gross' : 1000, 'json_class': 'actor'}
		self.movie = {'name': 'movie1', 'box_office': 100, 'year': 2017, 'actors': ['Lance'],
					  'wiki_page' : '', 'json_class': 'movie'}
		self.movie2 = {'name': 'movie2', 'box_office': 1000, 'year': 2016, 'actors': ['George'],
					   'wiki_page' : '', 'json_class': 'movie'}
		self.actor_node = ActorNode(self.actor)
		self.movie_node = MovieNode(self.movie)
		self.movie_node2 = MovieNode(self.movie2)

	# test construct correctly sets fields
	def test_node_constructors(self):
		self.assertEqual(self.actor_node.name, 'Lance')
		self.assertEqual(self.actor_node.age, 22)
		self.assertEqual(self.actor_node.movies, ['movie1'])
		self.assertEqual(self.movie_node.name, 'movie1')
		self.assertEqual(self.movie_node.year, 2017)
		self.assertEqual(self.movie_node.actors, ['Lance'])
		# neighbors should initially be empty
		self.assertEqual(self.movie_node.neighbors, {})
		self.assertEqual(self.actor_node.neighbors, {})

	# test converting node to Json (stored in dict)
	def test_node_to_json(self):
		json_actor = self.actor_node.to_json()
		json_movie = self.movie_node.to_json()
		self.assertItemsEqual(json_movie, self.movie)
		self.assertItemsEqual(json_actor, self.actor)

	# test getting movies an actor is in
	def test_movies_in(self):
		self.movie_node.add_neighbor(self.actor_node)
		self.actor_node.add_neighbor(self.movie_node)
		self.assertEqual(self.actor_node.get_movies_in(), ['movie1'])

	# test getting actors is in a movie
	def test_actors_in(self):
		self.movie_node.add_neighbor(self.actor_node)
		self.actor_node.add_neighbor(self.movie_node)
		self.assertEqual(self.movie_node.get_actors_in(), ['Lance'])

	# test getting gross for a movie
	def test_movie_gross(self):
		self.assertEqual(self.movie_node.get_gross(), 100)

	# test adding a neighbor valid
	def test_add_neighbor_valid(self):
		self.movie_node.add_neighbor(self.actor_node)
		self.actor_node.add_neighbor(self.movie_node)
		# check neighbor was set with correct weight on edge (age*gross)
		self.assertEqual(self.actor_node.neighbors, {self.movie_node : (22*100)})
		self.assertEqual(self.movie_node.neighbors, {self.actor_node : (22*100)})

	# test trying to add an invalid neighbor
	def test_add_neighbor_invalid(self):
		self.actor_node.add_neighbor(self.movie_node2)
		self.assertEqual(self.actor_node.neighbors, {})

	# test getting total grossing for an actor
	def test_total_grossing_actor(self):
		# add a neighbor
		self.movie_node.add_neighbor(self.actor_node)
		self.actor_node.add_neighbor(self.movie_node)
		self.assertEqual(self.actor_node.get_grossing_value(), 1000)

	# test total grossing no movies
	# test getting total grossing for an actor
	def test_total_grossing_actor_invalid(self):
		# add a neighbor
		self.actor_node.add_neighbor(self.movie_node2)
		self.assertEqual(self.actor_node.get_grossing_value(), 1000)

if __name__ == '__main__':
	unittest.main()