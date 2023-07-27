#!/usr/bin/env python3
"""
FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """
        Initializes the FIFO cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache using FIFO algorithm
        """
        if key is None or item is None:
             return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Discard the first item using FIFO algorithm
            first_item = self.order.pop(0)
            self.cache_data.pop(first_item)
            print("DISCARD:", first_item)

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
