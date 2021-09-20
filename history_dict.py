from datetime import datetime
from copy import deepcopy


class HistoryDict(dict):
    """
    Dict with the ability to remember previous overwritten values of specific key.

    Implemented methods:
        - setting new values;
        - getting recent values by default or old values by specified timestamp;
        - popping all/specific old values.

    General structure of the storage:
        STORAGE = {
            <key>: {
                <timestamp>: <value>,       # the oldest value
                <timestamp>: <value>,
                ...
                <timestamp>: <value>        # the newest value
            },
            <key>: { ... }, ...
        }
    """

    def __init__(self):
        self._storage = dict()

    def __setitem__(self, key, item):
        item_timestamp = datetime.now()

        if key in self._storage:
            self._storage[key][item_timestamp] = item
        else:
            self._storage[key] = {item_timestamp: item}

    def __getitem__(self, key):
        item_history = self._storage[key]
        return item_history[list(item_history)[-1]]

    def __len__(self):
        return len(self._storage)

    def __delitem__(self, key):
        del self._storage[key]

    def __contains__(self, key):
        return key in self._storage

    def clear(self):
        return self._storage.clear()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def has_key(self, key):
        return key in self._storage

    def keys(self):
        return self._storage.keys()

    def values(self):
        # TODO: fix method
        return NotImplemented

    def items(self):
        # TODO: fix method
        return NotImplemented

    def get(self, key):
        # TODO: fix signature - get(key, default=None)
        """
        Method for getting the most recent item.

        Returns None if key is not in the storage.
        """
        item_history = self._storage.get(key)

        return item_history[list(item_history)[-1]] if item_history else None

    def get_old(self, key, timestamp):
        # TODO: fix signature - get_old(key, default=None)
        """
        Method for getting value of specific key actual for specified timestamp.

        Returns None if key is not in the storage or timestamp is not found
        for specific item.
        """
        item_history = self._storage.get(key)

        if item_history is None:
            return

        filtered_timestamps = list(filter(lambda d: d <= timestamp, list(item_history)))

        if not len(filtered_timestamps):
            return

        return item_history.get(max(filtered_timestamps))

    def pop(self, key):
        # TODO: fix signature - pop(key, default=None)
        """
        Removes item and its history from the storage and returns them as a result.

        Throws KeyError if key is not in the storage.
        """
        return self._storage.pop(key)

    def pop_old(self, key, timestamp):
        """
        Removes item historical value from the storage by its timestamp.

        Throws KeyError if key is not in the storage.
        """
        return self._storage[key].pop(timestamp)

    def __str__(self):
        return self._storage.__str__()
