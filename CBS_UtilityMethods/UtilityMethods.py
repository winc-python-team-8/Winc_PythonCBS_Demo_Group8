import csv
import os


def is_file_valid(file_path):
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.stat(file_path).st_size != 0


# to create csv file from data fetched from database
def create_csv_file(csv_write_file_name, header_list, in_file_data):
    with open(csv_write_file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header_list)
        writer.writeheader()
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerows(in_file_data)

