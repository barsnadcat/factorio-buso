import json
import os

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
                
        bus = {}

        for product in targetProductList:
            AddIngredientsToBus(product, bus, 1)

        while len(bus) > 11:
            uslessProduct = min(bus, key=bus.get)     
            
            RemoveFromBus(uslessProduct, bus)

        for product in sorted(bus, key=bus.get):
            print(bus[product],  '\t', product)


def AddIngredientsToBus(product, bus, usage):
    recipeJson = FindRecipeByProduct(product)
    print("Proudct", product, "recipe", recipeJson["name"])
    #if  recipeJson["category"] == "smelting":
    #    fuel = "coal"
    #    bus[fuel] = bus.get(fuel, 0) + usage
    #    print("Add coal", usage, recipeJson["name"])
        
    for ingredientJson in recipeJson["ingredients"]:
        ingreidentName = ingredientJson["name"]
        if ingreidentName not in resourceList:
            bus[ingreidentName] = bus.get(ingreidentName, 0) + usage
            print("Add", ingreidentName, usage)
    
def RemoveFromBus(product, bus):
    print("Remove", product, bus[product])
    
    if product in resourceList:
        del bus[product]
    else:        
        ## Adding/updating usage of ingredients to bus
        usage = bus[product]
        AddIngredientsToBus(product, bus, usage)
        del bus[product]


def FindRecipeByProduct(product):    
    for recipeName, recipeJson in recipesJson.items():
        if recipeName not in blockedRecipes:
            for productJson in recipeJson["products"]:
                if product == productJson["name"]:
                    return recipeJson
        




if __name__ == '__main__':
    main()
