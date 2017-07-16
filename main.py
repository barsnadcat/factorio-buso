import json
import os

allowedRecipes = set(["basic-oil-processing",
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

necessaryRecipes = set([
"assembling-machine-1",
"assembling-machine-2",
"boiler",
"chemical-plant",
"construction-robot",
"logistic-robot",
"electric-mining-drill",
"express-splitter",
"express-transport-belt",
"express-underground-belt",
"fast-splitter",
"fast-transport-belt",
"fast-underground-belt",
"splitter",
"transport-belt",
"underground-belt",
"inserter",
"fast-inserter",
"stack-filter-inserter",
"stack-inserter",
"filter-inserter",
"firearm-magazine",
"gun-turret",
"lab",
"laser-turret",
"logistic-chest-passive-provider",
"logistic-chest-storage",
"long-handed-inserter",
"low-density-structure",
"medium-electric-pole",
"offshore-pump",
"oil-refinery",
"piercing-rounds-magazine",
"pipe",
"pipe-to-ground",
"pumpjack",
"repair-pack",
"roboport",
"rocket-part",
"science-pack-1",
"science-pack-2",
"science-pack-3",
"high-tech-science-pack",
"production-science-pack",
"military-science-pack",
"small-electric-pole",
"big-electric-pole",
"steam-engine",
"steel-chest",
"iron-chest",
"steel-furnace",
"stone-furnace",
"stone-wall",
"storage-tank",
"rocket-silo",
"satellite"])


resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone", "radar"])

recipesJson = None
technologiesJson = None
productUsage = {}
recipeRequiredItems = {}

def main():
	with open('technologies.json') as techfp:
		with open('recipes.json') as recipefp:
			global recipesJson
			recipesJson = json.load(recipefp)
			
			global productUsage

			recipes = set()
			for name in necessaryRecipes:
				recipes = recipes.union(GetSubRecipes(name, resourceList))

			for name in recipes:
				recipeJson = recipesJson[name]
				for ingredientJson in recipeJson["ingredients"]:
					ingreidentName = ingredientJson["name"]
					productUsage[ingreidentName] = productUsage.get(ingreidentName, 0) + 1

			global technologiesJson
			technologiesJson = json.load(techfp)

			global recipeRequiredItems
			for techName in technologiesJson:
				techJson = technologiesJson[techName]

				requiredItems = set()
				techIngredientsJson = techJson['research_unit_ingredients']
				for ingredientJson in techIngredientsJson:
					if ingredientJson["type"] == "item":
						requiredItems.add(ingredientJson["name"])

				effectsJson = techJson["effects"]
				for effectJson in effectsJson:
					if effectJson["type"] == "unlock-recipe":
						unlockedRecipe = effectJson["recipe"]
						recipeRequiredItems[effectJson["recipe"]] = set(requiredItems)

			BuildBus2()

def BuildBus2():
	recipes = set(necessaryRecipes)
	products = set(resourceList)
	bus = {}

	while recipes != set():
		## Calculate wieght - total number of required sub recipies for remaining recipes
		## Filter out unavailable because of research dependencies
		weights = {}
		for recipe in recipes:
			s = GetSubRecipes(recipe, products)
			if IsAllResearched(s, products):
				weights[recipe] = len(s)

		## Recipe that has all necessary stuff on products has 1 weight, and is the best to use.
		## What if we have 2 recipes with same weight? Rcipe with lower product usage takes priority

		best = None
		mw = 999
		mu = 999
		for recipe, weight in weights.items():
			usage = GetRecipeProductUsage(recipe)
			if weight < mw or weight == mw and usage < mu:
				best = recipe
				mw = weight
				mu = usage
		
		## Now we have some recipe, that may not have all ingedients on products. 
		## We need add all of its requrements who are not on products first, using recursion

		recipes = recipes.difference(AddToBus(best, products, bus))


def AddToBus(recipe, products, bus):
	result = set()
	result.add(recipe)

	recipeJson = recipesJson[recipe]
	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		if ingredientName not in products:
			result = result.union(AddToBus(FindRecipeByProduct(ingredientName), products, bus))


	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		## Introducing new resource
		if ingredientName not in bus and ingredientName in resourceList:			
			bus[ingredientName] = productUsage[ingredientName]
			print("New line", ingredientName, len(bus))
		## Using stuff on bus
		bus[ingredientName] -= 1
		## Droping stuff from bus
		if bus[ingredientName] == 0:
			del bus[ingredientName]
			print("Close line", ingredientName, len(bus))

	print("Do", recipe)

	for productJson in recipeJson["products"]:
		productName = productJson["name"]
		products.add(productName)
		usage = productUsage.get(productName, 0)
		if usage > 0:
			bus[productName] = usage
			print("New line", productName, len(bus))

	##print(len(bus), bus.keys())

	return result

	
	
def IsAllResearched(recipes, products):
	for recipeName in recipes:
		if recipeName in recipeRequiredItems and not recipeRequiredItems[recipeName].issubset(products):
			return False
	return True

def FindRecipeByProduct(product):
	for recipe in allowedRecipes:
		recipeJson = recipesJson[recipe]
		for productJson in recipeJson["products"]:
			if product == productJson["name"]:
				return recipe

def GetSubRecipes(recipe, products):
	result = set()
	result.add(recipe)

	recipeJson = recipesJson[recipe]
	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		if ingredientName not in products:
			result = result.union(GetSubRecipes(FindRecipeByProduct(ingredientName), products))

	return result

def GetRecipeProductUsage(recipe):
	recipeJson = recipesJson[recipe]
	result = 0
	for productJson in recipeJson["products"]:
		result += productUsage.get(productJson["name"], 0)
	return result



if __name__ == '__main__':
	main()