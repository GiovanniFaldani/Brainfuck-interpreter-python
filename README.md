# Description 
Simple script that runs a Brainfuck interpreter on the given input string or file

## Setup
Install python on your computer if you don't have it, then run:
```pip install -r requirements.txt```

## Usage
Giving the input string directly:
```python ./bf_interp -i ++++++++++[>+++++++>++++++++++>+++++++++++<<<-]>+.>+++++.-------->+.+++++++.--------<.>..-----.```

Parsing an input file:
```python ./bf_interp.py -f ./program.txt```

Remember to flip the `/` to `\` if on Windows.

options:
  -h, --help         show this help message and exit
  -i, --input INPUT  The input program string
  -f, --file FILE    The file containing the program string
  -d, --debug        Print the tape state after the program run