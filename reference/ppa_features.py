#!/usr/bin/python

#############################################################################
# Copyright 2011 Jason Baldridge
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#############################################################################

import sys
from porter_stemmer import PorterStemmer
from BitVector import BitVector
from classify_util import *

#############################################################################
# Set up the options
parser = get_feature_extractor_option_parser()
parser.add_option("-b", "--bitstrings", dest="bitstrings",
                  help="read bit vectors from FILE", metavar="FILE")

(options, args) = parser.parse_args()
check_mandatory_options(parser, options, ['input'])

#############################################################################
# Use the options to set the input and output files appropriately
input_file = file(options.input)
output_file = sys.stdout
if options.out != None:
    output_file = file(options.out, "w")

verbose = options.verbose
errmsg("Showing verbose output.", verbose)

# Load the bitstrings if the option has been given
bitstrings = {}
use_bitstrings = False
if options.bitstrings != None:
    use_bitstrings = True
    for line in file(options.bitstrings).readlines():
        (word,bits_for_word) = line.strip().split('\t')
        bitstrings[word] = BitVector( bitstring = bits_for_word)

# Create the stemmer for later use.
stemmer = PorterStemmer()

#############################################################################
# Extract features
for line in input_file.readlines():
    (id, verb, noun, prep, prep_obj, label) = \
         [protect_meta_characters(x) for x in line.strip().split()]

    features = []

    # Add the four basic features
    features.append("verb="+verb)
    features.append("noun="+noun)
    features.append("prep="+prep)
    features.append("prep_obj="+prep_obj)

    # Add additional features. An example has been given for stem
    # features, n-gram features, and bitstring features. It's up to
    # you to come up with other features like those, plus any new
    # features you might think of!
    if options.extended_features:

        # ADD CODE: Stem features
        features.append("verb_stem="+stemmer.stem_token(verb))
        features.append("noun_stem="+stemmer.stem_token(noun))

        # ADD CODE: N-gram features
        features.append("verb+noun="+verb+"+"+noun)
        features.append("prep+prep_obj="+prep+"+"+prep_obj)
        features.append("noun+prep+prep_obj="+noun+"+"+prep+"+"+prep_obj)

        # ADD CODE: bitstring features
        # Use the bitstrings to create features. See the paper for a
        # description:
        #
        #     http://aclweb.org/anthology-new/H/H94/H94-1048.pdf
        #
        # These are more advanced than the others, but are very
        # informative.
        if use_bitstrings:

            if bitstrings.has_key(noun):
                noun_bv = bitstrings.get(noun)
                features.append("noun_bit1="+str(noun_bv[1]))

        # ADD CODE: Other features.

        # Normalize the noun
        normalized_noun = noun.replace(",", "")
        features.append("noun_normalized="+normalized_noun)

        # Collapse numbers using ValueError checks
        is_number = False # number status
        try:
            int(normalized_noun) # check int
            is_number = True
            features.append("noun_form=number")
        except ValueError:
            try:
                float(normalized_noun) # check float
                is_number = True
                features.append("noun_form=number")
            except ValueError:
                pass # continue to capital check

        # Collapse abnormally long nouns
        is_long_noun = False # long status
        if len(noun) > 10:
            features.append("nount_form=long_noun")

        # Collapse capitalized words (assuming not a number or long word)
        if not is_long_noun and not is_number and noun[0].isupper():
            if len(noun) > 1 and noun[1].isupper(): # double capital
                features.append("noun_form=XX")
            else: # single capital
                features.append("noun_form=Xx")
        else: # non-number, non-uppercase word
            features.append("noun_form=normal")

        #


    # Add the label
    features.append(label)

    # Join and print the features
    output_file.write(','.join(features) + "\n")
