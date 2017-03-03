from model.graph.graph import Graph
import app
import json
import unittest


class APITestCase(unittest.TestCase):

	def setUp(self):
		app.app.config['TESTING'] = True
		self.flask_app = app.app.test_client()
		self.graph_data = Graph('model/data/data.json').to_json()

	# test a request to an invalid URL
	def test_get_invalid_url(self):
		res = self.flask_app.get('/api/invalid/actors/Bruce Willis')
		# should throw 404
		self.assertEqual(res.status_code, 404)

	# test a valid GET request for an actor
	def test_get_actor_valid(self):
		res = self.flask_app.get('/api/actors/Bruce Willis')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# compare response data to stored JSON
		self.assertEqual(data, self.graph_data[0]['Bruce Willis'])

	# Test an invalid GET request for an actor
	def test_get_actor_invalid(self):
		res = self.flask_app.get('/api/actors/afafafafaf')
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		# check that custom error handler was invoked
		data = json.loads(res.data)
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test a valid GET request for a movie
	def test_get_movie_valid(self):
		res = self.flask_app.get('/api/movies/Pulp Fiction')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# compare response data to stored JSON
		self.assertEqual(data, self.graph_data[1]['Pulp Fiction'])

	# Test a valid GET request for a movie
	def test_get_movie_invalid(self):
		res = self.flask_app.get('/api/movies/dfkadkadz')
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		# check that custom error handler was invoked
		data = json.loads(res.data)
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test a valid GET request for movies
	def test_get_movies_valid(self):
		res = self.flask_app.get('/api/movies/?name="Pulp Fiction"')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# Pulp Fiction should be in data response
		self.assertEqual(data['Pulp Fiction'], self.graph_data[1]['Pulp Fiction'])
		# Pulp Fiction should be only movie in data response
		self.assertEqual(len(data.keys()), 1)

	# Test a valid GET request for movies, more complex querystring
	def test_get_movies_complex(self):
		res = self.flask_app.get('/api/movies/?name="Pulp Fiction"|box_office=24')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# Pulp Fiction should be in data response
		self.assertEqual(data['Pulp Fiction'], self.graph_data[1]['Pulp Fiction'])
		# The Bye Bye Man should also be in data response
		self.assertEqual(data['The Bye Bye Man'], self.graph_data[1]['The Bye Bye Man'])
		# Nothing else should be in data
		self.assertEqual(len(data.keys()), 2)

	# Test a valid GET request for movies, more complex querystring
	def test_get_movies_complex_boolean_exp(self):
		res = self.flask_app.get('/api/movies/?name="Pulp Fiction"|box_office=24&actors="John Travolta"')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# Pulp Fiction should be in data response
		self.assertEqual(data['Pulp Fiction'], self.graph_data[1]['Pulp Fiction'])
		# Nothing else should be in data
		self.assertEqual(len(data.keys()), 1)

	# Test a invalid GET request for movies
	def test_get_movies_invalid(self):
		res = self.flask_app.get('/api/movies/?name="Unknown Fake Name')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# check that response data is empty
		data = json.loads(res.data)
		self.assertEqual(data, {})

	# Test a valid GET request for actors
	def test_get_actors_valid(self):
		res = self.flask_app.get('/api/actors/?name="Bruce Willis"')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# compare response data to stored JSON
		self.assertEqual(data['Bruce Willis'], self.graph_data[0]['Bruce Willis'])
		# Bruce Willis should be only actor in data response
		self.assertEqual(len(data.keys()), 1)

	# Test a valid GET request for actors, more complex querystring
	def test_get_actors_valid_complex(self):
		res = self.flask_app.get('/api/actors/?age=94|name="Bruce Willis')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# read res data into dictionary
		data = json.loads(res.data)
		# compare response data to stored JSON
		self.assertEqual(data['Bruce Willis'], self.graph_data[0]['Bruce Willis'])
		self.assertEqual(data['Steven Hill'], self.graph_data[0]['Steven Hill'])
		self.assertEqual(data['Abe Vigoda'], self.graph_data[0]['Abe Vigoda'])
		self.assertEqual(len(data.keys()), 3)

	# Test a invalid GET request for actors
	def test_get_actors_invalid(self):
		res = self.flask_app.get('/api/actors/?name="Unknown Fake Name')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# check that response data is empty
		data = json.loads(res.data)
		self.assertEqual(data, {})

	# Test a invalid GET request for actors
	def test_get_actors_invalid_param(self):
		res = self.flask_app.get('/api/actors/?stuff="Unknown Fake Name')
		# request should be successful
		self.assertEqual(res.status_code, 200)
		# check that response data is empty
		data = json.loads(res.data)
		self.assertEqual(data, {})

	# Test a valid PUT request for a movie
	def test_put_movie_valid(self):
		res = self.flask_app.put('/api/movies/Pulp Fiction', data=json.dumps({'box_office': 500}),
								 headers={'Content-Type': 'application/json'})
		# request should be successful
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		# check that box office was updated
		self.assertEqual(data['box_office'], 500)
		# if we now do a get request new value should be reflected
		res2 = self.flask_app.get('/api/movies/Pulp Fiction')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear still
		self.assertEqual(data['box_office'], 500)

	# Test a invalid PUT request for a movie
	def test_put_movie_invalid(self):
		res = self.flask_app.put('/api/movies/Pulp Fiction', data=json.dumps({'boxO': 500}),
								 headers={'Content-Type': 'application/json'})
		# request should not be successful
		self.assertEqual(res.status_code, 400)
		# if we now do a get request data should be unchanged
		res2 = self.flask_app.get('/api/movies/Pulp Fiction')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear still
		self.assertEqual(data['box_office'], 213)

	# Test a invalid PUT request for a movie
	def test_put_movie_invalid_content_type(self):
		res = self.flask_app.put('/api/movies/Pulp Fiction', data=json.dumps({'box_office': 500}),
								 headers={'Content-Type': 'application/text'})
		# request should not be successful
		self.assertEqual(res.status_code, 400)
		# if we now do a get request data should be unchanged
		res2 = self.flask_app.get('/api/movies/Pulp Fiction')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear still
		self.assertEqual(data['box_office'], 213)

	# Test a valid PUT request for an actor
	def test_put_actor_valid(self):
		res = self.flask_app.put('/api/actors/Bruce Willis', data=json.dumps({'total_gross': 500}),
								 headers={'Content-Type': 'application/json'})
		# request should be successful
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.data)
		# check that total gross was updated
		self.assertEqual(data['total_gross'], 500)
		# if we now do a get request new value should be reflected
		res2 = self.flask_app.get('/api/actors/Bruce Willis')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear still
		self.assertEqual(data['total_gross'], 500)

	# Test a invalid PUT request for an actor
	def test_put_actor_invalid(self):
		res = self.flask_app.put('/api/actors/Bruce Willis', data=json.dumps({'tgross': 500}),
								 headers={'Content-Type': 'application/json'})
		# request should be successful
		self.assertEqual(res.status_code, 400)
		# if we now do a get request no change should have made
		res2 = self.flask_app.get('/api/actors/Bruce Willis')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear still
		self.assertEqual(data['total_gross'], 562709189)

	# Test a valid POST request for an actor
	def test_post_movie_valid(self):
		res = self.flask_app.post('/api/movies/', data=json.dumps({'name': "Some New Movie"}),
								  headers={'Content-Type': 'application/json'})
		# request should be successful - 201 for created
		self.assertEqual(res.status_code, 201)
		data = json.loads(res.data)
		# check that new movie appears in output
		self.assertEqual(data, {'name': "Some New Movie"})
		# if we now do a get request new value should be reflected
		res2 = self.flask_app.get('/api/movies/Some New Movie')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear
		self.assertEqual(data, {'name': "Some New Movie"})

	# Test a invalid POST request for an movie
	def test_post_movie_invalid_no_name(self):
		res = self.flask_app.post('/api/movies/', data=json.dumps({'year': 2007}),
								  headers={'Content-Type': 'application/json'})
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		data = json.loads(res.data)
		# check that error output appears
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test a invalid POST request for an movie
	def test_post_movie_invalid_wrong_type(self):
		res = self.flask_app.post('/api/movies/', data=json.dumps({'name': 'some_new_movie'}),
								  headers={'Content-Type': 'application/text'})
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		data = json.loads(res.data)
		# check that error output appears
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test a valid POST request for an actor
	def test_post_actor_valid(self):
		res = self.flask_app.post('/api/actors/', data=json.dumps({'name': "Some New Actor"}),
								  headers={'Content-Type': 'application/json'})
		# request should be successful - 201 for created
		self.assertEqual(res.status_code, 201)
		data = json.loads(res.data)
		# check that new movie appears in output
		self.assertEqual(data, {'name': "Some New Actor"})
		# if we now do a get request new value should be reflected
		res2 = self.flask_app.get('/api/actors/Some New Actor')
		# request should be successful
		self.assertEqual(res2.status_code, 200)
		# read res data into dictionary
		data = json.loads(res2.data)
		# changed value should appear
		self.assertEqual(data, {'name': "Some New Actor"})

	# Test a invalid POST request for an actor
	def test_post_actor_invalid_no_name(self):
		res = self.flask_app.post('/api/actors/', data=json.dumps({'age': 20}),
								  headers={'Content-Type': 'application/json'})
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		data = json.loads(res.data)
		# check that error output appears
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test a invalid POST request for an actor
	def test_post_actor_invalid_wrong_type(self):
		res = self.flask_app.post('/api/actors/', data=json.dumps({'name': 'some_new_actor'}),
								  headers={'Content-Type': 'application/text'})
		# request should be unsuccessful
		self.assertEqual(res.status_code, 400)
		data = json.loads(res.data)
		# check that error output appears
		self.assertEqual(data, {'status': "Bad request. Make sure you are providing valid parameters"})

	# Test successful DELETE request for movie
	def test_delete_movie_valid(self):
		res = self.flask_app.delete('/api/movies/Ed')
		self.assertEquals(res.status_code, 200)
		data = json.loads(res.data)
		# success message should appear
		self.assertEqual({'status': "Deletion of Ed was successful"}, data)
		# should not be able to look up deleted movie
		res = self.flask_app.get('/api/movies/Ed')
		self.assertEqual(res.status_code, 400)

	# Test unsuccessful DELETE request for movie
	def test_delete_movie_invalid(self):
		res = self.flask_app.delete('/api/movies/some_movie')
		# should fail
		self.assertEquals(res.status_code, 400)

	# Test successful DELETE request for actor
	def test_delete_actor_valid(self):
		res = self.flask_app.delete('/api/actors/Madeleine Stowe')
		self.assertEquals(res.status_code, 200)
		data = json.loads(res.data)
		# success message should appear
		self.assertEqual({'status': "Deletion of Madeleine Stowe was successful"}, data)
		# should not be able to look up deleted movie
		res = self.flask_app.get('/api/actors/Madeleine Stowe')
		self.assertEqual(res.status_code, 400)

	# Test unsuccessful DELETE request for actor
	def test_delete_actor_invalid(self):
		res = self.flask_app.delete('/api/actors/some_actor')
		# should fail
		self.assertEquals(res.status_code, 400)







if __name__ == '__main__':
    unittest.main()