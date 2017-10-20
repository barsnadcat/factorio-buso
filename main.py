import json
import os

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
        	bus[product] = 1

        while len(bus) > 11:
            uslessProduct = min(bus, key=bus.get)     
            RemoveFromBus(uslessProduct, bus)

        for product in sorted(bus, key=bus.get):
            print(bus[product],  '\t', product)


def AddToBus(recipeJson, bus, usage):
    if  recipeJson["category"] == "smelting":
        fuel = "coal"
        bus[fuel] = bus.get(fuel, 0) + usage
        print("Add coal", usage, recipeJson["name"])
        
    for ingredientJson in recipeJson["ingredients"]:
        ingreidentName = ingredientJson["name"]
        bus[ingreidentName] = bus.get(ingreidentName, 0) + usage
        print("Add", ingreidentName, usage, recipeJson["name"])
    
def RemoveFromBus(product, bus):

    if product in resourceList:
        print("Del", product, bus[product])
        del bus[product]
    else:
        recipeJson = FindRecipeByProduct(product)
        usage = bus[product]

        ## Adding/updating usage of ingredients to bus
        AddToBus(recipeJson, bus, usage)

        ## Removing product from bus
        print("Del", product, bus[product], recipeJson["name"])
        del bus[product]


def FindRecipeByProduct(product):    
    for recipeName, recipeJson in recipesJson.items():
        if recipeName not in blockedRecipes:
            for productJson in recipeJson["products"]:
                if product == productJson["name"]:
                    return recipeJson
        




if __name__ == '__main__':
    main()
