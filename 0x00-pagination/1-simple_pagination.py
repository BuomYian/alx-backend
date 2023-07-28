#!/usr/bin/env python3
"""
Helper function for pagination

This module contains a function to calculate the start and end index
for a given page number and page size, useful for pagination.

Example:
    index_range(1, 7) returns (0, 7)
    index_range(3, 15) returns (30, 45)
"""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a given page number and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get a page of the dataset based on pagination parameters.

        Args:
            page (int, optional): The page number (1-indexed). Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[List]: The page of the dataset as a list of rows (lists).
        """
        assert isinstance(
            page, int) and page > 0, "Page must be a positive integer."
        assert isinstance(
            page_size, int) and page_size > 0, "Page size must be a positive integer."

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
