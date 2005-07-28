#!/usr/bin/env python

"""
Merge any overlapping regions of bed files.

usage: %prog bed files ...
"""

import psyco_full
import sys
from bx.bitset import BinnedBitSet

bed_filenames = sys.argv[1:]

last_chrom = None
last_bitset = None
bitsets = dict() 

for fname in bed_filenames:
    for line in open( fname ):
        if line.startswith("#") or line.startswith("track"): continue
        fields = line.split()
        if fields[0] != last_chrom:
            if fields[0] not in bitsets:
                bitsets[fields[0]] = BinnedBitSet()
            last_chrom = fields[0]
            last_bitset = bitsets[fields[0]]
        start, end = int( fields[1] ), int( fields[2] )
        if start > end: print >>sys.stderr, "Bed interval start after end: " + line.strip()
        last_bitset.set_range( start, end-start )

for chrom in bitsets:
    bits = bitsets[chrom]
    end = 0
    while 1:
        start = bits.next_set( end )
        if start == bits.size: break
        end = bits.next_clear( start )
        print "%s\t%d\t%d" % ( chrom, start, end )
