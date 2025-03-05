import unittest
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAdminDashboard(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:8000/admin_dashboard"
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

    def test_h1_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        h1 = self.soup.find('h1')
        self.assertIsNotNone(h1)
        self.assertEqual(h1.text, "Admin Dashboard")
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_grid_container_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        grid_container = self.soup.find('div', {'class': 'grid-container'})
        self.assertIsNotNone(grid_container)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_cards_exist(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        cards = self.soup.find_all('div', {'class': 'card'})
        self.assertEqual(len(cards), 3)
        card_titles = [card.find('h2').text for card in cards]
        self.assertIn("Job Nodes", card_titles)
        self.assertIn("Course Nodes", card_titles)
        self.assertIn("Skill Nodes", card_titles)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_button_group_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        button_group = self.soup.find('div', {'class': 'button-group'})
        self.assertIsNotNone(button_group)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_buttons_exist(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        buttons = self.soup.find_all('button', {'class': 'button'})
        self.assertEqual(len(buttons), 5)
        button_texts = [button.text for button in buttons]
        self.assertIn("Add New Course", button_texts)
        self.assertIn("Add New Job", button_texts)
        self.assertIn("Compile & Sync Data", button_texts)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_modals_exist(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        add_course_modal = self.soup.find('div', {'id': 'addCourseModal'})
        self.assertIsNotNone(add_course_modal)
        add_job_modal = self.soup.find('div', {'id': 'addJobModal'})
        self.assertIsNotNone(add_job_modal)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_modal_elements_exist(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        modal_content = self.soup.find('div', {'id': 'addCourseModal'}).find('div', {'class': 'modal-content'})
        self.assertIsNotNone(modal_content.find('span', {'class': 'close'}))
        self.assertIsNotNone(modal_content.find('h2'))
        self.assertIsNotNone(modal_content.find('input', {'id': 'courseName'}))
        self.assertIsNotNone(modal_content.find('textarea', {'id': 'courseDescription'}))
        self.assertIsNotNone(modal_content.find('input', {'id': 'courseImage'}))
        self.assertIsNotNone(modal_content.find('button', {'class': 'button'}))
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_particles_js_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        particles_js_div = self.soup.find('div', {'id': 'particles-js'})
        self.assertIsNotNone(particles_js_div)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

if __name__ == '__main__':
    unittest.main()