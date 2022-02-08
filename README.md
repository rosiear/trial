# Target ingredients identifier
## Author: Kevin Ma
 This repository has the following folders:
 - data: this folder should contain the csv's that you'll need as input for the python script. These files include: 1) a list of all products in the US and their associated ingredients, 2) a list of target ingredients, and 3) a list of excluded ingredients
 - output: this folder contains the output csv from the python script

### To run the script, all you need to do is the following:
- Set your directory in Terminal to wherever this repository sits
- Run the following command in Terminal: python target_brands_identifier.py data/[AllProductsFileName] data/[TargetIngredientsFileName] data/[ExcludedIngredientsFileName]
    - Where AllProductsFileName is the list of all products in the US, TargetIngredientsFileName is the list of target ingredients, and ExcludedIngredientsFileName is the list of excluded ingredients
