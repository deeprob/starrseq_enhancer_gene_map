import argparse
import os
import utils as ut


def main(
    lib_short,
    git_url,
    diff_activity_type,
    store_dir
    ):

    peak_desc = "lib_peak"
    da_type = "peaks"
    if diff_activity_type:
        da_type = diff_activity_type
        peak_desc = "diff_peak"

    # get peak file url
    peak_url = ut.get_request_url(git_url, peak_desc, lib_short, da_type)

    # store great results
    great_store_dir = ut.get_enhancer_gene_mapped_store_dir(store_dir, peak_desc, lib_short, "great")
    os.makedirs(great_store_dir, exist_ok=True)
    store_file = os.path.join(great_store_dir, f"{da_type}.tsv")
    ut.store_great_results(peak_url, "hg38", lib_short, "starrseq", store_file)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq MEA analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib", type=str, help="library name as given in the meta file")
    parser.add_argument("git_url", type=str, help="Github repo url where the peak file is stored")
    parser.add_argument("store_dir", type=str, help="Dir to store great results")
    parser.add_argument("--diff_activity_type", type=str, default="", help="type of differential enhancer activity, use this argument to compare induced,repressed and constitutive peaks between lib1 and control")

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib)

    main(
        lib_args.library_short,
        cli_args.git_url,
        cli_args.diff_activity_type,
        cli_args.store_dir
    )    
