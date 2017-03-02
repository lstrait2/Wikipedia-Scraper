from bs4 import BeautifulSoup
import json
import logging
import urllib2

# refactor
def parse_actor_page(pageurl):
	""" Attempt to parse actor information from given URL.

	:param pageurl: the wikipedia page to parse

	:return: dictionary containing data on actor, or None if page format was invalid.

	"""
	logging.info('attempt to parse page ' + pageurl + 'as an actor')
	# attempt to load the wikipedia page and parse with beautifulsoup
	soup = load_page(pageurl)
	if soup == None:
		return None
	# attempt to retrieve name from page tree
	name = parse_name_actor(soup,pageurl)
	if name == None:
		return None
	# attempt to retrieve age from page tree
	age = parse_age_actor(soup, pageurl)
	if age == None:
		return None
	# attempt to retrieve movie names and urls from page tree
	movies, movieurls = parse_filmography_actor(soup, pageurl)
	if movies == None:
		return None
	# build dictionary to return (will be converted to JSON before returned to user)
	actor = {}
	actor['name'] = name
	actor['age'] = age
	actor['movies'] = movies
	actor['movieurls'] = movieurls
	logging.info('' + pageurl + ' was successfully parsed as an actor')
	return actor

def parse_movie_page(pageurl):
	""" Attempt to parse movie information from given URL.

	:param pageurl: the wikipedia page to parse

	:return: dictionary containing data on movie, or None if page format was invalid.

	"""
	logging.info('attempt to parse page ' + pageurl + 'as a movie')
	movie = {}
	# attempt to load the wikipedia page and parse with beautifulsoup
	soup = load_page(pageurl)
	if soup == None:
		return None
	# attempt to retrieve name from page tree
	name = parse_name_movie(soup, pageurl)
	if name == None:
		return None
	# attempt to retrieve movie year and gross from page tree
	year, gross = parse_infotable_movie(soup, pageurl)
	if year == None or gross == None:
		return None
	# attempt to retrieve actor names and urls from page tree
	actors, actorurls = parse_actors_movie(soup, pageurl)
	if actors == None:
		return None
	# build dictionary to return (will be converted to JSON before returned to user)
	movie['name'] = name
	movie['year'] = year
	movie['gross'] = gross
	movie['actors'] = actors
	movie['actorurls'] = actorurls
	logging.info('' + pageurl + ' was successfully parsed as a movie')
	return movie

def load_page(pageurl):
	""" Helper method to load webpage using urllib2 and parse with beautifulsoup

	:param pageurl: url of webpage to load

	:return: BeautifulSoup object containing parse of webpage

	"""
	# Attempt to load the page
	try:
		webpage = urllib2.urlopen(pageurl)
	# Page could not be loaded (hit quota?)
	except urllib2.HTTPError, e:
		logging.warning('' + pageurl + ' is not a valid wikipedia page and could not be opened')
		return None
	# URL is invalid
	except urllib2.URLError, e:
		logging.warning('' + pageurl + ' is not a valid URL and could not be opened')
		return None
	# return beautifulsoup parsetree for the page
	return BeautifulSoup(webpage,'html.parser')

def parse_infotable_movie(soup, pageurl):
	""" Retrieve year and gross from parsetree for a movie

	:param soup: BeautifulSoup object containing parse of webpage

	:param pageurl: url of page to parse
	
	:return: year and gross of the movie

	"""
	# find the infobox (right of screen)
	info_table = soup.findAll('table', {'class': 'infobox vevent'})
	# if info_table doesn't exist, cannot find year and gross
	if len(info_table) == 0:
		return None, None
	gross = None
	year = None
	# search each row of the info_table
	for row in info_table[0].findAll('tr'):
		header = row.find('th')
		# check for header for year row
		if header != None and header.find('div') != None and header.find('div').get_text() == 'Release date':
			date = row.find('td')
			if date.find('div') != None and date.find('div').find('ul') != None:
				date = date.find('div').find('ul').find('li').find('span')
			# clean the date and extract year before returning
			year = parse_year_movie(date.get_text(), pageurl)
		# check for header for gross row
		if header != None and header.get_text() == 'Box office':
			gross = row.find('td').get_text()
			if gross == None:
				return None
			# clean the gross number to return as int
			gross = parse_gross_movie(gross, pageurl)
	return year, gross

