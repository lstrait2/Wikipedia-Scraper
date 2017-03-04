def apply_filter_movies(param, val, movie_data):
	""" Apply the filter to movie_data

	:param param: parameter to filter on
	:param val: value to filter for
	:param movie_data: JSON data for movies
	:return: entries in JSON data that satisfy filter.
	"""
	# create a fresh dictionary, do not want to delete data in main copy
	filtered_data = {}
	# iterate over all entires and check if parameter is satisfied
	for movie_name, movie in movie_data.iteritems():
		if param == 'name' and val in movie['name']:
			filtered_data[movie_name] = movie
		elif param == 'actors' and val in movie['actors']:
			filtered_data[movie_name] = movie
		elif param == 'year' and val.isdigit() and int(val) == movie['year']:
			filtered_data[movie_name] = movie
		elif param == 'box_office' and val.isdigit() and int(val) == movie['box_office']:
			filtered_data[movie_name] = movie
	# return dictionary with results
	return filtered_data


def apply_filter_actors(param, val, actor_data):
	""" Apply the filter to actor_data

		:param param: parameter to filter on
		:param val: value to filter for
		:param movie_data: JSON data for actors
		:return: entries in JSON data that satisfy filter.
	"""
	# create a fresh dictionary, do not want to delete data in main copy
	filtered_data = {}
	# iterate over all entires and check if parameter is satisfied
	for actor_name, actor in actor_data.iteritems():
		if param == 'name' and val in actor['name']:
			filtered_data[actor_name] = actor
		elif param == 'movies' and val in actor['movies']:
			filtered_data[actor_name] = actor
		elif param == 'age' and val.isdigit() and int(val) == actor['age']:
			filtered_data[actor_name] = actor
		elif param == 'total_gross' and val.isdigit() and int(val) == actor['total_gross']:
			filtered_data[actor_name] = actor
	# return dictionary with results
	return filtered_data


def filter_movies_helper(query, movie_data):
	""" apply query to movie_data

	:param query: query passed by user in querystring
	:param movie_data: JSON data for movies
	:return: filtered JSON data
	"""
	# a recursive query had no results, return None
	if movie_data is None:
		return None
	# if boolean operations exist in query, handle each clause recursively (& takes precedence)
	if '&' in query:
		# split into 2 clauses along &
		query1, query2 = query.split('&', 1)
		# apply first query
		temp_data = filter_movies_helper(query1, movie_data)
		# apply second query to data returned by first query
		return filter_movies_helper(query2, temp_data)
	elif '|' in query:
		# split into 2 clauses along |
		query1, query2 = query.split('|', 1)
		# apply first query
		temp_data = filter_movies_helper(query1, movie_data)
		if temp_data is None:
			temp_data = {}
		# apply second query to data and union with result of first query
		return dict(filter_movies_helper(query2, movie_data), **temp_data)
	# base case, just apply the query to single clause
	else:
		param, val = query.split('=')
		if val[0] == '"' or val[0] == '"':
			val = val[1:-1]
		# pass to apply filter helper
		return apply_filter_movies(param, val, movie_data)


def filter_actors_helper(query, actor_data):
	""" apply query to actor_data

		:param query: query passed by user in querystring
		:param actor_data: JSON data for actors
		:return: filtered JSON data
	"""
	# a recursive query had no results, return None
	if actor_data is None:
		return None
	# if boolean operations exist in query, handle each clause recursively (& takes precedence)
	if '&' in query:
		query1, query2 = query.split('&', 1)
		# apply first query
		temp_data = filter_actors_helper(query1, actor_data)
		# apply second query to data returned by first query
		return filter_actors_helper(query2, temp_data)
	elif '|' in query:
		query1, query2 = query.split('|', 1)
		# apply first query
		temp_data = filter_actors_helper(query1, actor_data)
		if temp_data is None:
			return None
		# apply second query to data and union with result of first query
		return dict(filter_actors_helper(query2, actor_data), **temp_data)
	else:
		param, val = query.split('=')
		if val[0] == '"' or val[0] == '"':
			val = val[1:-1]
		# pass to apply filter helper
		return apply_filter_actors(param, val, actor_data)
