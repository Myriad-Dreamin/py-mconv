#!/usr/bin/env python3

__version__ = '0.0.0'


import argparse
from mconv.conv import PyConv


class CommandLineInterface:
    version = __version__

    def __init__(self):
        self.flags = None
        self.parse_args()
        if self.flags is not None:
            self.encoding = self.flags.encoding
            self.source_encoding = self.flags.source_encoding or self.encoding
            self.target_encoding = self.flags.target_encoding or self.encoding
            self.src = self.flags.src
            self.tar = self.flags.o
        # print(self.source_encoding, self.target_encoding, self.src, self.tar)
        PyConv().from_file(self.src, self.source_encoding).to_file(self.tar, self.target_encoding)

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--encoding', type=str, default='utf-8', help='the source/target file encoding')
        parser.add_argument('--source_encoding', type=str, help='the source file encoding')
        parser.add_argument('--target_encoding', type=str, help='the target file encoding')
        parser.add_argument('--src', type=str, help='source file path')
        parser.add_argument('-o', type=str, default='res.json', help='target file path')
        self.flags = parser.parse_args()

        
def main():
    CommandLineInterface()

if __name__ == '__main__':
    main()