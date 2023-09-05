import asyncio
import time
from functools import wraps
from socket import getservbyport
from typing import Any, Coroutine, Tuple


def timer(func):
    """
    Decorator function that measures the execution time of a given async
    function.

    Parameters:
        func (coroutine function): The async function to be measured.

    Returns:
        The result of the decorated function.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        exec_time = end - start
        print(f"\nTotal execution time: {exec_time:.2f} seconds")
        return result

    return wrapper


class Scanner:
    """
    Represents a scanner object that scans hosts and ports for open
    connections.

    Attributes:
        hosts (Tuple[str, ...]): A tuple of strings representing the hosts.
        ports (Tuple[int, ...]): A tuple of integers representing the ports.
        open (bool): Indicates whether to show open ports in the results.
        results (DefaultDict[str, List[Dict[str, Tuple[str, str, str]]]]):
          A dictionary that stores the scan results for each host and port
          combination.
        exec_time (float): The execution time of the scan.

    Methods:
        __init__(hosts, ports, show_open):
            Initializes the Scanner object.
        tasks(hosts):
            Returns a tuple of coroutines representing the scan tasks.
        scan(host, port):
            Asynchronously scans a host and port for an open connection.
        timer():
            Context manager for measuring the total execution time.
        exec():
            The main method that executes the tasks.
    """

    def __init__(
        self, hosts: Tuple[str, ...], ports: Tuple[int, ...], show_open: bool
    ):
        self.hosts = hosts
        self.ports = ports
        self.open = show_open
        self.results: asyncio.Queue[
            Tuple[str, Tuple[str, str, str, str]]
        ] = asyncio.Queue()

    @property
    def tasks(self) -> tuple[Coroutine[Any, Any, None], ...]:
        """
        A property that returns a tuple of coroutines representing tasks.

        Parameters:
            - hosts (Tuple[str, ...]): A tuple of strings representing the
              hosts.
            - ports (Tuple[int, ...]): A tuple of integers representing the
              ports.

        Returns:
            - tuple[Coroutine[Any, Any, None], ...]: A tuple of coroutines
              representing tasks.
        """
        return tuple(
            self.scan(host, port) for port in self.ports for host in self.hosts
        )

    async def scan(self, host, port):
        """
        Asynchronously scans a host and port for an open connection.

        Args:
            host (str): The host to scan.
            port (int): The port to scan.

        Returns:
            None
        """
        try:
            await asyncio.wait_for(asyncio.open_connection(host, port), 0.3)
            state, reason = "open", "syn/ack"
            try:
                service = getservbyport(port)
            except Exception:
                service = "unkown service"
            await self.results.put((host, (port, state, reason, service)))
        except (asyncio.TimeoutError, OSError, ValueError) as error:
            state = "closed"
            try:
                service = getservbyport(port)
            except Exception:
                service = "unkown service"
            errors = {
                "TimeoutError": "connection timeout",
                "OSError": "connection refused",
                "ValueError": "invalid port",
            }
            reason = (
                errors[error.__class__.__name__]
                if error.__class__.__name__ in errors
                else "unexpected error"
            )

            await self.results.put((host, (port, state, reason, service)))

    async def printer(self):
        """
        A coroutine that prints the results of the scan.
        """
        output = "{:^15} {:^15} {:^15} {:^20} {:^15}"
        print(output.format("Host", "Port", "State", "Reason", "Service"))
        while True:
            host, (port, state, reason, service) = await self.results.get()
            if self.open and state == "closed":
                self.results.task_done()
                continue
            host = (host[:13] + "..") if len(host) > 15 else host
            state = (state[:13] + "..") if len(state) > 15 else state
            reason = (reason[:18] + "..") if len(reason) > 20 else reason
            service = (service[:13] + "..") if len(service) > 15 else service
            print(output.format(host, port, state, reason, service))
            self.results.task_done()

    @timer
    async def exec(self):
        """
        The kickstart method for the whole program. Start here if you're
        reading the code.

        This function creates a task to run the `printer` method
        asynchronously using the `asyncio.create_task` function.
        It then waits for all the tasks in the `self.tasks` list to complete
        using the `asyncio.gather` function.
        After that, it waits for the `self.results` to join using the `await`
        keyword. Finally, it cancels the `print_task` using the `cancel`
        method.
        """
        print_task = asyncio.create_task(self.printer())
        await asyncio.gather(*self.tasks)
        await self.results.join()
        print_task.cancel()
