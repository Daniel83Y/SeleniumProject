from unittest import TestCase
from selenium import webdriver
from random import choice, randint
from time import sleep
class SmartBearTest(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a browser object (Open the browser)
        self.driver = webdriver.Chrome()
        # Go to the required URL
        self.driver.get("https://bearstore-testsite.smartbear.com")
        # Maximize the window
        self.driver.maximize_window()
        # Define a timeout: In case an element is not found - wait 10 seconds
        self.driver.implicitly_wait(10)
        #self.home_page = PetsHomePage(self.driver)

    def tearDown(self):
        """Clean up after the test."""
        # Wait for 2 seconds before closing the browser
        sleep(2)
        # Close the browser
        self.driver.quit()

        """Check"""