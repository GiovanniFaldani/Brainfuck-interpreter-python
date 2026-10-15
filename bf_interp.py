import numpy as np
import argparse
from colorama import Fore, Style

# Class to represent the tape and head of the Turing Machine
class MyBrainfuckTuringMachine:
    # memory tape and current head position
    tape: np.array
    head: int
    
    def __init__(self):
        self.tape = np.array([0], dtype=np.uint8)
        self.head = 0
    
    def increment(self):
        self.tape[self.head] += np.uint8(1)
    
    def decrement(self):
        self.tape[self.head] -= np.uint8(1)
        
    def right(self):
        self.head += 1
        
        # Add new space to the right
        if self.head >= len(self.tape):
            self.tape = np.append(self.tape, np.uint8(0))
            
    def left(self):
        self.head -= 1
        
        # Add a new space to the left 
        if self.head < 0:
            self.tape = np.insert(self.tape, 0, np.uint8(0))
            self.head = 0 # normalize head
            
    def print(self):
        # print as ASCII character for readability
        print(chr(self.tape[self.head]), end='')
        
    def input(self):
        self.tape[self.head] = np.uint8(input("Input your value: "))
        
    def check_begin_loop(self, bracket_dict: dict, program_counter: int):        
        # if tape[head] != 0, increment program counter by 1, else jump to next matching ]
        if self.tape[self.head] != 0:
            program_counter += 1
            
        else:
            # find matching bracket position
            program_counter = bracket_dict[program_counter] + 1
                       
        return program_counter
        
    def check_end_loop(self, bracket_dict: dict, program_counter: int):           
        # if tape[head] == 0, increment program counter by 1, else jump to previous matching [
        if self.tape[self.head] == 0:
            program_counter += 1
            
        else:
            # find matching bracket position
            program_counter = bracket_dict[program_counter] + 1
                        
        return program_counter
        
    def parse_program(self, program_string: str):
        # execute commands given in the program string
        allowed_symbols = set(['.', ',', '<', '>', '+', '-', '[', ']'])
        
        program_counter = 0
        
        command_list = list(program_string)
        
        # guard clause for unknown commands
        if not any(symbol in allowed_symbols for symbol in command_list):
            print("Invalid program string")
            return
            
        bracket_dict = find_matching_brackets(program_string)
                
        while program_counter < len(command_list):
            
            command = command_list[program_counter]
                        
            match command:
                case '.':
                    self.print()
                    program_counter += 1
                case ',':
                    self.input()
                    program_counter += 1
                case '<':
                    self.left()
                    program_counter += 1
                case '>':
                    self.right()
                    program_counter += 1
                case '+':
                    self.increment()
                    program_counter += 1
                case '-':
                    self.decrement()
                    program_counter += 1
                case '[':
                    program_counter = self.check_begin_loop(bracket_dict, program_counter)
                case ']':
                    program_counter = self.check_end_loop(bracket_dict, program_counter)
                    
    def debug(self):
        print('\n')
        for i in range(len(self.tape)):
            if i == self.head:
                print(Fore.RED + str(self.tape[i]) + " ", end='')
                print(Style.RESET_ALL)
            else:
                print(str(self.tape[i]) + " ", end='')

# Thank stack overflow, with some slight modifications: https://stackoverflow.com/a/63382967
def find_matching_brackets(s):
    openers = {"[": "]"}
    closers = {v: k for k, v in openers.items()}
    stack = []
    result = dict()

    for i, c in enumerate(s):
        if c in openers:
            stack.append([c, i])
        elif c in closers:
            if not stack:
                raise ValueError(f"tried to close brace without an open at position {i}")

            pair, idx = stack.pop()
            
            # save search both ways so to easily lookup matching bracket
            result[idx] = i
            result[i] = idx

            if pair != closers[c]:
                raise ValueError(f"mismatched brace at position {i}")
    
    if stack:
        raise ValueError(f"no closing brace at position {i}")

    return result

def main():
    # ignore overflow warnings for np.uint8 (255 + 1 = 0), it's the behavior we want
    np.seterr(over='ignore')
    
    # TODO argparse
    parser = argparse.ArgumentParser(
                    prog="Brainfuck Interpreter",
                    description="Runs a brainfuck interpreter on the given input string or file",
                    epilog="I hate Python as a language :)")
                    
    parser.add_argument("-i", "--input", help="The input program string")
    parser.add_argument("-f", "--file", help="The file containing the program string")
    parser.add_argument("-d", "--debug", help="Print the tape state after the program run", action='store_true')
    
    args = parser.parse_args()
    if args.file:
        file_path = args.file
        with open(file_path, 'r') as file:
            file_content = file.read()
            
        program_string = file_content
        
    elif args.input:
        program_string = args.input
        
    else:
        parser.print_help()
        return
    
    # try using: "++++++++++[>+++++++>++++++++++>+++++++++++<<<-]>+.>+++++.-------->+.+++++++.--------<.>..-----." and you'll find my name ;)
    
    my_bf_tm = MyBrainfuckTuringMachine()
    
    my_bf_tm.parse_program(program_string)
    
    if(args.debug):
        my_bf_tm.debug()
    
    
if __name__ == "__main__":
    main()