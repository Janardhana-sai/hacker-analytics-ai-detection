"""
Sample: Complex Data Structure (LRU Cache) Generated in AI Assistant Style.
Includes Doubly-Linked Node class, step-by-step methods, and exhaustive documentation.
"""

from typing import Dict, Optional


class DoublyLinkedNode:
    """Represents a bidirectional node within the LRU cache linked list."""

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key: int = key
        self.value: int = value
        self.prev: Optional["DoublyLinkedNode"] = None
        self.next: Optional["DoublyLinkedNode"] = None


class LRUCacheAI:
    """
    Least Recently Used (LRU) Cache implementation with O(1) get and put time complexity.
    Maintains a hash map for lookups and a doubly linked list for eviction order.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize the LRU Cache with a specified capacity limit.

        Args:
            capacity: Positive integer capacity of cache.
        """
        self.capacity: int = capacity
        self.cache_map: Dict[int, DoublyLinkedNode] = {}

        # Dummy head and tail nodes to simplify boundary operations
        self.head: DoublyLinkedNode = DoublyLinkedNode()
        self.tail: DoublyLinkedNode = DoublyLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_to_head(self, node: DoublyLinkedNode) -> None:
        """Insert a node immediately after the pseudo head."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: DoublyLinkedNode) -> None:
        """Unlink an existing node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _move_to_head(self, node: DoublyLinkedNode) -> None:
        """Move an accessed node to the most recently used head position."""
        self._remove_node(node)
        self._add_node_to_head(node)

    def get(self, key: int) -> int:
        """
        Retrieve value associated with key. Updates recency order.

        Args:
            key: Target search key.

        Returns:
            The associated integer value, or -1 if not found.
        """
        # Step 1: Check if key exists in cache
        if key not in self.cache_map:
            return -1

        # Step 2: Retrieve target node
        node = self.cache_map[key]

        # Step 3: Mark as recently used by moving to head
        self._move_to_head(node)

        # Step 4: Return node value
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair. Evicts least recently used node if over capacity.

        Args:
            key: Storage key.
            value: Integer value to store.
        """
        if key in self.cache_map:
            node = self.cache_map[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = DoublyLinkedNode(key=key, value=value)
            self.cache_map[key] = new_node
            self._add_node_to_head(new_node)

            if len(self.cache_map) > self.capacity:
                # Evict least recently used from tail
                lru_node = self.tail.prev
                if lru_node and lru_node != self.head:
                    self._remove_node(lru_node)
                    del self.cache_map[lru_node.key]

