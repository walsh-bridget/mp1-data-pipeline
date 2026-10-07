"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""

   # initializes logging type and format
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )



def parse_arguments():
    """Parse command-line arguments."""

    # initializes argument parser
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True,help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true",
                         help="Enable verbose logging")
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""

    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True
    else:
        logger.error(f"Input file not found: {filepath}")
        return False


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}")

    # validate that both files exist
    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    # try to load data
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # make a copy of original dataframe
    df_original = df.copy()

    # try to clean the dataframe
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)

    # create and print cleaning report, log processing results
    report = create_cleaning_report(df_original, df_clean)
    print(report)
    logger.info(f"Processing complete: {len(df_original)} --> {len(df_clean)} rows")

    # save the cleaned DataFrame as CSV, log saving results
    df_clean.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")

if __name__ == "__main__":
    main()