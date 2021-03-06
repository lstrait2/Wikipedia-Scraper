class Node(object):

	def __init__(self, data):
		""" Constructor

		:param data: Json Data
		"""
		self.name = data['name']
		self.neighbors = {}


class ActorNode(Node):
	""" Node class to represent an Actor

	"""

	def __init__(self, actor):
		""" Constructor.
		
		:param actor: dictionary containing data on an actor

		"""
		super(ActorNode, self).__init__(actor)
		self.age = actor['age']
		self.movies = actor['movies']
		self.total_gross = actor['total_gross']

	def add_neighbor(self, movie_node):
		""" Add movie_node as neighbor if actor appeared in that movie

		:param movie_node: movie to attempt to add as a neighbor

		"""

		if movie_node.name in self.movies or self.name in movie_node.actors:
			# weight of edge is age of actor times gross of movie
			self.neighbors[movie_node] = (movie_node.get_gross() * self.age)

	def get_movies_in(self):
		""" return list of all movies actor appeared in
		
		:return: list of movies this actor was in

		"""
		return [movie.name for movie in self.neighbors.keys()]

	def get_grossing_value(self):
		""" sum the gross of all movies this actor has appeared in
		
		:return: the total grossing value of this actor

		"""
		return self.total_gross

	def get_actor_connections(self):
		""" get number of actors this actor has worked with

		:return: number of actors this actor has been in a movie with

		"""
		connections = set()
		# iterate over all movies this actor is in
		for movie_node in self.neighbors.keys():
			# iterate over all actors in this movie
			for actor_node in movie_node.neighbors:
				if actor_node != self:
					connections.add(actor_node)
		return len(connections)



	def to_json(self):
		""" convert node to JSON format (stored as dictionary)
		
		:return: the actor data stored in dictionary

		"""
		actor = {}
		actor['name'] = self.name
		actor['age'] = self.age
		actor['movies'] = self.movies
		actor['total_gross'] = self.total_gross
		actor['json_class'] = "Actor"
		return actor


class MovieNode(Node):
	""" Node class to represent an Actor

	"""

	def __init__(self, movie):
		""" Constructor.

		:param movie: movie data stored in dictionary

		"""
		super(MovieNode, self).__init__(movie)
		self.year = movie['year']
		self.gross = movie['box_office']
		self.actors = movie['actors']
		self.wiki_page = movie['wiki_page']

	def add_neighbor(self, actor_node):
		""" add actor_node as neighbor if actor acted in this movie

		:param actor_node: actor to attempt to add as neighbor

		"""
		if actor_node.name in self.actors or self.name in actor_node.movies:
			# weight of edge is age of actor times gross of movie
			self.neighbors[actor_node] = (actor_node.age * self.gross)

	def get_gross(self):
		""" get gross of this movie
		
		:return: gross of this movie

		"""
		return self.gross

	def get_actors_in(self):
		""" get actors who appeared in this movie

		:return: list of actors who were in this movie

		"""
		return [actor.name for actor in self.neighbors.keys()]

	def to_json(self):
		""" convert node to JSON format (stored as dictionary)
		
		:return: movie data in dictionary

		"""
		movie = {}
		movie['name'] = self.name
		movie['year'] = self.year
		movie['box_office'] = self.gross
		movie['actors'] = self.actors
		movie['wiki_page'] = self.wiki_page
		movie['json_class'] = 'Movie'
		return movie
