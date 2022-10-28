
import sys
import os
from argparse import ArgumentParser

argv = sys.argv
parser = ArgumentParser()
parser.add_argument('-j', '--job', dest='job', type=str, default='submit', action='store', help="which algorithm of pico.py to run" )
args = parser.parse_args()

tes=0.974
while tes <= 1.030:
    tesString = format(tes,'.3f')
    os.system( "pico.py %s -y UL2018v10 -c mutau_TES%s -s DY -E jec=False"%(args.job, tesString.replace('.','p')) )
    tes += 0.002