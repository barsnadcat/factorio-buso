import json
import os
import random

#This recipes create loops in production tree - script is not ready for them
blockedRecipes = set(["advanced-oil-processing", "heavy-oil-cracking", "light-oil-cracking", "coal-liquefaction",
"empty-crude-oil-barrel", "empty-heavy-oil-barrel", "empty-light-oil-barrel", "empty-lubricant-barrel", "empty-petroleum-gas-barrel", "empty-sulfuric-acid-barrel", "empty-water-barrel", 
"solid-fuel-from-light-oil", "solid-fuel-from-petroleum-gas" ])

resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone"])

targetProductList = [
"rocket-control-unit", "rocket-fuel", "low-density-structure", "rocket-silo", "satellite",
"science-pack-1", "science-pack-2", "science-pack-3", "military-science-pack", "high-tech-science-pack", "production-science-pack", 
"splitter", "fast-splitter",
"transport-belt", "fast-transport-belt",
"underground-belt", "fast-underground-belt",
"fast-inserter", "long-handed-inserter",
"roboport", "logistic-chest-passive-provider", "logistic-chest-storage", "logistic-robot", "construction-robot",
"pipe", "pipe-to-ground", "offshore-pump", "storage-tank",
"piercing-rounds-magazine", "flamethrower-ammo", "repair-pack",
"steel-furnace", "pumpjack", "assembling-machine-2", "lab", "chemical-plant", "electric-mining-drill",
"steam-engine",  "big-electric-pole", "medium-electric-pole", "boiler", "accumulator",
"landfill", "gate", "stone-wall", "radar", "laser-turret", "concrete", "gun-turret",
"fluid-wagon", "cargo-wagon", "train-stop", "pump", "locomotive", "rail", "rail-signal", "rail-chain-signal"
]

recipesJson = None


def main():
    with open('recipes.json') as recipefp:
        global recipesJson
        recipesJson = json.load(recipefp)
                
        bus = set()
        bus.update(targetProductList)
        bus.update(resourceList)
        
        complexProduct = GetMostComplexProduct(bus)
        while complexProduct:
            RemoveFromBus(complexProduct, bus)
            complexProduct = GetMostComplexProduct(bus)

        print(bus)

def GetMostComplexProduct(bus):
        complexProduct = None
        complexity = 2;
        
        for product in bus:
            newComplexity = GetProuductComplexity(product, bus)
            if newComplexity > complexity:
                complexProduct = product
                complexity = newComplexity
        
        print("Most complex", complexProduct, complexity)
        return complexProduct

def AddIngredientsToBus(product, bus):
    recipeJson = FindRecipeByProduct(product)
    print("Proudct", product, "recipe", recipeJson["name"])
    if  recipeJson["category"] == "smelting":
        fuel = "coal"
        bus.add(fuel)
        print("Add coal", recipeJson["name"])
        
    for ingredientJson in recipeJson["ingredients"]:
        ingreidentName = ingredientJson["name"]
        bus.add(ingreidentName)
        print("Add", ingreidentName)
    
def RemoveFromBus(product, bus):
    print("Remove", product)
    
    if product not in resourceList:        
        AddIngredientsToBus(product, bus)
        
    bus.remove(product)


def FindRecipeByProduct(product):    
    for recipeName, recipeJson in recipesJson.items():
        if recipeName not in blockedRecipes:
            for productJson in recipeJson["products"]:
                if product == productJson["name"]:
                    return recipeJson
        
def GetProuductComplexity(product, bus):
    complexity = 1
    if product not in resourceList:
        recipeJson = FindRecipeByProduct(product)
        for ingredientJson in recipeJson["ingredients"]:
            ingreidentName = ingredientJson["name"]
            if ingreidentName not in bus:
                complexity += GetProuductComplexity(ingreidentName, bus)
    
    #print("Complexity", product, complexity)
    return complexity




if __name__ == '__main__':
    main()
