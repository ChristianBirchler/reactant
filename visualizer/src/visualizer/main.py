from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from plotly_dash import run_plotly_dash_app


class QueueManager(BaseManager):
    pass


class PlotlyProcess(Process):
    def __init__(self, msg_queue_python, msg_queue_java):
        super().__init__()
        self.msg_queue_python = msg_queue_python
        self.msg_queue_java = msg_queue_java

    def run(self):
        print('* plotly process started')
        run_plotly_dash_app(msg_queue_python=self.msg_queue_python, msg_queue_java=self.msg_queue_java, debug=False)


class QueueManagerProcess(Process):
    def __init__(self):
        super().__init__()

    def run(self):
        print('* queue manager process started')

        python_queue = Queue()
        java_queue = Queue()

        plotly_process = PlotlyProcess(python_queue, java_queue)
        plotly_process.start()

        QueueManager.register('get_python_queue', callable=lambda: python_queue)
        QueueManager.register('get_java_queue', callable=lambda: java_queue)

        queue_manager = QueueManager(address=('', 50000), authkey=b'abracadabra')
        server = queue_manager.get_server()

        print('* start queue manager server')
        server.serve_forever()
        print('* queue manager server started')
        while True:
            pass


if __name__ == '__main__':
    print('* start visualizer ...')

    queue_manager_process = QueueManagerProcess()
    queue_manager_process.start()

    print('* end')
