import unittest
import os

class TestFileSize(unittest.TestCase):
    def test_encoded_file_size(self):
        # Get the path to a file
        file_path = './CBS_DecodeTransactionData/transaction_data_encoded'
        
        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Get the size of the file
        file_size = os.path.getsize(file_path)
        
        # Check if the file size is greater than zero
        self.assertGreater(file_size, 0)

    def test_decoded_file_size(self):
        # Get the path to a file
        file_path = './transaction_data_decoded'
        
        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Get the size of the file
        file_size = os.path.getsize(file_path)
        
        # Check if the file size is greater than zero
        self.assertGreater(file_size, 0)
