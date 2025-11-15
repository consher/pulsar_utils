# Conor Sheridan
# 14/11/2025
#
# Python util to add Gaussian noise to a pulse profile (in .ar format)

import numpy as np
import psrchive
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_help = "This script adds Gaussian noise to a pulse profile (uses .ar file format)"

    parser.add_argument('-file',    type=str,   help="File containing the pulse profile ")
    parser.add_argument('-scale',   type=float, help="The value by which to sacle the noise by before adding, as a fraction maximum value of the pulse profile.")
    parser.add_argument('-out',     type=str,   help="Name of the output")

    return parser.parse_args()

# read the file and outputs the loaded archive file and a pointer to the profile as an f,t & p scrunched profile in a numpy array
def read_profile_from_file(filename):
    ar_file = psrchive.Archive_load(filename) # read ar file
    ar_file.tscrunch()
    ar_file.fscrunch()
    ar_file.pscrunch()
    
    pdata = ar_file.get_Profile(0,0,0).get_amps() # returns the pointer to the array containing the amplitudes of the phase values of the profile
    return ar_file, pdata

# write data to an ar file
def write_profile_to_file(ar_file,filename,output):
    if(filename == output):
        print("warning! Input name and output name are the same, are you sure you want to overwrite? (y/n)")
        
        ans = 0
        # while loop to take input from user on whether to overwrite or not
        while(ans == 0):
            ans = input()
            if(ans == 'y' or ans == 'Y'):
                continue
            elif(ans == 'n' or ans == 'N'):
                print("Cancelling operation...") 
                sys.exit()
            else:
                print("Unkown input, please enter 'y' or 'n':") 
                ans = 0 # loops until program recieves valid input
        
    ar_file.unload(output) # saves the currently loaded archive file

# input a pointer to the profile data and a scale generate gaussian noise, scale it and add it to the pulse profile
def add_gaussian_noise(pdata,scale):
    max_val = np.max(pdata)
    nbins = len(pdata)

    noise = np.random.randn(nbins) # generate noise
    noise = ( noise / np.max(noise) ) * max_val * scale # normalise noise, then scale by fraction of the max value

    pdata += noise

def main():
    args = parse_args()

    ar_file, data_pointer = read_profile_from_file(args.file)

    add_gaussian_noise(data_pointer,args.scale)

    write_profile_to_file(ar_file,args.file,args.out)

if __name__ == '__main__':
    main()
