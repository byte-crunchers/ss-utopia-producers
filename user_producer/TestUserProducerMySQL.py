import unittest

from mysql.connector import MySQLConnection

from UserProducer import *


# This class Tests the user_producer and related helper functions
class TestClass(unittest.TestCase):

    # This method tests the connect method from DatabaseHelper.py
    def test_connect(self):
        conn1 = connect_mysql()
        self.assertIsNotNone(conn1)  # Test that connection is not null
        self.assertIsInstance(conn1, MySQLConnection)  # Test that connection is type MySQlConnection
        conn1.close()
        self.assertEqual(conn1.is_connected(), False)  # Test that connection is closed

    # This method tests the count, clear and add test user methods from DatabaseHelper.py
    def test_count_clear_add(self):
        clear_table("users")  # Clear the table
        self.assertEqual(count_rows("users"), 0)  # Test that count is 0
        add_test_user()  # Add a single user
        self.assertEqual(count_rows("users"), 1)  # Test that count is now 1
        clear_table("users")  # Clear the table again
        self.assertEqual(count_rows("users"), 0)  # Test that count is 0 again

    # This method tests the user producer and user data generator
    def test_user_producer_small(self):
        conn_small = connect_mysql()
        users_list = get_user_data(10)  # Generate 10 dummy users and store in list
        self.assertEqual(len(users_list), 10)  # Test that the list contains 100 entries
        clear_table("users")  # Clear table
        self.assertEqual(count_rows("users"), 0)  # Test that table is empty
        populate_users(users_list, conn_small, "users")  # Populate the database with the users
        self.assertEqual(count_rows("users"), 10)  # Test that there are now 10 rows in users
        clear_table("users")  # Clear the table
        self.assertEqual(count_rows("users"), 0)  # Test that table is empty
        conn_small.close()

    # This method tests the user producer and user data generator
    def test_user_producer_large(self):
        conn_large = connect_mysql()
        users_list = get_user_data(100)  # Generate 100 dummy users and store in list
        self.assertEqual(len(users_list), 100)  # Test that the list contains 100 entries
        clear_table("users")  # Clear table
        self.assertEqual(count_rows("users"), 0)  # Test that table is empty
        populate_users(users_list, conn_large, "users")  # Populate the database with the users
        self.assertEqual(count_rows("users"), 100)  # Test that there are now 100 rows in users
        users_list2 = get_user_data(1000)  # Generate new list of 1000 dummy users
        populate_users(users_list2, conn_large, "users")
        self.assertEqual(count_rows("users"), 1100)  # Test that the new list was added
        clear_table("users")  # Clear the table
        self.assertEqual(count_rows("users"), 0)  # Test that table is empty
        conn_large.close()

    # This method tests duplicate username or email
    # exception handling by adding a large number of rows (may take a minute)
    def test_user_producer_stress(self):
        conn_stress = connect_mysql()
        populate_users(get_user_data(10000), conn_stress, "users")  # Add 10,000 users to the database
        self.assertEqual(count_rows("users"), 10000)  # Test the users were all added
        clear_table("users")  # Clear the table
        self.assertEqual(count_rows("users"), 0)  # Test that table is empty
        conn_stress.close()


if __name__ == '__main__':
    unittest.main()

