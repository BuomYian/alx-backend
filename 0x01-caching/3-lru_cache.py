#!/usr/bin/env python3
""" LRUCache module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initializes the LRU cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using LRU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Discard the least recently used item using LRU algorithm
                lru_key = self.order.pop(0)
                self.cache_data.pop(lru_key)
                print("DISCARD:", lru_key)

            self.cache_data[key] = item
            self.order.append(key)

            # Move the newly added key to the end to signify it was most recently used
            self.order.remove(key)
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to signify it was most recently used
        self.order.remove(key)
        self.order.append(key)

        return self.cache_data[key]
