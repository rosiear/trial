__author__ = 'Kevin Ma'
__version__ = '1.0'

#Import libraries
import csv
import numpy as np
import pandas as pd
import os
import sys
from datetime import datetime

def main(args):
    #Load data
    food_brands = pd.read_csv(args[0])
    target_ingredients = pd.read_csv(args[1])
    excluded_ingredients = pd.read_csv(args[2])

    target_ingredients['products'] = target_ingredients.iloc[0].str.lower()
    excluded_ingredients['products'] = excluded_ingredients.iloc[0].str.lower()
    food_brands['ingredients'] = food_brands['ingredients'].str.lower()
    
    food_brands['ingredients'] = food_brands['ingredients'].replace("(",",")
    food_brands['ingredients'] = food_brands['ingredients'].replace(")",",")
    
    row_count = 0
    ingredient_count_array = []
    ultimate_ingredients_array = []
    for brand_ingredients in food_brands['ingredients']:
        ingredient_count = 0
        ingredients_array = []
        try:
            ingredients_list = brand_ingredients.split(",")
            for ingredient in ingredients_list:
                for target_ingredient in target_ingredients['products']:
                    if (ingredient.find(target_ingredient) != -1):
                        excluded_ingredient_matches = 0
                        for excluded_ingredient in excluded_ingredients['products']:
                            if (ingredient.find(excluded_ingredient) != -1):
                                print('excluded ingredient found! %s' % excluded_ingredient)
                                excluded_ingredient_matches += 1
                        if (excluded_ingredient_matches == 0):
                            print('target ingredient found! %s' % target_ingredient)
                            ingredient_count += 1
                            ingredients_array.append(target_ingredient)
        except:
            pass
        
        ultimate_ingredients_array.append(ingredients_array)
        print('# identified ingredients for row %s: %s' % (row_count,ingredient_count))
        ingredient_count_array.append(ingredient_count)
        
        row_count += 1

    food_brands['identified_ingredient_count'] = ingredient_count_array
    food_brands['identified_ingredients'] = ultimate_ingredients_array

    #create dataframe with all products that have at least one identified target ingredient
    product_ingredient_matches = food_brands.loc[(food_brands['identified_ingredient_count'] > 0), ['fdc_id','brand_owner','gtin_upc','branded_food_category','ingredients','identified_ingredient_count','identified_ingredients']] 

    identified_brands = product_ingredient_matches['brand_owner'].unique()
    identified_products_count_array = []
    identified_ingredients_count_array = []
    ultimate_ingredients_array = []

    for brand in identified_brands:
        df = product_ingredient_matches.loc[(product_ingredient_matches['brand_owner'] == brand), :]
        identified_products = 0
        ingredients_array = []
        for product_ingredients in df['identified_ingredients']:
            identified_products += 1
            for target_ingredient in target_ingredients['products']:
                for product_ingredient in product_ingredients:
                    if (target_ingredient == product_ingredient):
                        ingredients_array.append(target_ingredient)
        unique_ingredients_array = list(set(ingredients_array))
        identified_ingredients = len(unique_ingredients_array)
        
        ultimate_ingredients_array.append(unique_ingredients_array)
        identified_products_count_array.append(identified_products)
        identified_ingredients_count_array.append(identified_ingredients)

    #create dataframe with brands that have identified ingrdients
    identified_brands_df = pd.DataFrame()
    identified_brands_df['brand_owner'] = identified_brands
    identified_brands_df['identified_products_count'] = identified_products_count_array
    identified_brands_df['identified_ingredients_count'] = identified_ingredients_count_array
    identified_brands_df['ultimate_ingredients'] = ultimate_ingredients_array
        
    #export to excel
    writer = pd.ExcelWriter('output/identified_ingredient_brands_{}.xlsx'.format(datetime.today().strftime('%Y%m%d')), engine='xlsxwriter')
    identified_brands_df.to_excel(writer, sheet_name='identified_brands')
    product_ingredient_matches.to_excel(writer, sheet_name='product_ingredient_matches')
    writer.save()
        
if __name__ == "__main__":
    main(sys.argv[1:])