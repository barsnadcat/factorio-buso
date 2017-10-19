import json
import os

allowedRecipes = set(["basic-oil-processing",
"accumulator",
"advanced-circuit",
"assembling-machine-1",
"assembling-machine-2",
"battery",
"big-electric-pole",
"medium-electric-pole",
"small-electric-pole",
"boiler",
"chemical-plant",
"concrete",
"construction-robot",
"copper-cable",
"copper-plate",
"electric-engine-unit",
"electric-mining-drill",
"electronic-circuit",
"engine-unit",
"fast-inserter",
"fast-splitter",
"fast-transport-belt",
"fast-underground-belt",
"firearm-magazine",
"fluid-wagon",
"cargo-wagon",
"train-stop",
"pump",
"locomotive",
"gate",
"grenade",
"gun-turret",
"high-tech-science-pack",
"inserter",
"iron-chest",
"iron-gear-wheel",
"iron-plate",
"iron-stick",
"lab",
"laser-turret",
"flying-robot-frame",
"logistic-chest-passive-provider",
"logistic-chest-storage",
"logistic-robot",
"long-handed-inserter",
"low-density-structure",
"lubricant",
"military-science-pack",
"offshore-pump",
"piercing-rounds-magazine",
"pipe",
"pipe-to-ground",
"plastic-bar",
"processing-unit",
"production-science-pack",
"pumpjack",
"rail",
"repair-pack",
"roboport",
"rocket-control-unit",
"rocket-fuel",
"rocket-part",
"science-pack-1",
"science-pack-2",
"science-pack-3",
"solar-panel",
"speed-module",
"splitter",
"steam-engine",
"steel-chest",
"steel-furnace",
"steel-plate",
"stone-brick",
"stone-furnace",
"stone-wall",
"storage-tank",
"sulfur",
"sulfuric-acid",
"transport-belt",
"underground-belt",
"wood",
"flamethrower-ammo",
"landfill",
"rocket-silo",
"satellite",
"electric-furnace",
"solid-fuel-from-heavy-oil",
"radar"])

resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone"])

recipesJson = None

def main():
    with open('recipes.json') as recipefp:
        global recipesJson
        recipesJson = json.load(recipefp)
        
        bus = {}
        recipes = set(allowedRecipes)

        for recipe in recipes:
            AddToBus(recipesJson[recipe], bus, 1)

        for product in sorted(bus, key=bus.get):
            print(bus[product],  '\t', product)

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
        print("Add", ingreidentName, usage)
    
def RemoveFromBus(product, bus):

    if product in resourceList:
        print("Del", product, bus[product])
        del bus[product]
    else:
        recipe = FindRecipeByProduct(product)
        recipeJson = recipesJson[recipe]
        usage = bus[product]

        ## Adding/updating usage of ingredients to bus
        AddToBus(recipeJson, bus, usage)

        ## Removing product from bus
        print("Del", product, bus[product], recipe)
        del bus[product]


def FindRecipeByProduct(product):
    for recipe in allowedRecipes:
        recipeJson = recipesJson[recipe]
        for productJson in recipeJson["products"]:
            if product == productJson["name"]:
                return recipe
        




if __name__ == '__main__':
    main()
