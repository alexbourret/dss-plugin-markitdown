# Code for custom code recipe ingest (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.


# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)
config = get_recipe_config()
print("ALX:config={}".format(config))

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from markitdown import MarkItDown

# Read recipe inputs
documents_to_process = input_A_datasets[0] #dataiku.Dataset("documents_to_process")
documents_to_process_df = None
handle = None
try:
    documents_to_process_df = documents_to_process.get_dataframe()
except Exception as error_message:
    print("ALX:documents_to_process={}".format(dir(documents_to_process)))
    input_folder = get_input_names_for_role("input_A_role")
    print("ALX:2")
    input_A_datasets = [dataiku.Folder(name) for name in input_A_names]
    print("ALX:3")
    handle = input_A_datasets[0]
    print("ALX:4")

md = MarkItDown()

if handle:
    print("ALX:FODLER !")
    paths = handle.list_paths_in_partition()
    print("ALX:paths={}".format(paths))
    for path in paths:
        with handle.get_download_stream(path) as f:
            data = f.read()
            print("ALX:5")
            result = md.convert(data)
            print("ALX:6:{}".format(result.text_content))
column_name = config.get("url_column")
print("ALX:column_name={}".format(column_name))

results = []
for index, line in documents_to_process_df.iterrows():
    output_line = line
    url = line[column_name]
    result = md.convert(url)
    #output_line['url'] = url
    output_line['markdown_document'] = result.text_content
    print("ALX:url={}".format(result.text_content))
    results.append(output_line)

odf = pd.DataFrame(results)
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

#output_df = documents_to_process_df # For this sample code, simply copy input to output
#output_A_datasets[0] = documents_to_process_df
output_A_datasets[0].write_with_schema(odf)
# Write recipe outputs
#output = dataiku.Dataset("output")
#output.write_with_schema(output_df)