def parse_name_movie(soup, pageurl):
	""" Retrieve name of movie from parsetree

	:param soup: BeautifulSoup object containing parsetree

	:param pageurl: pageurl of page to parse

	:return: name of the movie

	"""
	# find the summary class header
	name_tag = soup.findAll('th', {'class': 'summary'})
	# if this header doesn't exist, cannot retrieve name
	if len(name_tag) == 0:
		logging.warn('' + pageurl + 'does not have a valid name field, parsing terminated')
		return None
	# return name as a string
	return name_tag[0].get_text()

def parse_actors_movie(soup, pageurl):
	""" Retrieve actors (names and urls) in the movie

	:param pageurl: url of page to parse

	:param soup: BeautifulSoup object containing parse of page

	:return: actors and actorurls of actors in the movie.
	"""
	# find the cast section
	cast = soup.findAll('span', {'id': 'Cast'})
	# if cast doesn't exist, return None
	if len(cast) == 0:
		logging.warning('' + pageurl + ' does not have a cast section, parsing will terminate')
		return None, None
	# cast will be stored in unordered list
	actor_list = cast[0].find_next('ul')
	actors = []
	actorurls = []
	# read the whole cast list
	while actor_list != None:
		for actor in actor_list.findAll('a'):
			# add name and URL to lists
			actors.append(actor.get('title'))
			actorurls.append(actor.get('href'))
		# reached the end of the list
		if actor_list.find_next('dl') == None:
			break
		# go to next row
		actor_list = actor_list.find_next('ul')
	return actors, actorurls

def parse_gross_movie(gross, pageurl):
	""" clean gross value.
	
	:param pageurl: url of page to parse

	:param gross: raw gross value

	:return: cleaned gross value converted to int.
	"""
	# numerical value sometimes stored in brackets
	if '[' in gross:
		gross = gross[:gross.index('[')]
	# numerical value sometimes stored in parens
	if '(' in gross:
		gross = gross[:gross.index('(')]
	# remove million affix and multiply numerical value by 1,000,000
	if 'million' in gross:
		# remove US prefix
		if 'US' in gross:
			gross = gross[2:]
		# remove prefix and attempt to cast to float
		try:
			gross = float(gross.replace('million', "").strip()[1:])					
			gross *= 1000000
			gross = int(gross)
		# invalid numerical value (cannot be cast to float)
		except ValueError:
				logging.warn('' + pageurl + 'has invalid format for gross field')
	# remove billion affix and multiply numerical value by 1,000,000,000
	elif 'billion' in gross:
		# remove prefix and attempt to cast to float
		try:
			gross = float(gross.replace('billion', "").strip()[1:])
			gross *= 1000000000
			gross = int(gross)
		# invalid numerical value, cannot be cast to float
		except ValueError:
			logging.warn('' + pageurl + 'has invalid format for gross field')
	# we just received a plain numerical value
	else:
		# strip whitespace before casting
		gross = gross[1:].replace(',', '').strip()
		if not gross.isdigit():
			logging.warning('' + pageurl + ' has a gross figure with invalid format, parsing will terminate')
			return None
		gross = int(gross)
	return gross

