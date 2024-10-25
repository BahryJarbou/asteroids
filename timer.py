import time
class Timer():
    def __init__(self):
        self.start_time = time.time()
        self.time = 0
    
    def get_time(self):
            self.time = int((time.time() - self.start_time))
            return self.time
            
timer = Timer()