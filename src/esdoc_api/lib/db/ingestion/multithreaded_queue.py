import subprocess
import os
import threading
from Queue import Queue  #py2

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

def _do_work(item):
    print(str(threading.currentThread()) + item + '\n')

def _send(t):
    t.start()
    for data in ['hello', 'dolly']:
        t.send(data)


if __name__ == "__main__":
    print(str(threading.currentThread()) + ' :: start ' + '\n')
    threads = []
    for i in range(1000):
        threads.append(WorkerThread())
    for t in threads:
        _send(t)
    for t in threads:
        t.close()
    print(str(threading.currentThread()) + ' :: end ' + '\n')
    

