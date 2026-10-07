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

from src import (
create_cleaning_report,
load_data,
process_data,
save_data,
setup_logging,
validate_dataframe,
validate_input,
)

logger = logging.getLogger(__name__)



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

    # read validation settings from config
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # validate the dataframe
    rows_before = len(df)
    try:
        df = validate_dataframe(df, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {rows_before} --> {len(df)} rows")

    # make a copy of original dataframe
    df_original = df.copy()

    # try to clean the dataframe
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)

    # create and print cleaning report, log processing results
    report = create_cleaning_report(df_original, df_clean)
   
    logger.info(f"Processing complete: {len(df_original)} --> {len(df_clean)} rows")

    # save the cleaned DataFrame as CSV, log saving results - *changed to output path
    output_path = save_data(df_clean, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    print(report)

if __name__ == "__main__":
    main()