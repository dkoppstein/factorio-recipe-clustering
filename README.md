# factorio-recipe-clustering

An attempt to cluster Factorio recipes with a heatmap and dendrogram. 

*Motivation*: To design malls/city blocks where the input and output requirements are similar in a systematic way. 

Step 1: Use the [Data Exporter to JSON mod](https://mods.factorio.com/mod/recipelister) to create a JSON file of all the recipes of the saved game. 

Step 2: Run recipe_requirements.py to recursively parse the recipe JSON to create a CSV of all the requirements for a particular item. Rows are items, columns are the input requirements for that item. 

Step 3: Run heatmap.R to generate the heatmap. 

