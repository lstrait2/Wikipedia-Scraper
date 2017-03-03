from graph import Graph
import numpy as np
import matplotlib.pyplot as plt


def get_actor_seperations(g):
	seperations = []
	# loop over all pairs of actors
	for actor1 in g.actor_vertices:
		for actor2 in g.actor_vertices:
			# don't calculate seperation between self and self
			if actor1 == actor2:
				continue
			i = g.bfs(actor1, actor2.name)
			j = g.bfs(actor2, actor1.name)
			if i != j:
				print "we gotta problem"
			if i != -1:
				seperations.append(i)

	print sum(seperations)/float(len(seperations))
	print max(seperations)
	print min(seperations)

	return seperations


def get_gross_all_age_groups(g):
	age_groups = []
	age_counts = []
	start = 10
	end = 19
	while start < 100:
		age_groups.append(g.get_gross_for_age_group(start, end))
		age_counts.append(g.get_actors_in_age_group(start, end))
		start += 10
		end += 10
	# add one to each count to prevent divide by zero
	age_counts = map(lambda x: x+1, age_counts)
	return age_groups, age_counts


def generate_age_gross_plot(age_grosses):
	x_axis = np.arange(9)
	age_grosses = np.array(age_grosses)
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, age_grosses)
	ax.set_ylabel("Total Grossing Value")
	ax.set_xlabel("Age Range")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99'))
	plt.show()


def generate_age_gross_plot_normalized(age_grosses, actor_counts):
	x_axis = np.arange(9)
	normalized_grosses = [float(gross)/count for gross, count in zip(age_grosses, age_counts)]
	age_grosses = np.array(normalized_grosses)
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, age_grosses)
	ax.set_ylabel("Total Grossing Value")
	ax.set_xlabel("Age Range")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99'))
	plt.show()

def plot_seperations(seperations):
	counts = [0,0,0]
	for seperation in seperations:
		if seperation == 1:
			counts[0] += 1
		if seperation == 2:
			counts[1] += 1
		else:
			counts[2] += 1

	x_axis = np.arange(3)
	fig, ax = plt.subplots()
	plot = ax.bar(x_axis, counts)
	ax.set_ylabel("Count")
	ax.set_xlabel("Degree of Seperation Between Pair")
	ax.set_xticks(x_axis)
	ax.set_xticklabels(('1', '2', 'infinity'))
	plt.show()



if __name__ == '__main__':
	g = Graph('model/data/data.json')
	seperations = get_actor_seperations(g)
	plot_seperations(seperations)
	#age_grosses, age_counts = get_gross_all_age_groups(g)
	##generate_age_gross_plot(age_grosses)
	#generate_age_gross_plot_normalized(age_grosses, age_counts)