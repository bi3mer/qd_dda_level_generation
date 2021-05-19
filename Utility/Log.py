from os.path import join

class Log:
    def __init__(self, id, dir):
        self.id = id
        self.f = open(join(dir, f'log_{id}.txt'), 'w')

    def log_info(self, message):
        self.f.write(f'INFO :: {message}\n')

    def log_warning(self, message):
        self.f.write(f'WARN :: {message}\n')

    def log_error(self, message):
        self.f.write(f'ERROR :: {message}\n')

    def close(self):
        self.f.close()
