This pipeline loads a CSV file, checks it for any problems, cleans it, and saves the result as a new CSV file. Data is first loaded, then validated, processed, and then saved. The main file pipeline.py runs these steps and reads its settings from config/config.yaml. The src/ folder holds one module for each job. data_loaders.py reads the input files by type, data_validator.py checks for required columns and removes rows with invalid numbers, and data_processor.py removes duplicates, missing values, and outliers. data_output.py saves the cleaned data, and utils.py handles logging and input file checks. The pipeline prints a report showing how many rows were removed.

EXAMPLE: python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

OUTPUT:
01:51:07 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
01:51:07 INFO     src.utils — Input file validated: fixtures/sample_data.csv
01:51:07 INFO     src.utils — Input file validated: config/config.yaml
01:51:07 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
01:51:07 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
01:51:07 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
01:51:07 DEBUG    src.data_validator — Validation: 100 --> 98 rows
01:51:07 INFO     __main__ — Validation complete: 100 --> 98 rows
01:51:07 DEBUG    src.data_processor — remove_duplicates: 98 --> 96 rows
01:51:07 DEBUG    src.data_processor — handle_missing: 96 --> 94 rows
01:51:07 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
01:51:07 INFO     __main__ — Processing complete: 98 --> 92 rows
01:51:07 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
01:51:07 INFO     __main__ — Saved cleaned data to output/clean.csv
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}