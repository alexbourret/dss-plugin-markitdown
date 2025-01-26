# Dataiku MarkItDown plugin

Based on Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library, converts various documents types to [MarkDown format](https://en.wikipedia.org/wiki/Markdown). 

The plugin consists in a custom recipe that takes a list of document to process as input. This dataset is duplicated at the output of the recipe, with an extra column containing the document in markdown format.

The library currently process HTML, PDF, CSV, JSON, XML, various MS formats.

## How to use

- Have a dataset containig the list of document to process in a column, here "`url`"
![](images/documents_to_process.jpg)
- In the flow, add the MarkItDown recipe by clicking on `+Recipe > Plugin > MarkItDown > Ingest`
- Use the documents list's dataset as an input, and create an output dataset.
![](images/markitdown_process_dataset.jpg)
- In the recipe, select the column containing the documents URL
- Run the recipe

The output dataset should contain the input dataset, as well as an extra `markdown_document` column.
