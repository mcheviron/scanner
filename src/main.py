import argparse
import asyncio
import signal
import sys

from utils import handle_exit, scaffold

if __name__ == "__main__":

    async def main():
        """
        Asynchronous function that serves as the entry point of the program.
        It takes no parameters.

        The function performs the following steps:
            1. Creates an argument parser object.
            2. Adds the "host" argument to the parser, which represents the
            hostname or IP address to scan.
            3. Adds the "--ports" argument to the parser, which represents the
            list of ports to scan.
            4. Adds the "--open" argument to the parser, which indicates
            whether to show only open ports.
            5. Parses the command-line arguments using the argument parser.
            6. Registers a signal handler for SIGINT, which will call the
            "handle_exit" function when the program receives an interrupt
            signal.
            7. Creates a "scanner" object by calling the "scaffold" function
            with the parsed arguments.
            8. Executes the scanner asynchronously using the "await" keyword.

        This function does not return any value.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "host",
            help=(
                "hostname or ip to scan, or a comma/space separated list"
                " thereof"
            ),
        )
        parser.add_argument(
            "-p",
            "--ports",
            help="List of ports to scan eg: 1-443,444,500-600",
        )
        parser.add_argument(
            "--open",
            action="store_true",
            help="Show only open ports",
        )
        args = parser.parse_args()

        signal.signal(signal.SIGINT, handle_exit)
        if sys.version_info < (3, 11):
            print(
                "WARNING: This application requires Python version 3.11 or"
                " higher."
            )
            confirmation = input("Do you still want to continue? (y/n): ")
            if confirmation.lower() != "y":
                return

        scanner = scaffold(args)
        await scanner.exec()


asyncio.run(main())
