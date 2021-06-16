# factorio-recipe-clustering

An attempt to cluster Factorio recipes with a heatmap and dendrogram. 

*Motivation*: To design malls/city blocks where the input and output requirements are similar in a systematic way. 

Requirements: 

* Python 3 environment with pandas and networkx
* For the heatmap, R with ComplexHeatmap

Step 1: Use the [Data Exporter to JSON mod](https://mods.factorio.com/mod/recipelister) to create a JSON file of all the recipes of the saved game. 

Step 2: Run recipe_json_to_graph.py to recursively parse the recipe JSON to create a CSV of all the requirements for a particular item. Rows are items, columns are the input requirements for that item. This also creates a GEXF file that can be loaded into Gephi. 

Step 3: Run heatmap.R to generate the heatmap. 

Step 4: Load the GEXF file into Gephi and analyze using Louvain community detection. 
