import csv
import pytest
import unittest


class Test_Check_File_Contents(unittest.TestCase):
    def test_preferred_transaction_csv_has_rows(self):
        csv_file_path = './preferred_transaction_details.csv'
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            num_rows = sum(1 for row in reader)
        assert num_rows > 15

    def test_preferred_transaction_csv_has_contents(self):
        csv_file_path = './preferred_transaction_details.csv'
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            num_rows = sum(1 for row in reader)
        assert num_rows > 0   

    def test_pensioner_csv_has_rows(self):
        csv_file_path = './bonus_to_pensioners.csv'
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            num_rows = sum(1 for row in reader)
        assert num_rows > 740

    def test_pensioner_csv_has_contents(self):
            csv_file_path = './bonus_to_pensioners.csv'
            with open(csv_file_path, 'r') as f:
                reader = csv.reader(f)
                num_rows = sum(1 for row in reader)
            assert num_rows > 0   

    def test_decoded_csv_has_rows(self):
        csv_file_path = './transaction_data.csv'
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            num_rows = sum(1 for row in reader)
        assert num_rows > 1048570

    def test_decoded_csv_has_contents(self):
            csv_file_path = './transaction_data.csv'
            with open(csv_file_path, 'r') as f:
                reader = csv.reader(f)
                num_rows = sum(1 for row in reader)
            assert num_rows > 0               