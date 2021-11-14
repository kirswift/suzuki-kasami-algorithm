PROCESS_LIST = []


class Process:
    def __init__(self, count, index):
        self._index = index
        self._rn = []
        self._token = None
        self._in_cs = False

        for i in range(count):
            self._rn.append(0)
        print(self._rn)

    def access(self):
        if self._token is None:
            self.send_request()
            self._in_cs = True
            # enter the critical section
            self._in_cs = False
            self.release()

    def send_request(self):
        rn = self._rn
        for i in range(len(rn)):
            rn[i] += 1
            PROCESS_LIST[i].receive_request(self._index, rn[i])

        print(self._rn)

    def receive_request(self, i, n):
        rn = self._rn
        in_cs = self._in_cs
        token = self._token
        rn[i] = max(rn[i], n)
        if not in_cs and token is not None and rn[i] == token.get_ln()[i]:
            PROCESS_LIST[i].set_token(token)
            self._token = None

    def release(self):
        index = self._index
        queue = self._token.get_queue()
        ln = self._token.get_ln()
        self._token.get_ln()[index] = self._rn[index]
        for j in range(len(PROCESS_LIST)):
            if j == index:
                continue
            if j not in queue and self._rn[j] == ln[j] + 1:
                queue.append(j)
        if len(queue) > 0:
            queue.pop().set_token(self._token)
            self._token = None

    def set_token(self, token):
        self._token = token


class Token:
    def __init__(self, count):
        self._ln = []
        self._queue = []
        for i in range(count):
            self._ln.append(0)

    def get_ln(self):
        return self._ln

    def get_queue(self):
        return self._queue


p_count = 3

p1 = Process(p_count, 0)
p2 = Process(p_count, 1)
p3 = Process(p_count, 2)
PROCESS_LIST = [p1, p2, p3]
p1.set_token(Token(p_count))

p2.access()
p1.access()
p3.access()
