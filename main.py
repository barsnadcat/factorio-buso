import json
import os


def main():
    with open('recipes.json') as fp:
        recipes = json.load(fp)
        for name, recipe in recipes.items():
        	print(recipe["name"])
        	print(recipe["ingredients"])

        

if __name__ == '__main__':
    main()