def parse_year_movie(date, pageurl):
	""" retrieve movie year from parse tree
	
	:param pageurl: pageurl to parse

	:param soup: BeautifulSoup Object with page parse

	:return: year of movie or None if page format is invalid.

	"""
	# remove dashes if 01-05-2015 format
	if '-' in date:
		date = date.strip()[1:-1]
		year = date.split('-')[0]
	# remove commas if format is 01,05,2015
	else:
		if ',' in date:
			year = date.split(',')[1].strip()
		elif ' ' in date.strip():
			if len(date.split(' ')) < 3:
				logging.warning('' + pageurl + ' has a year with invalid format, parsing will terminate')
				return None
			year = date.split(' ')[2]
		else:
			year = date
	# strip whitespace
	year = year.strip()
	# make sure we received valid numerical value to cast
	if not year.isdigit():
		logging.warning('' + pageurl + ' has a year with invalid format, parsing will terminate')
		return None
	# cast to int and return
	return int(year)

def parse_age_actor(soup, pageurl):
	""" retrieve actor age from parse tree
	
	:param pageurl: pageurl to parse

	:param soup: BeautifulSoup Object with page parse

	:return: age of the actor or None if page format is invalid.
	"""
	age = None
	# search for class containing age
	age_span = soup.findAll('span', { 'class' : 'noprint ForceAgeToShow' });
	if len(age_span) == 0:
		# check if actor is dead.
		death_span = soup.findAll('span', {'class': 'deathplace'})
		# if actor is dead, need to parse slightly differently to get age
		if len(death_span) != 0:
			s = death_span[0].find_parent().get_text()
			idx = s.index('aged')
			end_idx = s[idx:].index(')')
			s = s[idx:idx+end_idx]
			age = [int(s) for s in s.split() if s.isdigit()]
			# entry did not contain age, likely only contained deathplace.
			if len(age) == 0:
				logging.warning('' + pageurl + ' does not contain an age for the actor and will not be parsed')
				return None
			age = age[0]
		# if actor is not dead and no age field, no other way to get age
		else:
			logging.warning('' + pageurl + ' does not contain an age for the actor and will not be parsed')
			return None
	# clean the input and cast to int
	if age == None:
		age = int(age_span[0].next[1:-1].split()[1])
	return age

def parse_filmography_actor(soup, pageurl):
	""" retrieve filmography from parse tree
	
	:param pageurl: pageurl to parse

	:param soup: BeautifulSoup Object with page parse

	:return: filmography of the actor or None if page format is invalid.
	"""
	movies = []
	movieurls = []
	# find the filmography section
	filmography  = soup.findAll('div', {'class': 'div-col columns column-count column-count-3'})
	filmography +=	soup.findAll('div', {'class': 'div-col columns column-count column-count-2'})
	# if filmography div exists, search each row.
	if len(filmography) != 0:
		movie_list = filmography[0].find_next('ul')
		for movie in movie_list.findAll('a'):
			movieurls.append(movie.get('href'))
			movies.append(movie.get('title'))
	else:
		# filmography may be stored in table format instead
		filmography = soup.findAll('span', {'id': 'Filmography'})
		if len(filmography) == 0:
			logging.warning('' + pageurl + ' does not contain a filmography for the actor and will not be parsed')
			return None, None
		movie_table = filmography[0].find_next('table')
		# if no table either, nowhere we can get filmography
		if movie_table == None:
			logging.warning('' + pageurl + ' does not contain a filmography for the actor and will not be parsed')
			return None, None
		# if table exits, read each row of it
		for row in movie_table.findAll('tr'):
			col1 = row.find_next('td')
			# table should have at least 1 column
			if col1 == None:
				logging.warning('' + pageurl + ' has filmography table in irregular format, parsing will terminate')
				return None, None
			# table should have at least 2 columns
			col2 = col1.find_next('td')
			if col2 == None:
				logging.warning('' + pageurl + ' has filmography table in irregular format, parsing will terminate')
				return None, None
			# find the link in the second column
			movie = col2.find('a')
			# if this link is nonempty, get href and title
			if movie != None:
				movieurls.append(movie.get('href'))
				movies.append(movie.get('title'))
		# address case of external filmography
		if len(movieurls) == 1:
			logging.warning('' + pageurl + ' has an external filmography, parsing will terminate')
			return None, None
	return movies, movieurls

