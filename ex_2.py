class SimpleQueue:
    def __init__(self, queue):
        self.items = list(queue)

    def is_empty(self):
        return True if self.items == [] else False

    def enqueue(self, item):
        return self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def get_first(self):
        return self.items[0]

    def __eq__(self, other):
        if len(self.items) == len(other.items) and self.items[0] == other.items[0]:
            return True
        else:
            return False

    def __gt__(self, other):
        if len(self.items) > len(other.items):
            return True
        else:
            if len(self.items) == len(other.items) and self.items[0] < other.items[0]:
                return True
            else:
                return False

    def __lt__(self, other):
        if len(self.items) < len(other.items):
            return True
        else:
            if len(self.items) == len(other.items) and self.items[0] < other.items[0]:
                return False
            else:
                return True


def parse_ques(q1: SimpleQueue, q2: SimpleQueue):
    while q1.is_empty() is False or q2.is_empty() is False:
        if q1 > q2:
            print(q1.get_first())
            q1.dequeue()
        elif q1 < q2:
            print(q2.get_first())
            q2.dequeue()
        else:
            print(q1.get_first())
            q1.dequeue()


q = SimpleQueue('AB')
q_scnd = SimpleQueue('BB')
parse_ques(q, q_scnd)
