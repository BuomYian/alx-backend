#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Union, Tuple


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
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

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

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Get hypermedia information for the dataset based on the start index.

        Args:
            index (int, optional): The start index of the return page. Defaults to None.
            page_size (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Dict[str, Union[int, List[List], None]]: A dictionary containing hypermedia information.
        """
        assert isinstance(
            index, int) and index >= 0, "Index must be a non-negative integer."
        assert isinstance(
            page_size, int) and page_size > 0, "Page size must be a positive integer."

        indexed_dataset = self.indexed_dataset()
        max_index = len(indexed_dataset) - 1

        if index is None or index > max_index:
            index = 0

        if index > max_index:
            return {
                "index": index,
                "data": [],
                "page_size": page_size,
                "next_index": None
            }

        start_page, _ = index_range(index // page_size + 1, page_size)
        end_page, _ = index_range(
            (index + page_size - 1) // page_size + 1, page_size)

        data = [indexed_dataset[i]
                for i in range(start_page, end_page + 1) if i in indexed_dataset]

        next_index = min(index + page_size, max_index + 1)

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index
        }
