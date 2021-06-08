seed = 28982  # use 28982 to reproduce the exact same sampling results as mine
charts_folder = "figures"


# vars for sample.py
class SampleVars:
    samplepct = 0.1  # Sample percentage, 0.1 for 10 pc
    input_directory = "data"  # Directory where all dataset files are
    output_directory = "sample_output"
    output_prefix = "sample"  # Prefix for output file names
    output_chunk_size = 100  # Size of output chunks, in MB


# vars for filter.py
class FilterVars:
    input_directory = "sample_output"
    output_directory = "filter_output"
    output_prefix = "filtered"
    output_chunk_size = 150000  # Size of output chunks, in number of rows


# vars for visualization.py
class VizVars:
    input_directory = "filter_output"
    output_directory = "viz_output"
    output_prefix = "viz"
    output_chunk_size = 100  # Size of output chunks, in MB


# vars for exploratory.py
class ExploratoryVars:
    input_directory = "filter_output"
    output_directory = "temp_weekly_data"
    output_prefix = "week"
    output_chunk_size = 100  # Size of output chunks, in MB
