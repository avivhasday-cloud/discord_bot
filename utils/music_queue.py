
class MusicQueue:

    def __init__(self):
        self.queue = list()
        self.current_track_index = 0
        self.loop_queue = False

    def __len__(self):
        return len(self.queue)

    def get(self) -> [any, None]:
        if self.is_empty():
            item = None
        else:
            item = self.queue[self.current_track_index]

        return item if item else None

    def put(self, item, index: int = None) -> None:
        if index is None:
            self.queue.append(item)
        else:
            self.insert(item, index)

    def clear(self):
        self.queue.clear()

    def pop(self, index: int = 0):
        self.queue.pop(index)

    def insert(self, item: any, index: int) -> None:
        self.queue.insert(item, index)

    def is_empty(self) -> bool:
        return len(self) == 0

    def is_item_in_queue(self, item: any) -> bool:
        is_item_in_queue = False
        for _item in self.queue:
            if _item == item:
                is_item_in_queue = True
        return is_item_in_queue

    def get_queue_as_dict(self) -> dict:
        return {idx: item for idx, item in enumerate(self.queue)}

    def set_loop_over_queue(self, status: bool):
        self.loop_queue = status

    def reset(self):
        self.queue.clear()
        self.current_track_index = 0
        self.loop_queue = False
