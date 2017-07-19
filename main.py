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
"big-electric-pole",
"steam-engine",
"steel-chest",
"iron-chest",
"steel-furnace",
"stone-furnace",
"stone-wall",
"storage-tank",
"rocket-silo",
"small-electric-pole",
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

			for product in sorted(productUsage, key=productUsage.get):
				print(productUsage[product],  '\t', product)

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
	print("Go!")
	recipes = GetLeafRecipes(necessaryRecipes)	
	products = set(resourceList)
	bus = {}
	totalBus = 0

	## Low volume line, that has all inputs on bus, can be removed right after each usage, and readded for each usage.

	while recipes != set():
		## Filter out unavailable because of research dependencies
		## Calculate wieght - total number of required sub recipies for leaf recipe
		## Recipe that has all necessary stuff on products has 1 weight, and is the best to use.
		## Storage tank problem - it has low weight, and low usage of components, but steel it introduces
		## is not going to be used by next like 5 productions, and it can be moved later at line.
		## We can calculate most needed lines for current available recipes, and use this as... well this is updated usage,
		## and inverted comparsion.
		## This steel does not help. Probably usage should include parent usage as well -- copper cable usage is low, 
		## but actually it helps alot.
		## !
		## Weight is number of new parents, with current bus, should include new lines count - removed lines count
		## Usage is number of children
		## What we need actually is count of new lines added specifically for this recipe. If other recipe adds lines, 
		## but they are used by another available recipe - it has higer priority.
		## Local usage how to account usage with children - copper wire is used not only by EC, but by all who use EC as well.

		best = None
		mw = 99999
		ml = 99999
		mu = 99999

		localUsage = {}
		for recipe in recipes:
			s = GetSubRecipes(recipe, products)
			if IsAllResearched(s, products):
				for subRecipe in s:			
					recipeJson = recipesJson[subRecipe]
					for ingredientJson in recipeJson["ingredients"]:
						ingreidentName = ingredientJson["name"]
						localUsage[ingreidentName] = localUsage.get(ingreidentName, 0) + 1

		for recipe in recipes:
			s = GetSubRecipes(recipe, products)
			if IsAllResearched(s, products):
				weight = len(s)

				newLines = 0 #number of new unique lines for this recipe
				
				for subRecipe in s:
					recipeJson = recipesJson[subRecipe]	
					for productJson in recipeJson["products"]:
						productName = productJson["name"]
						if productName in localUsage:
							if localUsage[productName] == 1:
								newLines += 1
								#print("_____", recipe, "New line", productName)
					for ingredientJson in recipeJson["ingredients"]:
						ingredientName = ingredientJson["name"]
						if ingredientName in bus:
							if bus[ingredientName] == 1:
								newLines -= 1
								#print("_____", recipe, "Remove from bus", ingredientName)
						else:
							if ingredientName not in resourceList and productUsage[ingredientName] == 1:
								newLines -= 1
								#print("_____", recipe, "Remove just added from bus", ingredientName)

				totalUsage = 0
				for subRecipe in s:
					totalUsage += GetRecipeProductUsage(subRecipe)

				print("   ", "newLines", newLines, "weight", weight,  "usage", totalUsage, recipe)
				if newLines < ml or newLines == ml and weight < mw or newLines == ml and weight == mw and totalUsage < mu:
				#if weight < mw or weight == mw and newLines < ml:
					best = recipe
					mw = weight
					ml = newLines
					mu = totalUsage
					

		
		## Now we have some recipe, that may not have all ingedients on products. 
		## We need add all of its requrements who are not on products first, using recursion

		recipes = recipes.difference(AddToBus(best, products, bus))
		totalBus += len(bus)

	print(totalBus)


def GetLeafRecipes(recipes):
	result = set()
	for recipe in recipes:
		if GetRecipeProductUsage(recipe) == 0:
			result.add(recipe)

	return result

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
		usage = productUsage[ingredientName]
		## Introducing new resource
		if ingredientName not in bus and ingredientName in resourceList:			
			bus[ingredientName] = usage
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