from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Smartbear_main_page import BearStoreMainPage
from SmartBear_Cart_Page import BearStoreCartPage
from Smartbear_Login_Page import BearStoreLoginPage
from Smartbear_toolbar import BearStoreToolBar
from Smartbear_Category_page import BearStoreCategoryPage
from SmartBear_Product_Page import BearStoreProductPage
from SmartBear_CartPopUp import BearStoreCartPopUp
from SmartBear_Checkout_Page import BearStoreCheckoutPage
from selenium.webdriver.remote.webelement import WebElement
import re
from random import choice, randint
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


class SmartBearTest(TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Initialize the Chrome browser
        self.driver = webdriver.Edge()
        # Navigate to the BearStore test site
        self.driver.get("https://bearstore-testsite.smartbear.com")
        # Maximize the browser window for better visibility
        self.driver.maximize_window()
        # Set implicit wait for elements to load
        self.driver.implicitly_wait(10)

        # Initialize page objects for various site components
        self.main_page = BearStoreMainPage(self.driver)
        self.toolbar = BearStoreToolBar(self.driver)
        self.category_page = BearStoreCategoryPage(self.driver)
        self.product_page = BearStoreProductPage(self.driver)
        self.cart_popup = BearStoreCartPopUp(self.driver)
        self.cart_page = BearStoreCartPage(self.driver)
        self.login_page = BearStoreLoginPage(self.driver)
        self.check_page = BearStoreCheckoutPage(self.driver)
    #Test 1
    def test_page_transitions(self):
        """
        Test navigation and transitions between category, product, and homepage.
        """
        # Choose a random category and click it
        selected_products = set()  # Track selected products to avoid duplicates
        category_name = choice(self.main_page.categories()).text
        self.main_page.click_category(category_name)

        # Assert that the selected category name matches the current page
        self.assertEqual(category_name, self.category_page.get_category_name().text)

        # Scroll down a bit on the category page
        self.driver.execute_script("window.scrollBy(0, 100);")

        # Choose a random product and click it
        product = choice(self.category_page.product()).text
        self.category_page.click_product(product)

        # Assert that the selected product name matches the current product page
        self.assertEqual(self.product_page.get_product_name().text, product)

        # Navigate back to the category page via breadcrumbs
        self.product_page.inactive_breadcrumbs()[-1].click()

        # Return to the homepage by clicking the toolbar logo
        self.toolbar.toolbar_logo_click()
        # Return to the cart by clicking the cart logo
        self.toolbar.toolbar_cart_click()
        self.clean_cart()
    #Test 2
    def test_add_to_cart(self):
        """
        Adds multiple products to the shopping cart and verifies quantities.
        """
        selected_products = set()  # Track selected products to avoid duplicates
        sum_quantity = 0

        # Add first product
        quantity = randint(2, 5)
        sum_quantity += quantity
        self.add_random_product_to_cart(quantity)

        # Return to homepage
        self.toolbar.toolbar_logo_click()

        # Add second product with a new random quantity
        quantity = randint(2, 5)  # Ensure random quantity instead of incrementing
        sum_quantity += quantity
        self.add_random_product_to_cart(quantity)

        # Ensure UI has updated before checking cart quantity
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.cart_popup.cart_total_items_amount() == str(sum_quantity)
        )

        # Verify the total cart quantity
        self.assertEqual(self.cart_popup.cart_total_items_amount(), str(sum_quantity))

        # Empty the cart at the end of the test
        self.clean_cart()

    # Test 3
    def test_add_to_cart_3(self):
        """
        Adds multiple products to the shopping cart and verifies quantities, names, and prices.
        Ensures no duplicate products are selected.
        """
        expected_quantities = []
        expected_product_names = []
        expected_prices = []
        selected_products = set()  # Track selected products to avoid duplicates

        # Add two unique products to the cart
        for _ in range(2):
            quantity = randint(2, 10)
            expected_quantities.append(quantity)
            self.add_random_product_to_cart(quantity, True, selected_products)  # Ensure unique selection
            expected_product_names.append(self.product_page.get_product_name().text)
            expected_prices.append(self.product_page.get_product_price().text)
            self.toolbar.toolbar_logo_click()

        # Add a third unique product to the cart
        quantity = randint(2, 5)
        expected_quantities.append(quantity)
        self.add_random_product_to_cart(quantity, False, selected_products)  # Ensure unique selection
        expected_product_names.append(self.product_page.get_product_name().text)
        expected_prices.append(self.product_page.get_product_price().text)

        actual_names = self.cart_popup.cart_product_name()
        actual_prices = self.cart_popup.cart_product_price()
        actual_quantities = self.cart_popup.cart_product_quantity()

        for i in range(len(actual_names)):
            # Check that the names of the products are correct
            self.assertEqual(expected_product_names[i], actual_names[3 - i - 1].text)
            # Check that the prices of the products are correct
            self.assertEqual(expected_prices[i], actual_prices[3 - i - 1].text)
            # Check that the quantities of the products are correct
            self.assertEqual(str(expected_quantities[i]), actual_quantities[3 - i - 1].get_attribute('value'))
            print('True')

        self.clean_cart()

    # Test 4
    def test_add_to_cart_and_remove(self):
        """
        Adds multiple products to the shopping cart, removes the first item added, and verifies that only the second item remains.
        """
        selected_products = set()  # Track selected products to avoid duplicates
        expected_quantities = []
        for i in range(2):
            # Add the first product
            quantity = randint(2, 10)
            expected_quantities.append(quantity)
            self.add_random_product_to_cart(quantity, True)
            self.toolbar.toolbar_logo_click()
        self.toolbar.toolbar_cart_click()

        # Remove the first item added (which is last in the cart list)
        remaining_quantity = str(expected_quantities[-1])
        self.remove_first_cart_item()
        #Wait until UI update
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.cart_popup.cart_total_items_amount() == remaining_quantity)
        # Verify the updated cart quantity
        self.assertEqual(self.cart_popup.cart_total_items_amount(), remaining_quantity)

        # Get the remaining cart product details
        remaining_quantities = [q.get_attribute('value') for q in self.cart_popup.cart_product_quantity()]

        # Ensure only the second product remains
        self.assertEqual(remaining_quantities[0], str(expected_quantities[1]),
                         "Wrong quantity for the remaining product")

        self.clean_cart()

    # Test 5
    def test_cart_transitions(self):
        # Add a random product to the cart, specifying the quantity as 2.
        selected_products = set()  # Track selected products to avoid duplicates
        self.add_random_product_to_cart(2)

        # Verify that the cart popup shows the total items amount is not empty after adding the product.
        self.assertNotEqual(self.cart_popup.cart_total_items_amount(), '',
                            "Cart total items amount should not be empty after adding a product.")

        # Remove any blocking element that might prevent interaction with the cart (assuming this method exists).
        self.remove_cart_blocker()

        # Simulate a click on the toolbar cart button to open the cart.
        self.toolbar.toolbar_cart_click()

        # Verify that the cart popup shows the total items amount is not empty after clicking the cart button.
        self.assertNotEqual(self.cart_popup.cart_total_items_amount(), '',
                            "Cart total items amount should not be empty after clicking the cart button.")

        # Click on the "Go to cart" button and navigate to the shopping cart page.
        self.cart_popup.go_to_cart()

        # Verify that the shopping cart page is displayed by checking if the shopping cart element is found.
        self.assertIsNotNone(self.cart_page.find_shopping_cart(),
                             "Shopping cart page should be displayed after clicking 'Go to cart'.")
        self.cart_page.empty_cart()

    # Test 6
    def test_3_products_details(self):
        """
        Adds three different products to the shopping cart with different quantities.
        Verifies that the total order amount in both the cart popup and the full cart page
        matches the expected total based on product prices and quantities.
        Prints the name, quantity, and price of each product in the cart.
        Ensures no duplicate products are selected.
        """
        selected_products = set()  # Track selected products to avoid duplicates

        for _ in range(2):
            quantity = randint(2, 10)
            self.add_random_product_to_cart(quantity, True, selected_products)  # Ensure unique selection
            self.toolbar.toolbar_logo_click()

            # Add a third unique product to the cart
        quantity = randint(2, 5)
        self.add_random_product_to_cart(quantity, False, selected_products)  # Ensure unique selection

        # GET Name, Price, Quantity from Popup Cart
        actual_names_popup = [name.text.strip() for name in self.cart_popup.cart_product_name()]
        actual_unit_prices_popup = [self.extract_price(price) for price in self.cart_popup.cart_product_price()]
        actual_quantities_popup = [qty.get_attribute('value') for qty in self.cart_popup.cart_product_quantity()]

        # Extract the subtotal from the cart popup
        cart_subtotal = float(self.extract_price(self.cart_popup.find_subtotal()))

        # Go to the full cart page
        self.cart_popup.go_to_cart()

        # GET Name, Price, Quantity from Cart Page
        actual_names_cart_page = [name.text.strip() for name in self.cart_page.cart_page_product_name()]
        actual_unit_prices_cart_page = [self.extract_price(price) for price in
                                        self.cart_page.cart_page_product_price()]  # FIXED: Now correctly gets only unit prices
        actual_subtotal_prices_cart_page = [self.extract_price(price) for price in
                                            self.cart_page.cart_page_product_subtotal_price()]
        actual_quantities_cart_page = [qty.get_attribute('value') for qty in
                                       self.cart_page.cart_page_product_quantity()]

        # Calculate the total price from the cart page
        total_price = sum(float(price) for price in actual_subtotal_prices_cart_page)

        # Adjust popup prices to match cart page subtotal prices
        adjusted_popup_prices = [float(actual_unit_prices_popup[i]) * int(actual_quantities_popup[i])
                                 for i in range(len(actual_unit_prices_popup))]

        # Log extracted details for debugging
        logging.info("\n=== Popup Cart Details ===")
        for i in range(len(actual_names_popup)):
            logging.info(
                f"Product: {actual_names_popup[i]}, Unit Price: {actual_unit_prices_popup[i]}, Quantity: {actual_quantities_popup[i]}")

        logging.info("\n=== Cart Page Details ===")
        for i in range(len(actual_names_cart_page)):
            logging.info(f"Product: {actual_names_cart_page[i]}, Unit Price: {actual_unit_prices_cart_page[i]}, "
                         f"Subtotal Price: {actual_subtotal_prices_cart_page[i]}, Quantity: {actual_quantities_cart_page[i]}")

        logging.info(f"\nSubtotal from Cart Popup: {cart_subtotal}")
        logging.info(f"Total Price from Cart Page: {total_price}")

        # Verify that product names match in both popup cart and cart page
        self.assertEqual(actual_names_popup, actual_names_cart_page,
                         "Mismatch in product names between popup and cart page.")

        # Verify that **only** unit prices are matched correctly
        self.assertEqual(len(actual_unit_prices_popup), len(actual_unit_prices_cart_page),
                         "Mismatch in the number of unit prices extracted.")
        self.assertEqual(actual_unit_prices_popup, actual_unit_prices_cart_page,
                         "Mismatch in unit prices between popup and cart page.")
        # Convert both lists to float and round to two decimal places for precise comparison
        adjusted_popup_prices = [round(float(price), 2) for price in adjusted_popup_prices]
        actual_subtotal_prices_cart_page = [round(float(price), 2) for price in actual_subtotal_prices_cart_page]
        # Verify that adjusted popup prices match subtotal prices in cart page
        self.assertEqual(adjusted_popup_prices, actual_subtotal_prices_cart_page,
                         "Mismatch in total product prices between popup and cart page.")

        # Verify that product quantities match in both popup cart and cart page
        self.assertEqual(actual_quantities_popup, actual_quantities_cart_page,
                         "Mismatch in product quantities between popup and cart page.")

        # Verify that total price in cart page matches the subtotal in popup
        self.assertEqual(total_price, cart_subtotal, "Mismatch in total price between cart popup and cart page.")

        # Empty the cart at the end of the test
        self.cart_page.empty_cart()

    # Test 7
    def test_change_products_in_cart(self):
        """
        Adds two products to the shopping cart, navigates to the cart page, and updates the quantities of both products.
        Verifies that the total price for each product is updated correctly based on the new quantity.
        Ensures the overall total price in the cart is updated accordingly.
        Checks that the updated total price is reflected correctly in the cart popup.
        """
        selected_products = set()  # Track selected products to avoid duplicates
        # self.add_random_product_to_cart(2)
        # self.clean_cart()
        # Add two unique products to the cart
        for _ in range(2):
            quantity = randint(2, 10)
            self.add_random_product_to_cart(quantity, True, selected_products)  # Ensure unique selection
            self.toolbar.toolbar_logo_click()

        # Navigate to the cart
        self.toolbar.toolbar_cart_click()
        self.cart_popup.go_to_cart()

        # Find the quantities of the products in the cart
        prod_quantities = self.cart_page.cart_page_product_quantity()

        # Update the quantities of the products in the cart
        for quantity in prod_quantities:
            self.cart_page.change_quantity(quantity, randint(2, 10))

        # Find the updated quantities of the products
        updated_quantities = self.cart_page.cart_page_product_quantity()

        # Find the subtotal prices of the products in the cart
        cart_prod_sub_total = self.cart_page.cart_page_product_subtotal_price()

        # Verify that the total price for each product is updated correctly
        for i in range(len(updated_quantities)):
            product_price = float(self.extract_price(self.cart_page.cart_page_product_price()[i]))
            updated_quantity = updated_quantities[i].text.strip()

            # Check if updated_quantity is not empty before converting to float
            if updated_quantity:
                updated_quantity = float(updated_quantity)
                expected_sub_total = product_price * updated_quantity
                actual_sub_total = float(self.extract_price(cart_prod_sub_total[i]))
                self.assertEqual(expected_sub_total, actual_sub_total,
                                 f"Expected subtotal: {expected_sub_total}, but got: {actual_sub_total}")

        # Verify the overall total price in the cart
        total_cost_element = self.cart_page.cart_summary_total()
        total_cost = float(self.extract_price(total_cost_element))
        sum_cart_total = sum(float(self.extract_price(sub_total)) for sub_total in cart_prod_sub_total)
        self.assertEqual(total_cost, sum_cart_total,
                         f"Expected total cost: {total_cost}, but got: {sum_cart_total}")
        self.cart_page.empty_cart()
    # Test 8
    def test_complete_order(self):
        """complete  order including login"""
        selected_products = set()  # Track selected products to avoid duplicates
        # self.add_random_product_to_cart(2)
        # self.clean_cart()
        # Add two unique products to the cart
        username = "DanielTeslerTest"
        password = "DanielTest5309"
        for _ in range(2):
            quantity = randint(2, 10)
            self.add_random_product_to_cart(quantity, True, selected_products)  # Ensure unique selection
            self.toolbar.toolbar_logo_click()
        self.toolbar.toolbar_cart_click()
        self.cart_popup.go_to_checkout()
        self.login_page.login_input_sendkeys(username)
        self.login_page.password_input_sendkeys(password)
        self.login_page.log_in_button()
        self.cart_page.cart_checkout()
        self.check_page.click_billing_address()
        self.check_page.click_shipping_address()
        self.check_page.confirm_shipping_method()
        self.check_page.confirm_payment_method()
        self.check_page.agree_to_terms()
        self.check_page.confirm_checkout()
        order_number = self.check_page.get_order_number().text
        self.check_page.go_to_order_details()
        self.assertEqual(order_number, self.check_page.get_completed_order_number())
        self.toolbar.toolbar_cart_click()
        self.assertEqual(self.cart_popup.cart_total_items_amount(), '0')
    # Test 9
    def test_login_logout(self):
        """
        Logs into the website and verifies that the login was successful.
        Logs out of the website and confirms that the logout was completed correctly.
        """

        # Define login credentials
        username = "DanielTeslerTest"
        password = "DanielTest5309"

        # Click the login button on the toolbar to open the login page
        self.toolbar.toolbar_login_click()

        # Enter the username and password into the login form
        self.login_page.login_input_sendkeys(username)
        self.login_page.password_input_sendkeys(password)

        # Click the login button to submit the form
        self.login_page.log_in_button()

        # Verify that the account name displayed in the toolbar matches the logged-in user
        self.assertEqual(self.toolbar.toolbar_account_name().text.lower(), username.lower())

        # Click on the account menu to open logout options
        self.toolbar.toolbar_account_click()

        # Click the logout button
        self.toolbar.toolbar_logout()

        # Verify that the account name changes back to "Log in" after logging out
        self.assertEqual(self.toolbar.toolbar_account_name().text.lower(), "Log in".lower())

    # def test_clean_cart(self):
    #     self.add_random_product_to_cart(2)
    #     self.clean_cart()



    def extract_price(self, element: WebElement):
        """
            Extracts the numeric price from a given element.
            """
        if element is None:
            return None
        text = element.text.replace(',', '')
        text = text.strip()
        match = re.search(r"\d+.\d+", text)  # Looks for a floating-point number
        return match.group() if match else None  # Return the matched number as a string

    def add_random_product_to_cart(self, quantity, mouse_click=False, selected_products=None):
        """
        Adds a random product from a random category to the shopping cart
        with a random quantity, ensuring no duplicate selections.
        """

        if selected_products is None:
            selected_products = set()  # Initialize set if not provided
        while True:
            # Choose a random category and click it
            category_name = choice(self.main_page.categories()).text
            while "Gift" in category_name:
                category_name = choice(self.main_page.categories()).text
            self.main_page.click_category(category_name)

            # Scroll down slightly on the category page
            self.driver.execute_script("window.scrollBy(0, 350);")

            # Get available products and remove already selected ones
            products = [p.text for p in self.category_page.product()]
            available_products = list(set(products) - selected_products)

            if not available_products:
                self.toolbar.toolbar_logo_click()
                continue

            product = choice(available_products)  # Pick a unique product
            selected_products.add(product)  # Track selected product

            self.category_page.click_product(product)
            self.driver.execute_script("window.scrollBy(0, 200);")

            if 'Converse' in product:
                self.product_page.choose_color()

            self.product_page.change_quantity(quantity)
            self.product_page.add_to_cart()

            if mouse_click:
                self.remove_cart_blocker()
            break

    def clean_cart(self):
        while True:
            try:
                # Wait until all "remove" buttons are present
                cart_items = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-to-danger"))
                )
                if not cart_items:
                    break  # Exit loop if there are no more items in the cart
                # Click the "remove" button for the first item in the cart
                cart_items[0].click()
                # Wait until the item is no longer present in the DOM before proceeding
                WebDriverWait(self.driver, 2).until(
                    EC.staleness_of(cart_items[0])
                )
            except:
                break  # Exit the function if there are no more items or an exception occurs

    def remove_first_cart_item(self):
        """
        Removes the first item added to the cart, which appears last in the cart list.
        """
        try:
            # Wait for the cart items to load
            cart_items = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "offcanvas-cart-item"))
            )

            if cart_items:
                # Select the last item in the cart, since the first added product is last in the list
                last_item = cart_items[-1]
                remove_button = last_item.find_element(By.CLASS_NAME, "btn-to-danger")
                remove_button.click()

                # Wait until the last item is removed from the cart
                WebDriverWait(self.driver, 2).until(EC.staleness_of(last_item))

        except Exception as e:
            print(f"Error removing the first added cart item: {e}")

    def remove_cart_blocker(self):
        """
        Removes the cart blocker overlay using JavaScript.
        """
        self.driver.execute_script("""
            var blocker = document.querySelector('.canvas-blocker.canvas-slid-able');
            if (blocker) blocker.remove();
        """)

    def tearDown(self):
        """Clean up after the test."""
        # Wait for 2 seconds to observe results (if needed)
        sleep(2)
        # Open Shopping cart popup and remove all items
        # Close the browser to free up resources
        self.driver.quit()
