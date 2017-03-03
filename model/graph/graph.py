import json
from nodes import ActorNode
from nodes import MovieNode

class Graph(object):
	""" Class to represent graph of ActorNodes and MovieNodes
	"""

	def __init__(self, actors_and_movies_json):
		""" Constructor.

		:param actors_and_movies_json: JSON file of actor and wikipedia data from scraper.

		"""
		self.actor_vertices = set()
		self.movie_vertices = set()
		self.name_to_movie_node = {}
		self.name_to_actor_node = {}
		# read the JSON file into a dictionary
		with open(actors_and_movies_json) as f:
			d = json.load(f)
		# initialize the nodes and edges of the graph
		self.add_nodes(d)
		self.add_edges()

	def add_nodes(self, d):
		""" add ActorNode for each actor and movie in data

		:param d: dictionary containing data from scraper.

		"""

		# create the actor and movie nodes
		for actor in d[0]:
			actor_node = ActorNode(d[0][actor])
			self.actor_vertices.add(actor_node)
			self.name_to_actor_node[actor] = actor_node
		# create the movie nodes
		for movie in d[1]:
			movie_node = MovieNode(d[1][movie])
			self.movie_vertices.add(movie_node)
			self.name_to_movie_node[movie] = movie_node

	def add_edges(self):
		""" create edges between MovieNodes and ActorNodes if actor appeared in movie.

		"""
		for actor_node in self.actor_vertices:
			for movie_node in self.movie_vertices:
				movie_node.add_neighbor(actor_node)
				actor_node.add_neighbor(movie_node)


	def dfs_traversal(self):
		""" perform a DFS traversel of graph

		"""
		# reset visited flags
		for actor_node in self.actor_vertices:
				actor_node.visited = False
		for movie_node in self.movie_vertices:
				movie_node.visited = False
		# call DFS on all nodes since might not be connected
		for actor_node in self.actor_vertices:
			if not actor_node.visited:
				self.dfs_helper(actor_node)
		for movie_node in self.movie_vertices:
			if not movie_node.visited:
				self.dfs_helper(movie_node)

	def dfs_helper(self, node):
		""" Helper function for DFS

		"""
		node.visited = True  # we've now visited node
		# visit neighbors if not visited
		for neighbor_node in node.neighbors.keys():
			if not neighbor_node.visited:
				self.dfs_helper(neighbor_node)

	def bfs(self, node, target):
		"""
		do a BFS search for target starting from node

		:param node: node to start search from

		:param target: node to search for

		:return: the depth of the search when node is found, ignore movie nodes

		"""
		# store a list of seen nodes and queue of active nodes
		seen = set()
		queue = [None, node]
		depth = 0
		while len(queue) > 0:
			curr_node = queue.pop()
			# end of current level
			if curr_node is None:
				depth += 1
				queue.insert(0, None)
				# could not find in the graph
				if queue[-1] is None:
					return -1
				continue
			# found target, return level
			if curr_node.name == target:
				return int(depth/2) # we don't want to count steps on movie nodes
			seen.add(curr_node)
			for next_node in curr_node.neighbors.keys():
				if next_node not in seen:
					queue.insert(0, next_node)

	def to_json(self):
		""" convert graph to JSON
		
		:return: a dictionary holding graph data in JSON format

		"""
		d = [{}, {}]
		for actor_name in self.name_to_actor_node.keys():
			actor = self.name_to_actor_node[actor_name].to_json()
			d[0][actor_name] = actor
		for movie_name in self.name_to_movie_node.keys():
			movie = self.name_to_movie_node[movie_name].to_json()
			d[1][movie_name] = movie
		return d

	def to_json_query(self, attr, val):
		d = [{}, {}]
		for actor_name in self.name_to_actor_node.keys():
			actor = self.name_to_actor_node[actor_name].to_json()
			if self.should_filter_actor(attr, val, actor_name, actor):
				continue
			d[0][actor_name] = actor
		for movie_name in self.name_to_movie_node.keys():
			movie = self.name_to_movie_node[movie_name].to_json()
			d[1][movie_name] = movie
		return d

	def write_to_file(self, filename):
		""" write JSON data to file
		
		:param filename: filename to store graph JSON data in

		"""
		# encode graph in JSON format
		d = self.to_json()
		# open the file with write permissions and dump JSON data
		with open(filename, 'w') as f:
			json.dump(d, f)

	def get_oldest_X_actors(self, x):
		""" sort the actors by age and return the top x
		
		:param x: number of actors to select

		:return: a list containing oldest x actors

		"""
		# check for invalid param
		if x == 0 or x < 0:
			return []
		actors = sorted(self.actor_vertices, key = lambda actor : actor.age)[-x:]
		return [(actor.name, actor.age) for actor in actors]

	def get_movies_from_year(self, year):
		""" create a new list with only movies in the given year

		:param year: the year to select movies from

		:return: a list containing movies from that year

		"""
		movies = self.get_movies_from_year_nodes(year)
		return [movie.name for movie in movies]

	def get_movies_from_year_nodes(self,year):
		""" helper method for get_movies_from_year and get_actors_from_year
    	:param year: year to select movies from

		:return: a list containing movies objects from that year

		"""
		return [movie for movie in self.movie_vertices if movie.year == year]

	def get_actors_from_year(self ,year):
		""" create list of all actors who appeared in a given year

		:param year: year to select actors from

		:return: a list of actors from that year
		"""
		actors_from_year = set()
		# get all movies for the given year
		movies_from_year = self.get_movies_from_year_nodes(year)
		# loop over movies from that year and get all actors
		for movie in movies_from_year:
			actors_from_year.update(set(movie.neighbors.keys()))
		return [actor.name for actor in actors_from_year]

	def get_top_X_grossing_actors(self, x):
		""" sort actors by grossing value and return the top x
		
		:param x: number of actors to select

		:return: list containing top-x grossing actors
		"""
		# check for invalid param
		if x == 0 or x < 0:
			return []
		actors = sorted(self.actor_vertices, key = lambda actor: actor.get_grossing_value())[-x:]
		return [(actor.name, actor.get_grossing_value()) for actor in actors]

	def get_hub_actors(self, i):
		""" sorted actors by number of connections and return top i

		:param i: number of hub actors to select
		:return: list of top i actors in terms of connections

		"""
		if i == 0 or i < 0:
			return []
		return sorted([(actor.name, actor.get_actor_connections()) for actor in self.actor_vertices], key=lambda x: x[1])[-i:]

	def get_gross_for_age_group(self, start, end):
		""" get total gross value for all actors with age between start and end

		:param start: start of age range
		:param end: end of age range
		:return: sum of gross value for all actors in this age range.

		"""
		return sum([actor.get_grossing_value() for actor in self.actor_vertices if start <= actor.age <= end])

	def get_actors_in_age_group(self, start, end):
		""" Get number of actors in age group
		:param start: start of age range
		:param end: end of age range
		:return: number actors in this age range.

		"""
		return len([actor for actor in self.actor_vertices if start <= actor.age <= end])

