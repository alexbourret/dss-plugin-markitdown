import dataiku
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config
from temp_utils import CustomTmpFile

input_A_names = get_input_names_for_role('input_A_role')
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]

my_variable = get_recipe_config().get('parameter_name', None)
config = get_recipe_config()
print("ALX:config={}".format(config))

# -*- coding: utf-8 -*-
import dataiku
import pandas
from markitdown import MarkItDown

# Read recipe inputs
documents_to_process = input_A_datasets[0]
documents_to_process_dataframe = None
handle = None
try:
    documents_to_process_dataframe = documents_to_process.get_dataframe()
except Exception as error_message:
    input_folder = get_input_names_for_role("input_A_role")
    input_A_datasets = [dataiku.Folder(name) for name in input_A_names]
    handle = input_A_datasets[0]

markitdown = MarkItDown()

if handle:
    paths = handle.list_paths_in_partition()
    for path in paths:
        with handle.get_download_stream(path) as f:
            temp_cache = CustomTmpFile()
            temp_location = temp_cache.get_temporary_cache_dir()
            data = f.read()
            result = markitdown.convert(data)
else:
    column_name = config.get("url_column")
    if not column_name:
        raise Exception("The column containing the documents URl must be selected")

    results = []
    for index, line in documents_to_process_dataframe.iterrows():
        output_line = line
        url = line[column_name]
        result = markitdown.convert(url)
        if result:
            output_line['markdown_document'] = result.text_content
        else:
            output_line['markdown_document'] = None
        results.append(output_line)

    output_dataframe = pandas.DataFrame(results)
    output_A_datasets[0].write_with_schema(output_dataframe)
