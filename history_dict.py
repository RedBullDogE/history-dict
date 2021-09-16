from datetime import datetime

test_data = {
    "key": {
        "newest": (datetime(2021, 9, 13, 10), "value-1"),
        datetime(2021, 9, 13, 12): "value-2",
    },
    "another_key": {"newest": (datetime(2021, 9, 13, 10), "value-xxx")},
}


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
        self.storage = dict()

        # -------- ONLY FOR TESTING ----------
        self.storage.update(test_data)

    def __setitem__(self, key, item):
        now = datetime.now()
        item_timestamp = datetime(now.year, now.month, now.day, now.hour)

        if key in self.storage:
            if item_timestamp == self.storage[key]["newest"][0]:
                self.storage[key]["newest"] = (item_timestamp, item)
            else:
                old_timestamp, old_item = self.storage[key]["newest"]
                self.storage[key][old_timestamp] = old_item
                self.storage[key]["newest"] = (item_timestamp, item)
        else:
            self.storage[key] = {"newest": (item_timestamp, item)}

    def __getitem__(self, key):
        return self.storage[key]["newest"][1]

    def get(self, key):
        item_dict = self.storage.get(key)
        if item_dict is not None:
            return item_dict.get("newest")[1]

        return None

    def get_old(self, key, timestamp):
        storage_item = self.storage.get(key)
        if storage_item is not None:
            return (
                storage_item["newest"][1]
                if storage_item["newest"][0] == timestamp
                else storage_item.get(timestamp)
            )

        return None

    def pop(self, key):
        return self.storage.pop(key)

    def pop_old(self, key, timestamp):
        return self.storage[key].pop(timestamp)

    def __str__(self):
        return self.storage.__str__()


if __name__ == "__main__":
    test = HistoryDict()
    print(test.get("key"))  # returns value-1

    print(test.get_old("key", datetime(2021, 9, 13, 12)))  # returns value-2
    print(test.get_old("key", datetime(2021, 9, 13, 9)))  # returns None

    print(test["another_key"])  # returns value-xxx
    test['another_key'] = "value-xxx-2"
    print(test.get("another_key"))  # returns value-xxx-2

    print(test["fake"])  # raises KeyError
    print(test.get("fake"))  # return None
