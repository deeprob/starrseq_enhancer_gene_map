import os
import json
from argparse import Namespace
import pandas as pd


###############################
# read meta file; create args #
###############################

def create_args(meta_file, lib_name):
    with open(meta_file, "r") as f: 
        meta_dict = json.load(f)
        
    args = Namespace(
        # from metadata file
        library_prefix = meta_dict[lib_name]["prefix"],
        library_reps = meta_dict[lib_name]["replicates"],
        library_pair= meta_dict[lib_name]["read_pairs"],
        library_umi = meta_dict[lib_name]["umi"],
        library_suffix = meta_dict[lib_name]["suffix"],
        library_short = meta_dict[lib_name]["shortform"],
        reference_genome = meta_dict["genome"]["ref_fasta"],
        reference_genome_twobit = meta_dict["genome"]["ref_twobit"],
        roi_file = meta_dict["roi"]["filtered"]
    )

    return args


###################
# filepath parser #
###################

def get_lib_peak_filepath(peak_dir, lib_short, peak_caller="starrpeaker"):
    peak_filename_dict = {"starrpeaker": "peaks.peak.final.bed"}
    peak_filepath = os.path.join(
        peak_dir, lib_short, peak_caller, peak_filename_dict[peak_caller]
        )
    return peak_filepath

def get_lib_dapeak_filepath(peak_dir, lib_short, da_type):
    peak_filepath = os.path.join(
        peak_dir, lib_short, f"{da_type}.bed"
        )
    return peak_filepath

def get_lib_peak_parsed_filepath(store_dir, lib_short):
    peak_filepath = os.path.join(
        store_dir, "lib_peak",lib_short, "peaks.bed"
        )
    return peak_filepath

def get_lib_dapeak_parsed_filepath(store_dir, lib_short, da_type):
    peak_filepath = os.path.join(
        store_dir, "diff_peak", lib_short, f"{da_type}.bed"
        )
    return peak_filepath

###################
# peakfile parser #
###################

def parse_peakfile(file_in, file_out):
    df = pd.read_csv(file_in, sep="\t", header=None, usecols=[0,1,2])
    df[3] = df[0] + ":" + df[1].astype(str) + "-" + df[2].astype(str)
    df[4] = 0
    df[5] = "."
    df.to_csv(file_out, sep="\t", header=False, index=False)
    return
