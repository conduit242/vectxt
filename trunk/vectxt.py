#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#
# Copyright 2014 Robert Bird
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# vectxt.py
# Version 0.1
# A simple program for converting text to numeric vectors in csv.
# Accepts input from STDIN and outputs to STDOUT; Whitespace is scrubbed


from pyhashxx import hashxx
from sys import stdin, argv
import argparse


def feature_hash_character_ngrams(s, window, dim, hashit, slide):

    v = [0] * dim

    # Generate window-char Markov chains & create feature hash vector

    for x in xrange(0, len(s) - window, slide):
        v[hashit(s[x:x + window]) % dim] += 0x1
    return ",".join(map(str, v))

def feature_hash_word_ngrams(s, window, dim, hashit, slide):

    v = [0] * dim
    s = s.split()

    # Generate word n-grams & create feature hash vector

    for x in xrange(0, len(s) - window, slide):
        v[hashit(" ".join(s[x:x + window])) % dim] += 0x1
    return ",".join(map(str, v))


parser = argparse.ArgumentParser()

parser.add_argument(
    '-d',
    action='store',
    dest='dim',
    default=64,
    type=int,
    help='Set the feature vector width; default=64',
    )

parser.add_argument(
    '-w',
    action='store',
    dest='window',
    default=4,
    type=int,
    help='Set the n-gram window; default=4',
    )

parser.add_argument(
    '-s',
    action='store',
    dest='slide',
    default=1,
    type=int,
    help='Set the slide of the n-gram window; default=1',
    )

parser.add_argument(
    '-o',
    action='store_true',
    dest='use_words',
    default=False,
    help='Use word n-grams; default off',
    )

parser.add_argument(
    '-e',
    action='store_true',
    dest='use_whitespace',
    default=False,
    help='Include whitespace in character n-grams; default off',
    )

args = vars(parser.parse_args())

hashref = hashxx
dim = args['dim']
window = args['window']
slide = args['slide']

if args['use_words']:
    for line in stdin:
        print feature_hash_word_ngrams(line, window, dim, hashref, slide)
elif args['use_whitespace']:
    for line in stdin:
        print feature_hash_character_ngrams(line, window, dim, hashref, slide)
else:    
    for line in stdin:
        line = ''.join(line.split())
        print feature_hash_character_ngrams(line, window, dim, hashref, slide)



