#!/usr/bin/env python3
"""
Helper function for pagination

This module contains a function to calculate the start and end index
for a given page number and page size, useful for pagination.

Example:
    index_range(1, 7) returns (0, 7)
    index_range(3, 15) returns (30, 45)
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a given page number and page size

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page

    Returns:
        Tuple[int, int]: A tuple containing the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
