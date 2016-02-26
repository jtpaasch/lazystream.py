# -*- coding: utf-8 -*-

"""Reads a stream lazily."""

from Queue import Queue, Empty
from threading import Thread

class LazyStream:
    """                                                                         
    A class that reads a stream (like stdout) in a thread,                      
    so that it does not block main program execution.                           
                                                                                
    """

    def __init__(self, stream):
        """                                                                     
        Given a stream, this starts everything up.                              
                                                                                
        """
        self.stream = stream
        self.queue = Queue()
        self.start_thread()

    def start_thread(self):
        """                                                                     
        This initializes and starts the thread.                                 
                                                                                
        """
        self.thread = Thread(target=self.put_lines_into_queue)
        self.thread.daemon = True
        self.thread.start()

    def put_lines_into_queue(self):
        """                                                                     
        This reads all lines from a stream and puts them in a queue.            
        Note: this is blocking (for the thread it is running in).               
                                                                                
        """
        for line in iter(self.stream.readline, b''):
            self.queue.put(line)
        self.stream.close()

    def readline(self):
        """                                                                     
        Check if there are any new lines in the queue.                          
                                                                                
        """
        try:
            return self.queue.get_nowait()
        except Empty:
            return None


