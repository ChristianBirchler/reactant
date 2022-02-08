from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue


class QueueManager(BaseManager):
    pass


class Worker(Process):
    def __init__(self, queue_):
        super().__init__()
        self.queue = queue_

    def run(self):
        while True:
            print('while loop')
            element = self.queue.get()
            print(element)


class QueueManagerProcess(Process):
    def __init__(self):
        super().__init__()

    def run(self):
        queue = Queue()

        worker = Worker(queue)
        worker.start()
        print('* worker started')

        QueueManager.register('get_queue', callable=lambda: queue)
        m = QueueManager(address=('', 50000), authkey=b'abracadabra')
        s = m.get_server()
        s.serve_forever()


if __name__ == '__main__':
    print('* start visualizer ...')

    queue_manager_process = QueueManagerProcess()
    queue_manager_process.start()

    print('* end')
