# !/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
import threading
import time

class WorkManager(object):
    def __init__(self, jobs,thread_num=6):
        self.work_queue = jobs
        self.threads = []
        self.__init_thread_pool(thread_num)

    """
        Init mutiple threads
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        Waiting for all threads finish
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # Infinity loop until meet 
        while True:
            try:
                # Asynchronously get taks and Quese is thread safe
                do, args = self.work_queue.get(block=False)
                # Execute task
                do(args)
                # Notify task done.
                self.work_queue.task_done()
            except:
                break

