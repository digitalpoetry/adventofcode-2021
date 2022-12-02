import queue
import time
from dataclasses import dataclass, field
from io import StringIO
from multiprocessing import Queue, Process
from random import random

from aocd.models import Puzzle


@dataclass
class ALU:
    variable: dict[str, int] = field(default_factory=lambda: {'w': 0, 'x': 0, 'y': 0, 'z': 0})

    def _value_of(self, variable: str) -> int:
        try:
            return int(variable)
        except ValueError:
            return self.variable[variable]

    def inp(self, variable, value: str):
        assert variable in self.variable
        self.variable[variable] = self._value_of(value)

    def add(self, a, b: str):
        self.variable[a] += self._value_of(b)

    def mul(self, a, b: str):
        self.variable[a] *= self._value_of(b)

    def div(self, a, b: str):
        self.variable[a] //= self._value_of(b)

    def mod(self, a, b: str):
        self.variable[a] %= self._value_of(b)

    def eql(self, a, b: str):
        self.variable[a] = 1 if self.variable[a] == self._value_of(b) else 0


@dataclass
class Execution:
    instructions: list[str]
    input_tape: str

    def execute(self) -> dict[str, int]:
        tape = StringIO(self.input_tape)
        alu: ALU = ALU()
        commands = {
            'inp': lambda args: alu.inp(*args),
            'add': lambda args: alu.add(*args),
            'mul': lambda args: alu.mul(*args),
            'div': lambda args: alu.div(*args),
            'mod': lambda args: alu.mod(*args),
            'eql': lambda args: alu.eql(*args),
        }
        for line in self.instructions:
            command, *arguments = line.split()
            if command == 'inp':
                arguments.append(tape.read(1))
            commands[command](arguments)
        return dict(alu.variable)


class Worker(Process):
    def __init__(self, instructions: list[str], work_queue, result_queue: Queue):
        super(Worker, self).__init__()
        self.instructions = instructions
        self.work_queue = work_queue
        self.result_queue = result_queue

    def run(self):
        print(f'{self.name} started.')
        for n in iter(self.work_queue.get, None):
            if n is None:
                print(f'{self.name} out of work. Going to sleep for 1s.')
                time.sleep(1000)
                continue
            result = Execution(self.instructions, str(n)).execute()
            self.result_queue.put((n, result))

            if random() < 0.0001:
                print(f'{self.name} processed {n}, result {result}')

        print(f'{self.name} shutting down.')


def part1(input_data: str) -> int:
    monad = input_data.splitlines()
    work_queue = Queue()
    result_queue = Queue()

    n_processes = 16
    for i in range(n_processes):
        Worker(monad, work_queue, result_queue).start()

    next_work = 99_999_999_999_999
    answer: int = 0
    while True:
        try:
            n, result = result_queue.get(block=False)
            if result.get('z') == 0:
                answer = n
                break
        except queue.Empty:
            pass
        try:
            work_queue.put(next_work, block=False)
            next_work -= 1
        except queue.Full:
            pass

    # Signal workers to stop working.
    for i in range(n_processes):
        work_queue.put(None)

    # Drain the result queue
    while not result_queue.empty():
        n, result = result_queue.get()
        if result.get('z') == 0:
            answer = max(answer, n)

    return answer


def part2(input_data: str) -> int:
    return 0


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=24)
    # print(part1(puzzle.input_data))
    # print(part2(puzzle.input_data))
