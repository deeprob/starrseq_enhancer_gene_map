import argparse
import os
import utils as ut


def main(
    lib_short,
    peak_dir,
    store_dir,
    diff_activity_type,
    ):

    # get peak filepath
    peak_file = ut.get_lib_peak_filepath(peak_dir, lib_short) if not diff_activity_type else ut.get_lib_dapeak_filepath(peak_dir, lib_short, diff_activity_type)

    # get peak store filepath
    peak_store_file = ut.get_lib_peak_parsed_filepath(store_dir, lib_short) if not diff_activity_type else ut.get_lib_dapeak_parsed_filepath(store_dir, lib_short, diff_activity_type)

    # copy peak file to store dir
    os.makedirs(os.path.dirname(peak_store_file), exist_ok=True)
    ut.parse_peakfile(peak_file, peak_store_file)

    # push repo to github after storing these files manually
    # it will create shareable links that can be used to run great

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq MEA analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib", type=str, help="library name as given in the meta file")
    parser.add_argument("peak_dir", type=str, help="Dir where peak files are stored")
    parser.add_argument("store_dir", type=str, help="Output dir where results will be stored")
    parser.add_argument("--diff_activity_type", type=str, default="", help="type of differential enhancer activity, use this argument to compare induced,repressed and constitutive peaks between lib1 and control")

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib)

    main(
        lib_args.library_short,
        cli_args.peak_dir,
        cli_args.store_dir,
        cli_args.diff_activity_type,
    )    
