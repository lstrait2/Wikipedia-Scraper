import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from graph import Graph


def generate_bipartite_graph(graph):
	""" Generate a graph with disjoint sets seperated to each side
	:param graph: graph to plot
	"""
	nx_graph = nx.Graph()
	labels = {}
	# loop over the top 5 actors
	for actor_node in sorted(list(graph.actor_vertices), key=lambda x : len(x.neighbors.keys()))[-5:]:
		nx_graph.add_node(actor_node.name, type='actor')
		labels[actor_node.name] = actor_node.name + ": " + str(actor_node.age)
		# loop over 5 of the movies these actors were in
		for movie_node in actor_node.neighbors.keys()[:5]:
			nx_graph.add_node(movie_node.name, type='movie')
			nx_graph.add_edge(actor_node.name, movie_node.name)
			labels[movie_node.name] = movie_node.name + ": " + str(movie_node.gross)
			# add some actors who were also in this movie
			for actor_node2 in movie_node.neighbors.keys()[:3]:
				nx_graph.add_node(actor_node2.name, type='actor')
				nx_graph.add_edge(actor_node2.name, movie_node.name)
				labels[actor_node2.name] = actor_node2.name + ": " + str(actor_node2.age)
	actor_nodes = []
	movie_nodes =[]
	colors = []
	pos = {}
	i = 0
	j = 0
	# set the color for each set and pull disjoint sets apart
	for node, data in nx_graph.nodes(data=True):
		if data['type'] == 'actor':
			actor_nodes.append(node)
			colors.append('r')
			pos[node] = (1, i)
			i += 1
		else:
			movie_nodes.append(node)
			colors.append('g')
			pos[node] = (2, j)
			j += 1
	# draw the graph using matplotlib
	nx.draw(nx_graph, pos=pos, labels=labels, with_labels= True, node_color=colors)
	plt.show()


def generate_spring_graph_large(graph):
	""" Generate a plot for large graph and seperate with Spring algo.

	:param graph: graph to draw
	"""
	nx_graph = nx.Graph()
	# loop over top 150 actors
	for actor_node in sorted(list(graph.actor_vertices), key=lambda x: len(x.neighbors.keys()))[-150:]:
		nx_graph.add_node(actor_node.name, type='actor')
		# loop over all movies they were in
		for movie_node in actor_node.neighbors.keys():
			nx_graph.add_node(movie_node.name, type='movie')
			nx_graph.add_edge(actor_node.name, movie_node.name)

	actor_nodes = []
	movie_nodes = []
	colors = []
	# change color of nodes.
	for node, data in nx_graph.nodes(data=True):
		if data['type'] == 'actor':
			actor_nodes.append(node)
			colors.append('r')
		else:
			movie_nodes.append(node)
			colors.append('g')
	# draw the plot
	nx.draw_spring(nx_graph, with_labels=False, node_color=colors)
	plt.show()


def generate_spring_graph_small(graph):
	""" Generate a plot for large graph and seperate with Spring algo. Special case

	:param graph: graph to plot
	"""
	nx_graph = nx.Graph()
	labels = {}
	# loop over bottom 200 actors
	for actor_node in sorted(list(graph.actor_vertices), key=lambda x: len(x.neighbors.keys()))[:200]:
		nx_graph.add_node(actor_node.name, type='actor')
		labels[actor_node.name] = ""
		# loop over neighboring actors
		for movie_node in actor_node.neighbors.keys():
			labels[movie_node.name] = ""
			nx_graph.add_node(movie_node.name, type='movie')
			nx_graph.add_edge(actor_node.name, movie_node.name)

	# add bruce willis seperately
	bruce_willis = sorted(list(graph.actor_vertices), key=lambda x: len(x.neighbors.keys()))[-1]
	nx_graph.add_node(bruce_willis.name, type='actor')
	labels[bruce_willis.name] = "BRUCE WILLIS"
	for movie_node in bruce_willis.neighbors.keys():
		labels[movie_node.name] = ""
		nx_graph.add_node(movie_node.name, type='movie')
		nx_graph.add_edge(bruce_willis.name, movie_node.name)

	actor_nodes = []
	movie_nodes = []
	colors = []
	# add colors to graph
	for node, data in nx_graph.nodes(data=True):
		if data['type'] == 'actor':
			actor_nodes.append(node)
			colors.append('r')
		else:
			movie_nodes.append(node)
			colors.append('g')
	# draw plot.
	nx.draw_spring(nx_graph, labels=labels, with_labels=True, node_color=colors)
	plt.show()


def generate_spring_graph_subset(graph):
	""" generate spring plot for small subset of graph

	:param graph: graph to plot
	"""
	nx_graph = nx.Graph()
	labels = {}
	# select "mid-size" actors
	for actor_node in sorted(list(graph.actor_vertices), key=lambda x: len(x.neighbors.keys()))[-35:-30]:
		nx_graph.add_node(actor_node.name, type='actor')
		labels[actor_node.name] = actor_node.name + ": " + str(actor_node.age)
		# add movies these actors were in
		for movie_node in actor_node.neighbors.keys():
			nx_graph.add_node(movie_node.name, type='movie')
			nx_graph.add_edge(actor_node.name, movie_node.name)
			labels[movie_node.name] = movie_node.name + ": " + str(movie_node.gross)
			# add a few actors from these movies
			for actor_node2 in movie_node.neighbors.keys()[:3]:
				nx_graph.add_node(actor_node2.name, type='actor')
				nx_graph.add_edge(actor_node2.name, movie_node.name)
				labels[actor_node2.name] = actor_node2.name + ": " + str(actor_node2.age)
	actor_nodes = []
	movie_nodes = []
	colors = []
	# change colors
	for node, data in nx_graph.nodes(data=True):
		if data['type'] == 'actor':
			actor_nodes.append(node)
			colors.append('r')
		else:
			movie_nodes.append(node)
			colors.append('g')
	# draw plot
	nx.draw_spring(nx_graph, labels=labels, with_labels=True, node_color=colors)
	plt.show()


graph_data = Graph('model/data/data.json')
generate_bipartite_graph(graph_data)
generate_spring_graph_large(graph_data)
generate_spring_graph_small(graph_data)
generate_spring_graph_subset(graph_data)


