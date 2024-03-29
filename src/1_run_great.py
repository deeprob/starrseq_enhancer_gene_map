import argparse
import os
import utils as ut


def main(
    lib_short,
    git_url,
    peak_dir,
    diff_activity_type,
    diff_activity_analysis_type,
    store_dir
    ):

    peak_desc = "lib_peaks"
    da_type = "peaks"
    if diff_activity_type:
        da_type = diff_activity_type
        peak_desc = diff_activity_analysis_type

    analysis_type = "enrichment" if git_url else "association"
    great_store_dir = ut.get_enhancer_gene_mapped_store_dir(store_dir, peak_desc, lib_short, "great", analysis_type)
    os.makedirs(great_store_dir, exist_ok=True)
    store_file = os.path.join(great_store_dir, f"{da_type}.tsv")

    if analysis_type == "enrichment":
        # get peak file url
        peak_url = ut.get_request_url(git_url, peak_desc, lib_short, da_type)
        # store great results
        ut.store_great_results_enrichment(peak_url, "hg38", lib_short, "starrseq", store_file)
    
    else:
        # get peak file
        peak_file = ut.get_peak_file(peak_dir, peak_desc, lib_short, da_type)
        # store great associations
        ut.store_great_results_associations(peak_file, store_file)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq MEA analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib", type=str, help="library name as given in the meta file")
    parser.add_argument("store_dir", type=str, help="Dir to store great results")
    parser.add_argument("--git_url", type=str, default = "", help="Github repo url where the peak file is stored")
    parser.add_argument("--peak_dir", type=str, default = "", help="Dir where the peak file is stored")
    parser.add_argument("--diff_activity_type", type=str, default="", help="type of differential enhancer activity, use this argument to compare induced,repressed and constitutive peaks between lib1 and control")
    parser.add_argument("--diff_activity_analysis_type", type=str, default="diff_peaks", help="type of method used to measure differential enhancer activity, use this argument to compare differential peaks called using deseq2 or normal bedtools intersection")

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib)

    main(
        lib_args.library_short,
        cli_args.git_url,
        cli_args.peak_dir,
        cli_args.diff_activity_type,
        cli_args.diff_activity_analysis_type,
        cli_args.store_dir
    )    
