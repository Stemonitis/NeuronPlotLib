#!/usr/bin/env python
import csv


class LoadCsv:
    '''
        The input CSV file must be comma delimited and aligned on three columns.
        Each column represents one modality. Empty cells are counted as 0.
        Each row containing at least one value will be represented as a point.
    '''

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def ParseCsv(self) -> list:

        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            data, binarization = [], []
            for row in reader:
                data.append(
                    tuple(float(cell) if cell else 0 for cell in row[:3]))
                binarization.append(
                    tuple(True if cell else False for cell in row[3:6]))

        return data, binarization


if __name__ == '__main__':
    print('\nThis script can be used as an imported module only\n')
