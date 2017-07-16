import json
import os

necessaryRecipes = set(["advanced-oil-processing",
"accumulator",
"advanced-circuit",
"assembling-machine-1",
"assembling-machine-2",
"battery",
"big-electric-pole",
"boiler",
"cargo-wagon",
"chemical-plant",
"concrete",
"construction-robot",
"copper-cable",
"copper-plate",
"electric-engine-unit",
"electric-mining-drill",
"electronic-circuit",
"engine-unit",
"express-splitter",
"express-transport-belt",
"express-underground-belt",
"fast-inserter",
"fast-splitter",
"fast-transport-belt",
"fast-underground-belt",
"filter-inserter",
"firearm-magazine",
"fluid-wagon",
"flying-robot-frame",
"gate",
"grenade",
"gun-turret",
"hazard-concrete",
"high-tech-science-pack",
"inserter",
"iron-chest",
"iron-gear-wheel",
"iron-plate",
"iron-stick",
"lab",
"laser-turret",
"locomotive",
"logistic-chest-passive-provider",
"logistic-chest-storage",
"logistic-robot",
"long-handed-inserter",
"low-density-structure",
"lubricant",
"medium-electric-pole",
"military-science-pack",
"offshore-pump",
"oil-refinery",
"piercing-rounds-magazine",
"pipe",
"pipe-to-ground",
"plastic-bar",
"processing-unit",
"production-science-pack",
"pumpjack",
"rail",
"rail-chain-signal",
"rail-signal",
"repair-pack",
"roboport",
"rocket-control-unit",
"rocket-fuel",
"rocket-part",
"science-pack-1",
"science-pack-2",
"science-pack-3",
"small-electric-pole",
"solar-panel",
"speed-module",
"splitter",
"stack-filter-inserter",
"stack-inserter",
"steam-engine",
"steel-chest",
"steel-furnace",
"steel-plate",
"stone-brick",
"stone-furnace",
"stone-wall",
"storage-tank",
"substation",
"sulfur",
"sulfuric-acid",
"train-stop",
"transport-belt",
"underground-belt",
"wood",
"rocket-silo",
"satellite",
"electric-furnace",
"solid-fuel-from-heavy-oil"])

resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone", "radar"])

recipesJson = None
ingredientUsage = {}

def main():
	with open('recipes.json') as fp:
		global recipesJson
		recipesJson = json.load(fp)

		global ingredientUsage

		for name in necessaryRecipes:
			recipeJson = recipesJson[name]
			for ingredientJson in recipeJson["ingredients"]:
				ingreidentName = ingredientJson["name"]
				ingredientUsage[ingreidentName] = ingredientUsage.get(ingreidentName, 0) + 1


		bus = set(resourceList)
		recipes = set(necessaryRecipes)

		while recipes != set():
			print(bus)

			leafRecipes = GetLeafRecipes(GetAvailableRecipes(recipes, bus))
			for recipe in leafRecipes:
				## Use recipe
				print("Use ", recipe)
				recipes.remove(recipe)
		

			bestNewLine = GetBestNewLine(GetAvailableRecipes(recipes, bus))

			## Use recipe
			print("Use ",bestNewLine)
			recipes.remove(bestNewLine)
			AddProductsToBus(bus, bestNewLine)


	
def AddProductsToBus(bus, recipe):
	recipeJson = recipesJson[recipe]
	for productJson in recipeJson["products"]:
		bus.add(productJson["name"])

def GetLeafRecipes(recipes):
	result = set()

	for recipe in recipes:
		totalProductUsage = GetRecipeTotalProductUsage(recipe)
		if totalProductUsage == 0:
			result.add(recipe)

	return result

def GetRecipeTotalProductUsage(recipe):
	recipeJson = recipesJson[recipe]
	result = 0
	for productJson in recipeJson["products"]:
		result += ingredientUsage.get(productJson["name"], 0)
	return result


def GetBestNewLine(recipes):
	m = 0
	best = ""

	for recipe in recipes:
		totalProductUsage = GetRecipeTotalProductUsage(recipe)
		if totalProductUsage > m:
			m = totalProductUsage
			best = recipe

	return best


def GetAvailableRecipes(recipes, bus):
		result = set()
		
		for recipeName in recipes:
			ingredients = set()
			
			recipeJson = recipesJson[recipeName]
			for ingredientJson in recipeJson["ingredients"]:
				ingredients.add(ingredientJson["name"])

			if ingredients.issubset(bus):
				result.add(recipeName)

		return result


		
## udpate bus
## find out aviable recipes with current bus
## add available line closing recipes
## add leaf recipes
## add new line recipe
##     with most leaf consumers?
##     with most line closing consumers?
##     with most consumers?
## ...

if __name__ == '__main__':
	main()