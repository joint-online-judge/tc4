from tc4.util import parse_time_ns, parse_memory_bytes

DEFAULT_TIME_NS = 1000000000
DEFAULT_MEMORY_BYTES = 268435456
DEFAULT_PROCESS_LIMIT = 64
DEFAULT_SCORE = 10

class Case:
    def __init__(self, data):
        self.time_limit_ns = 'time' in data and parse_time_ns(data['time']) or DEFAULT_TIME_NS
        self.memory_limit_bytes = 'memory' in data and parse_memory_bytes(data['memory']) or DEFAULT_MEMORY_BYTES
        self.process_limit = 'process' in data and int(data['process']) or DEFAULT_PROCESS_LIMIT
        self.score = 'score' in data and int(data['score']) or DEFAULT_SCORE
        self.execute_file = 'execute_file' in data
        self.execute_args = execute_args
        pass
