import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestSearchResultsPage(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:8000/results?q=Full%20Stack%20JavaScript"
        self.driver = webdriver.Safari()
        self.driver.get(self.url)
        logging.info(f"Loaded page successfully from {self.url}")

    def tearDown(self):
        self.driver.quit()

    def test_title(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        self.assertEqual(self.driver.title, "Knowledge Pass")
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_h1_contains_text(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        h1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        self.assertTrue("Search Results" in h1.text)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_sankey_chart_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        sankey_chart = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "sankey_multiple"))
        )
        self.assertIsNotNone(sankey_chart)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_job_results_exist(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        job_results = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "job-result"))
        )
        self.assertTrue(len(job_results) > 0)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_summary_text_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        summary_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary-text"))
        )
        self.assertIsNotNone(summary_text)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_suggestion_text_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        suggestion_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "suggestion-text"))
        )
        self.assertIsNotNone(suggestion_text)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_export_button_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        export_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "export-button"))
        )
        self.assertIsNotNone(export_button)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

    def test_back_to_home_link_exists(self):
        logging.info(f"[Running test]: {self._testMethodName}")
        back_to_home_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Back to Home"))
        )
        self.assertIsNotNone(back_to_home_link)
        logging.info(f"✅ Test {self._testMethodName} passed.\n")

if __name__ == '__main__':
    unittest.main()