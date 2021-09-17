from datetime import datetime


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
                'newest': (<timestamp>, <value>),   # the most recent value
                <timestamp>: <value>,               # old values
                <timestamp>: <value>,
                ...
            },
            <key>: { ... }, ...
        }
    """

    def __init__(self):
        self._storage = dict()

    def load_test_data(self, test_data):
        self._storage.update(test_data)

    def __setitem__(self, key, item):
        now = datetime.now()
        item_timestamp = datetime(now.year, now.month, now.day, now.hour)

        if key not in self._storage:
            self._storage[key] = {"newest": (item_timestamp, item)}
            return

        if item_timestamp == self._storage[key]["newest"][0]:
            self._storage[key]["newest"] = (item_timestamp, item)
        else:
            old_timestamp, old_item = self._storage[key]["newest"]
            self._storage[key][old_timestamp] = old_item
            self._storage[key]["newest"] = (item_timestamp, item)
        
            

    def __getitem__(self, key):
        return self._storage[key]["newest"][1]

    def __len__(self):
        return len(self._storage)

    def __delitem__(self, key):
        del self._storage[key]

    def __contains__(self, key):
        return key in self._storage

    def clear(self):
        return self._storage.clear()

    def copy(self):
        return self._storage.copy()

    def has_key(self, key):
        return key in self._storage

    def update(self, key):
        raise NotImplemented

    def keys(self):
        return self._storage.keys()

    def values(self):
        return self._storage.values()

    def items(self):
        return self._storage.items()

    def get(self, key):
        item_dict = self._storage.get(key)
        
        if item_dict is None:
            return

        return item_dict.get("newest")[1]

    def get_old(self, key, timestamp):
        storage_item = self._storage.get(key)
        
        if storage_item is None:
            return

        return (
            storage_item["newest"][1]
            if storage_item["newest"][0] == timestamp
            else storage_item.get(timestamp)
        )

    def pop(self, key):
        return self._storage.pop(key)

    def pop_old(self, key, timestamp):
        return self._storage[key].pop(timestamp)

    def __str__(self):
        return self._storage.__str__()