def parse_name_actor(soup, pageurl):
	""" retrieve actor name from parse tree
	
	:param pageurl: pageurl to parse

	:param soup: BeautifulSoup Object with page parse

	:return: name of the actor or None if page format is invalid.
	"""
	# find fn (fullname) class
	name_span = soup.findAll('span', {'class': 'fn'});
	# if class does not exist, cannot get name
	if len(name_span) == 0:
		logging.warning('' + pageurl + ' does not contain a name for the actor and will not be parsed')
		return None
	name = name_span[0].get_text()
	# handle edge cases where HTML is butchered - cannot convert to JSON if this goes through
	if '<' in name:
		logging.warning('' + pageurl + ' does not contain a name for the actor and will not be parsed')
		return None
	return name

def run_scraping(max_actors, max_movies, starting_url):
	""" run the scraper until <max_actors> actors and <max_movies> movies have been read starting from starting_url

	:param max_actors: maximum number of actor pages to parse

	:param max_movies: maximum number of movie pages to parse

	:param starting_url: first page to run the scraper on

	"""
	actors = []
	movies = []
	seen_actors = set() # keep track of actor urls we have already read
	seen_movies = set() # keep track of movie urls we have already read
	# attempt to parse starting page as actor
	actor = parse_actor_page(starting_url)
	# parsing as actor was successful
	if actor != None:
		actors.append(actor)
		seen_actors.add(starting_url[24:])
	# parsing as actor was unsuccessful, try as a movie instead
	else:
		logging.warning('' + starting_url + 'was unable to be parsed as an actor, will attempt as a movie')
		movie = parse_movie_page(starting_url)
		# if we could not parse as movie either, just end
		if movie == None:
			logging.error('' + starting_url + 'was unable to be parsed as a movie as well, application must terminate')
			return
		movies.append(movie)
		seen_movies.add(starting_url[24:])

	baseurl = 'https://en.wikipedia.org' # all URLS in dictionaries are relative, need this.
	i = 0 # keep track where in actor list we currently are
	j = 0 # keep track where in movie list we currently are
	# continue scraping until enough actors and movies found
	while len(actors) < max_actors or len(movies) < max_movies:
		# traverse over new actors (since last iteration)
		for actor in actors[i:]:
			# if actor exists, attempt to read pages for movies they are in.
			if actor != None and len(movies) < max_movies + 1:
				for movieurl in actor['movieurls'][-20:]:
					# if we already read this movie, skip it
					if movieurl in seen_movies:
						continue
					movie = parse_movie_page(baseurl + movieurl)
					seen_movies.add(movieurl)
					# if parsing was successful add it
					if movie != None:
						movies.append(movie)
		# update where in actor list we are
		i = max(0,len(actors) - 1)
		# traverse over new movies (since last iteration)
		for movie in movies[j:]:
			if movie != None and len(actors) < max_actors +1:
				for actorurl in movie['actorurls'][:20]:
					# if we already read this actor, skip it
					if actorurl in seen_actors:
						continue
					actor = parse_actor_page(baseurl + actorurl)
					seen_actors.add(actorurl)
					# if parsing was successful, add it
					if actor != None:
						actors.append(actor)
		# update current position in movie list
		j = max(0,len(movies) - 1)

	# convert python dictionaries to JSON and dump to file
	with open('data/actors_and_movies7.json', 'w') as f:
		json.dump({'actors': actors, 'movies': movies}, f)


def main():
	# start the logger, set level to lowest possible.
	logging.basicConfig(filename='logs/scraper.log', level=logging.DEBUG)
	logging.info('Started running web scraper')
	run_scraping(15, 15, 'https://en.wikipedia.org/wiki/Rogue_One')
	logging.info('Completed running of web scraper')

if __name__ == '__main__':
	main()
