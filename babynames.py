#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import argparse

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""
def get_match(pattern, line):
    match = re.findall(pattern, line)
    return match[0] if len(match) else None

def write_summary(filename, output):
    with open(filename, "w") as f:
        f.write(output)

def read_file(filename):
    """returns text from filename"""
    babies_pattern = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'

    with open(filename, "r") as f:
        return [get_match(babies_pattern, line) for line in f if get_match(babies_pattern, line)]

def build_name_dict(names):
    name_dict = {}
    for count, name1, name2 in names:
        name_dict[name1] = count if name1 not in name_dict else min(name_dict[name1], count)
        name_dict[name2] = count if name2 not in name_dict else min(name_dict[name2], count)

    return name_dict

def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single list starting
    with the year string followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    year_pattern = r'baby(.*).html'
    year = re.match(year_pattern, filename).group(1)
    name_dict = build_name_dict(read_file(filename))
    names = list(map(lambda x: "%s %s" % (x[0], x[1]), zip(name_dict.keys(), name_dict.values())))
    names = sorted(names)
    names.insert(0, year)
    return names


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""
    parser = argparse.ArgumentParser(description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more filenames.
    # It will also expand wildcards just like the shell, e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command-line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command-line arguments into a NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files
    # option flag
    create_summary = ns.summaryfile

    for f in file_list:
        names = extract_names(f)
        if create_summary:
            write_summary("baby%s.html.summary" % names[0], "\n".join(names))
        else:
            print("\n".join(names) + "\n")

if __name__ == '__main__':
    main(sys.argv[1:])
