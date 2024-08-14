import csv
import random

num_rows = 1500

# Open a new CSV file to write the data
with open('modality_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    # writer.writerow(['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6'])

    # Generate the data
    for _ in range(num_rows):
        col1 = random.uniform(0, 1.8)
        col2 = random.uniform(0, 0.6)
        col3 = random.uniform(0, 1.8)

        col4 = 1 if col1 > 1.0 else ''
        col5 = 1 if col2 > .4 else ''
        col6 = 1 if col3 > .6 else ''

        writer.writerow([col1, col2, col3, col4, col5, col6])
