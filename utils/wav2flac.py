import argparse
import glob
import pathlib
import sox
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(
        prog="wav2flac",
        description="Converts WAV files to FLAC files",
    )
    parser.add_argument(
        "path",
        help="Path to the file to convert. If -d or --directory is specified then `path` is glob searched for WAV files.",
        type=pathlib.Path
    )
    parser.add_argument(
        "-o", "--output",
        required=False,
        help="Directory to output to. If omitted, files are output in the directory that corresponds to the original WAV file.",
        type=pathlib.Path
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_path: pathlib.Path = args.path.absolute()

    # set up sox conversion variables (output verbosity and file format)
    converter = sox.Transformer()
    converter.set_globals(verbosity=0)
    converter.set_output_format("flac")

    # create output directory if it does not exist
    if args.output is not None:
        if args.output.suffix == "":
            if not args.output.exists():
                args.output.mkdir()
            else:
                args.output.parent.mkdir()

    if input_path.is_dir():
        # for directories: glob search for wav files
        wav_files = glob.glob(str(input_path.joinpath("**/*.wav")), recursive=True)

        # iterate through wav files and convert to flacs
        for file in tqdm(wav_files, desc="Converting files"):
            file = pathlib.Path(file).absolute()

            if args.output is None:
                output_path = file.with_suffix(".flac")
            else:
                output_path = args.output.joinpath(file.with_suffix(".flac").name)

            # print(f"Input: {str(file)}\nOutput: {str(output_path)}")
            converter.build(str(file), str(output_path))
    else:
        # for files, simply convert the file and save it to either the output directory or alongside the original file
        if args.output is None:
            output_path = input_path.parent
        else:
            output_path = args.output.absolute()

        # print(f"Input:{str(input_path)}\nOutput: {str(output_path)}")
        converter.build(str(input_path), str(output_path))
