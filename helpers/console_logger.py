import datetime

class console_logger:
    prefix: str
    time: datetime
    total_time: datetime

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.total_time = datetime.datetime.now()

    def log(self, message: str):
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {self.prefix} : {message}')

    def run_execution_timer(self):
        self.time = datetime.datetime.now()

    def log_with_execution_time(self, message:str):
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {self.prefix}: {message} ({datetime.datetime.now() - self.time})')

    def log_total_time(self):
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Total execution time of \'{self.prefix}\': {datetime.datetime.now() - self.total_time}')