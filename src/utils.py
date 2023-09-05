import argparse
import sys
from typing import Any, Generator

from scanner import Scanner


def scaffold(cli_args: argparse.Namespace):
    """
    Process the ports and hosts and make sure they're in the proper format
    expected by the Scanner

    Args:
        cli_args (argparse.Namespace): The command line arguments passed to
        the function.

    Returns:
        Scanner: An instance of the Scanner class with the specified hosts,
        ports, and open flag.
    """
    hosts = tuple(
        cli_args.host.split(",")
        if "," in cli_args.host
        else cli_args.host.split()
    )
    ports = tuple(
        cli_args.ports.split(",")
        if "," in cli_args.ports
        else cli_args.ports.split()
    )

    full_ports = tuple(_get_ports(ports))
    return Scanner(hosts, full_ports, cli_args.open)


def _get_ports(ports) -> Generator[int, Any, None]:
    """
    Generate a sequence of integers based on the given ports.

    Args:
        ports (List[str]): A list of strings representing ports.

    Yields:
        int: An integer from the range of ports.

    Returns:
        None

    """
    for port in ports:
        if "-" in port:
            start, end = port.split("-")
            yield from range(int(start), int(end) + 1)
        else:
            yield int(port)


def handle_exit(sig, frame):
    """
    Handle the exit signal (ctrl+c) by printing a message and exiting the
    program.

    Parameters:
        sig (int): The signal number.
        frame (frame): The current stack frame.
    """
    print("\nExiting...")
    sys.exit(0)
