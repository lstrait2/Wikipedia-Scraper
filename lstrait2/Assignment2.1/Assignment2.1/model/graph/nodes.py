# refactor into node 
class ActorNode(object):
	""" Node class to represent an Actor

	"""

	def __init__(self, actor):
		""" Constructor.
		
		:param actor: dictionary containing data on an actor

		"""
		self.name = actor['name']
		self.age = actor['age']
		self.movies = actor['movies']
		self.total_gross = actor['total_gross']
		self.neighbors = {} # map MovieNode to weight of edge

	def add_neighbor(self, movie_node):
		""" Add movie_node as neighbor if actor appeared in that movie

		:param movie_node: movie to attempt to add as a neighbor

		"""
		if self in movie_node.neighbors.keys():
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



class MovieNode(object):
	""" Node class to represent an Actor

	"""

	def __init__(self, movie):
		""" Constructor.

		:param movie: movie data stored in dictionary

		"""
		self.name = movie['name']
		self.year = movie['year']
		self.gross = movie['box_office']
		self.actors = movie['actors']
		self.wiki_page = movie['wiki_page']
		self.neighbors = {} # map ActorNode to weight of edge

	def add_neighbor(self, actor_node):
		""" add actor_node as neighbor if actor acted in this movie

		:param actor_node: actor to attempt to add as neighbor

		"""
		if actor_node.name in self.actors:
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
