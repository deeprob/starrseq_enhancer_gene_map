import os
import re
import json
from argparse import Namespace
import requests
import subprocess
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
        store_dir, "lib_peaks",lib_short, "peaks.bed"
        )
    return peak_filepath

def get_lib_dapeak_parsed_filepath(store_dir, lib_short, da_type, diff_activity_analysis_type):
    peak_filepath = os.path.join(
        store_dir, diff_activity_analysis_type, lib_short, f"{da_type}.bed"
        )
    return peak_filepath

def get_enhancer_gene_mapped_store_dir(store_dir, peak_desc, lib_short, method, analysis_type):
    return os.path.join(store_dir, peak_desc, lib_short, method, analysis_type)

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

#############
# run GREAT #
#############

# link: https://great-help.atlassian.net/wiki/spaces/GREAT/pages/655447/Programming+Interface

def get_request_url(git_url_prefix, peak_desc, lib_short, da_activity_type):
    """
    Peak file url from github
    """
    return "/".join([git_url_prefix.strip("/"), peak_desc, lib_short, f"{da_activity_type}.bed"])

def submit_batch_job_to_great(url, store_file):
    subprocess.run([
        "wget", "-O", store_file, url
    ])
    return

def store_great_results_enrichment(request_url, genome_version, request_name, request_sender, store_file):
    request_url = request_url.replace(":", "%3A").replace("/", f"%2F")
    great_url = f"http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php?outputType=batch&requestSpecies={genome_version}&requestName={request_name}&requestSender={request_sender}&requestURL={request_url}"
    submit_batch_job_to_great(great_url, store_file)
    return

def get_peak_file(peak_dir, peak_desc, lib_short, da_activity_type):
    """
    Peak file
    """
    return os.path.join(peak_dir, peak_desc, lib_short, f"{da_activity_type}.bed")

def get_session_id(resp):
    id_info = resp.text.split("\n")[0].split(";")[0].strip().replace("'", "")
    id_info = re.sub(r"\s+", "", id_info)
    pattern = re.compile("<script>console.log\(outputDir:/scratch/great/tmp/results/(\d{8}-public-4.0.4-\S{6}).d/\)")
    m = re.match(pattern, id_info)
    return m.group(1)

def store_great_results_associations(peak_file, store_file):
    file = open(peak_file, "r")
    file_data = file.read()
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
        "species": "hg38",
        "includeCuratedRegDoms" : True,
        "rule" : "basalPlusExt",
        "upstream" : 5.0,
        "downstream" : 1.0,
        "span" : 1000.0,
        "twoDistance" : 1000.0,
        "oneDistance" : 1000.0,
        "fgChoice": "data",
        "fgData": file_data,
        "bgChoice": "wholeGenome",
        "adv_upstream": 5.0,
        "adv_downstream": 1.0,
        "adv_span": 1000.0
    }
    great_base_url = "http://great.stanford.edu/public/cgi-bin/greatWeb.php"
    session = requests.Session()
    response = session.post(great_base_url, headers=headers, data=payload)
    session_id = get_session_id(response)
    assoc_url = f"http://great.stanford.edu/public/cgi-bin/downloadAssociations.php?sessionName={session_id}&species=hg38&foreName=user-provided%20data&backName=&table=region"
    associations = session.get(assoc_url)
    with open(store_file, "wb") as f:
        f.write(associations.content)
    session.close()
    file.close()
    return