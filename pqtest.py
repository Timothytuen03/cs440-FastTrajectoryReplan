import heapq

class PriorityQueue(object):
    def __init__(self) -> None:
        self.heap = []
        # self._index = 0 # For identical priorities

    def __str__(self) -> str:
        # return ' '.join(tuple(self.heap))
        return ' '.join(map(str, self.heap))
    
    def empty(self):
        return len(self.heap) == 0
    
    def add(self, element, g, priority):
        heapq.heappush(self.heap, (priority, g, element))
        # self._index += 1

    def remove(self):
        return heapq.heappop(self.heap)[-1]
    

pq = PriorityQueue()

pq.add('a', 1, 0)
pq.add('b', 0, 0)
pq.add('c', 5, 0)
pq.add('d', -8, 0)
pq.add('e', 100, -1)
print(pq)

while not pq.empty():
    x = pq.remove()
    print(x)