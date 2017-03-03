from graph import Graph
import numpy as np
import matplotlib.pyplot as plt


def get_actor_seperations(g):
	""" get a list of seperation degree between all pairs of actors

	:param g: graph to calc. seperation for
	:return: a list of seperations
	"""
	seperations = []
	# loop over all pairs of actors
	for actor1 in g.actor_vertices:
		for actor2 in g.actor_vertices:
			# don't calculate seperation between self and self
			if actor1 == actor2:
				continue
			i = g.bfs(actor1, actor2.name)
			j = g.bfs(actor2, actor1.name)
			if i != -1:
				seperations.append(i)
	return seperations


def get_gross_all_age_groups(g):
	""" get total grossing value for all age groups

	:param g: graph to calculate for
	:return: list of grossing value for all age groups
	"""
	age_groups = []
	age_count = []
	start = 10
	end = 19
	# create gross and counts for all 9 age groups
	while start < 100:
		age_groups.append(g.get_gross_for_age_group(start, end))
		age_count.append(g.get_actors_in_age_group(start, end))
		# go to next age group
		start += 10
		end += 10
	# add one to each count to prevent divide by zero
	age_count = map(lambda x: x+1, age_count)
	return age_groups, age_count


def generate_age_gross_plot(age_grosses):
	""" create plot showing gross data for all age groups

	:param age_grosses: list of total gross for all age groups
	"""
	# organize data
	x_axis = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
	age_grosses = np.array(age_grosses)
	# create plot
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, age_grosses)
	# label plot
	ax.set_ylabel("Total Grossing Value")
	ax.set_xlabel("Age Range")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99'))
	plt.show()


def generate_age_gross_plot_normalized(age_grosses, actor_counts):
	""" create plot showing gross data for all age groups normalized

	:param age_grosses: total gross for all age groups
	:param actor_counts: count for all age groups
	:return:
	"""
	# organize data and normalize
	x_axis = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
	normalized_grosses = [float(gross)/count for gross, count in zip(age_grosses, actor_counts)]
	age_grosses = np.array(normalized_grosses)
	# create plot
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, age_grosses)
	# label the plot
	ax.set_ylabel("Total Grossing Value")
	ax.set_xlabel("Age Range")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99'))
	plt.show()


def plot_seperations(seperations):
	""" create plot of seperation degree data

	:param seperations: list of seperation degree for all pairs
	"""
	counts = [0,0,0]
	# iterate over all seperations
	for seperation in seperations:
		if seperation == 1:
			counts[0] += 1
		if seperation == 2:
			counts[1] += 1
		else:
			counts[2] += 1

	# create the plot
	x_axis = np.array([0, 1, 2])
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, counts)
	# label the plot
	ax.set_ylabel("Count")
	ax.set_xlabel("Degree of Seperation Between Pair")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('1', '2', 'infinity'))
	plt.show()

def plot_connections(g):
	""" create a box plot showing data on connections

	:param g: graph to create plot for
	"""
	connections = np.array([actor.get_actor_connections() for actor in g.actor_vertices])
	plt.boxplot(connections, showfliers=False)
	plt.show()


if __name__ == '__main__':
	g = Graph('model/data/data.json')
	seperation = get_actor_seperations(g)
	plot_seperations(seperation)
	age_gross, age_counts = get_gross_all_age_groups(g)
	generate_age_gross_plot(age_gross)
	generate_age_gross_plot_normalized(age_gross, age_counts)
	print g.get_hub_actors(10)
	plot_connections(g)
