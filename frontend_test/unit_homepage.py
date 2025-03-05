import requests
from bs4 import BeautifulSoup
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestKnowledgePass(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:8000"
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            logging.info(f"Loaded page successfully from {self.url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to load page: {e}")
            self.fail(f"Failed to load page: {e}")

    def test_title(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        title = self.soup.title.string
        self.assertEqual(title, "Knowledge Pass")
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_search_input_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        search_input = self.soup.find('input', {'id': 'search-input'})
        self.assertIsNotNone(search_input)
        self.assertEqual(search_input.get('placeholder'), "Search for jobs...")
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_search_button_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        search_button = self.soup.find('button', {'class': 'search-button'})
        self.assertIsNotNone(search_button)
        self.assertEqual(search_button.text, "Search")
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_particles_js_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        particles_js_div = self.soup.find('div', {'id': 'particles-js'})
        self.assertIsNotNone(particles_js_div)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_suggestions_box_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        suggestions_box = self.soup.find('div', {'id': 'suggestions-box'})
        self.assertIsNotNone(suggestions_box)
        self.assertEqual(suggestions_box.get('style'), None)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_h1_contains_text(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        h1 = self.soup.find('h1')
        self.assertIsNotNone(h1)
        self.assertTrue("สวัสดี เพื่อน ๆ อยากจะไปฝึกงานอะไรกัน" in h1.text)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_search_container_exists(self):
        logging.info(f"Running test: {self._testMethodName}")
        search_container = self.soup.find('div', {'class': 'search-container'})
        self.assertIsNotNone(search_container)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

if __name__ == '__main__':
    unittest.main()