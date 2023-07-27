#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initializes the LFU cache
        """
        super().__init__()
        self.frequencies = {}  # To store the frequency of each key
        self.min_frequency = 0
        self.order = []  # To store the order of key access

    def put(self, key, item):
        """
        Add an item in the cache using LFU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Discard the least frequency used item using LFU algorithm
                lfu_keys = [
                    k for k in self.frequencies if self.frequencies[k] == self.min_frequency]
                if not lfu_keys:
                    # If no keys with the least frequency, use LRU to break the tie
                    lru_key = min(
                        self.order, key=lambda k: self.order.index(k))
                    lfu_keys = [
                        k for k in self.frequencies if self.frequencies[k] == self.frequencies[lru_key]]

                lfu_key = lfu_keys[0]
                self.cache_data.pop(lfu_key)
                self.frequencies.pop(lfu_key)
                self.order.remove(lfu_key)
                print("DISCARD:", lfu_key)

            self.cache_data[key] = item
            self.frequencies[key] = 1
            self.order.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Update the frequency of the accessed key
        self.frequencies[key] += 1

        # Move the accessed key to the end
        self.order.remove(key)
        self.order.append(key)

        return self.cache_data[key]
