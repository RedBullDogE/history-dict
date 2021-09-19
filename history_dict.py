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

    def load_test_data(self, test_data):
        self._storage.update(test_data)

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
        return self._storage.values()

    def items(self):
        return self._storage.items()

    def get(self, key):
        item_history = self._storage.get(key)

        if item_history is None:
            return

        if len(item_history) == 0:
            return

        return item_history[list(item_history)[-1]]

    def get_old(self, key, timestamp):
        item_history = self._storage.get(key)

        if item_history is None:
            return

        return item_history.get(timestamp)

    def pop(self, key):
        return self._storage.pop(key)

    def pop_old(self, key, timestamp):
        return self._storage[key].pop(timestamp)

    def __str__(self):
        return self._storage.__str__()
