from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	"""Ensure that flask was set correctly"""
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)

   #Ensure that login was set correctly
	def test_login_page_loads(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertTrue(b'Please login' in response.data)

	#Ensure that login behaves correctly given the correct credentials
	def test_correct_login(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login', data=dict(username='admin', password='admin'),
			follow_redirects = True
		)
		self.assertIn(b'You were logged in!', response.data)

	#Ensure that login behaves correctly given the incorrect credentials
	def test_incorrect_login(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login', data=dict(username='wrong', password='wrong'),
			follow_redirects = True
		)
		self.assertIn(b'Invalod credentails. Please try again ', response.data)
	
	#Ensure that logout behaves correctly 
	def test_logout(self):
		tester = app.test_client(self)
		tester.post(
			'/login', data=dict(username='admin', password='admin'),
			follow_redirects = True
		)
		response = tester.get('/logout', follow_redirects = True)
		self.assertIn(b'You were just logged out!', response.data)

	#Ensure that main page require login
	def test_main_route_requires_login(self):
		tester = app.test_client(self)
		response = tester.get('/', follow_redirects=True)
		self.assertTrue(b'You need to login first.' in response.data)
	
	#Ensure that posts show up in the login page
	def test_post_show_up(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login', data=dict(username='admin', password='admin'),
			follow_redirects = True
		)
		self.assertIn(b'Hello from the shell', response.data)


if __name__ == '__main__':
	unittest.main()
		