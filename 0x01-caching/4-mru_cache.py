#!/usr/bin/env python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initializes the MRU cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using MRU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Discard the most recently used item using MRU algorithm
                if self.order:
                    mru_key = self.order.pop()
                    self.cache_data.pop(mru_key)
                    print("DISCARD:", mru_key)

            self.cache_data[key] = item

            # Move the newly added key to the end
            if key in self.order:
                self.order.remove(key)
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

        return self.cache_data[key]
