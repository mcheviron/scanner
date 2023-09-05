# Async Scanner

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This is a simple async scanner that uses Python 3.11 high-level asyncio API. The project has not dependancies and be run on versions 3.10 and 3.11. Earlier versions aren't supported nor tested.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repository.git
```

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

The application will perform the following steps:

1. For each hostname or IP provided the range of ports provided will be scanned 
2. Printing results will be in a simple tabular format
3. Print order isn't guranteed
4. Unresolvable hosts will be silently skipped

If the Python version is less than 3.11, the user will be prompted for confirmation before proceeding.

## Examples
```bash
usage: main.py [-h] [-p PORTS] [--open] host

positional arguments:
  host                  hostname or ip to scan, or a comma/space separated list thereof

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        List of ports to scan eg: 1-443,444,500-600
```

```bash
$ py ./main.py scanme.nmap.org  -p 1-100,443 --open      
     Host          Port      State        Reason      Service 
scanme.nmap.org     22        open        syn/ack       ssh   
scanme.nmap.org     80        open        syn/ack       http  

Total execution time: 0.38 seconds

```


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).