from datetime import datetime


class HistoryDict:
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

        if key in self._storage:
            if item_timestamp == self._storage[key]["newest"][0]:
                self._storage[key]["newest"] = (item_timestamp, item)
            else:
                old_timestamp, old_item = self._storage[key]["newest"]
                self._storage[key][old_timestamp] = old_item
                self._storage[key]["newest"] = (item_timestamp, item)
        else:
            self._storage[key] = {"newest": (item_timestamp, item)}

    def __getitem__(self, key):
        return self._storage[key]["newest"][1]

    def get(self, key):
        item_dict = self._storage.get(key)
        if item_dict is not None:
            return item_dict.get("newest")[1]

        return None

    def get_old(self, key, timestamp):
        storage_item = self._storage.get(key)
        if storage_item is not None:
            return (
                storage_item["newest"][1]
                if storage_item["newest"][0] == timestamp
                else storage_item.get(timestamp)
            )

        return None

    def pop(self, key):
        return self._storage.pop(key)

    def pop_old(self, key, timestamp):
        return self._storage[key].pop(timestamp)

    def __str__(self):
        return self._storage.__str__()
