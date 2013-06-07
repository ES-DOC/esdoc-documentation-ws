import subprocess
import os
import threading
from Queue import Queue  #py2


class SharedState(object):
    def __init__(self):
        self.index = 0

shared_state = SharedState()


class WorkerThreadState(object):
    def __init__(self, shared, specific):
        self.shared = shared
        self.specific = specific

    

class WorkerThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        self.input_queue.put(item)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                break

            # Do work.
            _do_work(item)
            
            self.input_queue.task_done()

        # Indicate that sentinel was received and acted upon.
        self.input_queue.task_done()
        return

def _do_work(ctx):
    print(str(threading.currentThread()) + str(ctx.shared.index) + '::' + ctx.specific + '\n')

def _send(t):
    global shared_state
    t.start()
    for data in ['hello', 'dolly']:
        shared_state.index += 1
        t.send(WorkerThreadState(shared_state, data))


if __name__ == "__main__":
    print(str(threading.currentThread()) + ' :: start ' + '\n')
    threads = []
    for i in range(10):
        threads.append(WorkerThread())
    for t in threads:
        _send(t)
    for t in threads:
        t.close()
    print(str(threading.currentThread()) + ' :: end ' + '\n')
    

