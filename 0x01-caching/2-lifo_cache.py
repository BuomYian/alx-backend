#!/usr/bin/env python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initializes the LIFO cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using LIFO algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Discard the last item using LIFO algorithm
                last_key = self.order.pop()
                self.cache_data.pop(last_key)
                print("DISCARD:", last_key)

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
