import json
import unittest
from graph import Graph

class GraphTests(unittest.TestCase):

	def setUp(self):
		# create graph from JSON file
		self.g = Graph('model/data/data.json')
		# read JSON file into Python dictionary
		with open('model/data/data.json') as f:
			self.json_data = json.load(f)

	# test that Graph constructor correctly built graph from JSON file
	def test_json_to_graph(self):
		# each movie and actor in JSON data should have a node in graph
		self.assertEqual(len(self.json_data[1]), len(self.g.movie_vertices))
		self.assertEqual(len(self.json_data[0]), len(self.g.actor_vertices))
		# test that edge weight are properly set to (age * gross) and edges all built
		bruce_willis = None
		blind_date = None
		for actor in self.g.actor_vertices:
			if actor.name == 'Bruce Willis':
				bruce_willis = actor
		for movie in self.g.movie_vertices:
			if 'Blind Date' in movie.name:
				blind_date = movie
		# christian bale has 10 movies in test set
		self.assertEqual(len(bruce_willis.neighbors), 91)
		# both edge directions should have correct weight
		self.assertIn(bruce_willis.age * blind_date.gross, bruce_willis.neighbors.values())
		self.assertIn(bruce_willis.age * blind_date.gross, blind_date.neighbors.values())

	# test graph is properly converted back to JSON 
	def test_graph_to_json(self):
		# convert graph to json
		d = self.g.to_json()
		# check that dictionaries are the same (order doesn't matter)
		self.assertItemsEqual(self.json_data, d)

	# test small number oldest X
	def test_oldest_X_small(self):
		oldest = self.g.get_oldest_X_actors(2)
		# oldest person(s) in test set is 94
		self.assertEqual(oldest[1][1], 94)

	# test large number oldest X
	def test_oldest_X_large(self):
		# choose number larger than test set
		oldest = self.g.get_oldest_X_actors(100000)
		# oldest person(s) in test set is 94
		self.assertEqual(oldest[-1][1], 94)
		# younger person in test set is -1?
		self.assertEqual(oldest[0][1], -1)

	# test a year with small number of movies
	def test_movies_from_year_small(self):
		movies = self.g.get_movies_from_year(2017)
		# only one movie from 2017 in test set
		self.assertEqual(len(movies), 1)
		self.assertEqual(movies[0], 'The Bye Bye Man')

	# test a year that hasn't happened
	def test_movies_from_year_invalid(self):
		# no movies from 2018 exist yet
		movies = self.g.get_movies_from_year(2018)
		self.assertEqual(len(movies), 0)

	# test a year with large number of movies
	def test_movies_from_year_large(self):
		movies = self.g.get_movies_from_year(2015)
		# 28 movies from 2015 in test set
		self.assertEqual(len(movies), 3)
		# one of these movies should be Vice
		self.assertIn('Vice', movies)

	# test a year with small number of movies
	def test_actors_from_year_small(self):
		actors = self.g.get_actors_from_year(2017)
		# 1 actor in test set from John Wick: Chapter 2 (only 2017 movie we have)
		self.assertEqual(len(actors), 1)
		# Keanu Reeves should be the actor
		self.assertIn('Faye Dunaway', actors.pop())

	# look for actors in invalid year
	def test_actors_from_year_invalid(self):
		# no movies from 2018 exist yet
		actors = self.g.get_actors_from_year(2018)
		self.assertEqual(len(actors), 0)

	# look for actors in year with a lot of movies
	def test_actors_from_year_large(self):
		actor_names = self.g.get_actors_from_year(2015)
		# 10 actors in test set from 2015 movies
		self.assertEqual(len(actor_names), 10)
		# two of these actors should be Danny McBride and Bruce Willis
		self.assertIn('Bruce Willis', actor_names)
		self.assertIn('Danny McBride', actor_names)

	# check top grossing with small arg
	def test_top_grossing_actors_small(self):
		top_actors = self.g.get_top_X_grossing_actors(1)
		# top grossing actor in test set is Morgan Freeman with ~3.2 billion gross
		self.assertEqual('Bruce Willis', top_actors[0][0])
		self.assertEqual(562709189, top_actors[0][1])

	# check top grossing with invalid arg
	def test_top_grossing_actors_invalid_param(self):
		# invalid param should not cause an error
		top_actors = self.g.get_top_X_grossing_actors(-1)
		self.assertEqual(len(top_actors), 0)

	# test top grossing with large arg
	def test_top_grossing_actors_large(self):
		# choose number larger than set
		top_actors = self.g.get_top_X_grossing_actors(100000)
		# top grossing actor in test set is Bruce Willis
		self.assertEqual('Bruce Willis', top_actors[308][0])
		self.assertEqual(562709189, top_actors[308][1])
		# second top grossing actor is Faye Dunaway
		self.assertEqual('Faye Dunaway', top_actors[307][0])
		self.assertEqual(515893034, top_actors[307][1])
		# several bottom grossing actors, all with 0 
		self.assertEqual(0, top_actors[0][1])

	# test DFS traversal
	def test_dfs_traversal(self):
		self.g.dfs_traversal()
		# all nodes should be visited now
		for actor_node in self.g.actor_vertices:
			self.assertTrue(actor_node.visited)
		for movie_node in self.g.movie_vertices:
			self.assertTrue(movie_node.visited)

	# Test BFS traversal w/ a depth 1
	def test_bfs_d1(self):
		for actor in self.g.actor_vertices:
			if actor.name == 'Bruce Willis':
				bruce_willis = actor
			if actor.name == 'Kim Basinger':
				kim_bas = actor
		i = self.g.bfs(bruce_willis, kim_bas.name)
		# shortest path should have length 2
		self.assertEqual(i, 1)

	# Test BFS traversal w/ a larger depth
	def test_bfs_d2(self):
		for actor in self.g.actor_vertices:
			if actor.name == 'Kirstie Alley':
				bruce_willis = actor
			if actor.name == 'John Pankow':
				other = actor
		i = self.g.bfs(bruce_willis, other.name)
		# shortest path should have length 2
		self.assertEqual(i, 2)
		# lengths should be reciprocal
		j = self.g.bfs(other, bruce_willis.name)
		self.assertEqual(j,2)

	# Test nodes not reachable
	def test_bfs_unreachabel(self):
		for actor in self.g.actor_vertices:
			if actor.name == 'Bruce Willis':
				bruce_willis = actor
		i = self.g.bfs(bruce_willis, 'Not an Actor')
		# -1 should be returned
		self.assertEqual(i, -1)

	# Test BFS traversal w/ a larger depth
	def test_bfs_d3(self):
		for actor in self.g.actor_vertices:
			if actor.name == 'Danny Aiello':
				first = actor
			if actor.name == 'Kirstie Alley':
				other = actor
		i = self.g.bfs(first, other.name)
		# shortest path should have length 2
		self.assertEqual(i, 2)
		# lengths should be reciprocal
		j = self.g.bfs(other, first.name)
		self.assertEqual(j, 2)

	# Test top 5 hub actors
	def test_hub_actors(self):
		# select top 5 hub actors
		hub_actors = self.g.get_hub_actors(5)
		# top actor should be Bruce willis
		self.assertEqual(hub_actors[-1][0], 'Bruce Willis')
		self.assertEqual(hub_actors[-1][1], 305)
		# second to top is Jack Warden
		self.assertEqual(hub_actors[-2][0], 'Jack Warden')
		self.assertEqual(hub_actors[-2][1], 39)

	# Test getting hub actors with larger parameter
	def test_hub_actors_large(self):
		# select top 5 hub actors
		hub_actors = self.g.get_hub_actors(500)
		# top actor should still be Bruce willis
		self.assertEqual(hub_actors[-1][0], 'Bruce Willis')
		self.assertEqual(hub_actors[-1][1], 305)
		# Multiple bottom individuals with no connections
		self.assertEqual(hub_actors[0][1], 0)

	# Test hub actors with invalid param
	def test_hub_actors_invalid(self):
		hub_actors = self.g.get_hub_actors(-15)
		self.assertEqual(hub_actors, [])

	# Test gross for age group
	def test_get_gross_for_age_group(self):
		gross = self.g.get_gross_for_age_group(60, 69)
		self.assertEqual(gross, 1005773688)
		gross2 = self.g.get_gross_for_age_group(20, 29)
		self.assertEqual(gross2, 21767523)

	# Test gross for invalid age group
	def test_get_gross_for_age_group_invalid(self):
		# start age larger than end
		gross = self.g.get_gross_for_age_group(69, 60)
		self.assertEqual(gross, 0)
		# no actors in age group
		gross = self.g.get_gross_for_age_group(100, 150)
		self.assertEqual(gross, 0)

if __name__ == '__main__':
	unittest.main()
