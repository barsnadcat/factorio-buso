import json
import os

necessaryRecipes = set(["basic-oil-processing",
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
technologiesJson = None
productUsage = {}
recipeRequiredItems = {}

def main():
	with open('technologies.json') as techfp:
		with open('recipes.json') as recipefp:
			global recipesJson
			recipesJson = json.load(recipefp)
			
			global productUsage
			for name in necessaryRecipes:
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

			BuildBus()



def BuildBus():
	recipes = set(necessaryRecipes)
	products = set(resourceList)

	while recipes != set():
		leafRecipes = GetLeafRecipes(GetAvailableRecipes(recipes, products))
		if leafRecipes != set():
			for recipe in leafRecipes:
				print("Add leaf ", recipe)
				recipes.remove(recipe)
				AddProducts(products, recipe)
		else:
			bestNewLine = GetBestNewLine(GetAvailableRecipes(recipes, products))
			print("New line ",bestNewLine)
			recipes.remove(bestNewLine)
			AddProducts(products, bestNewLine)


def AddProducts(products, recipe):
	recipeJson = recipesJson[recipe]
	for productJson in recipeJson["products"]:
		products.add(productJson["name"])

def GetLeafRecipes(recipes):
	result = set()

	for recipe in recipes:
		usage = GetRecipeProductUsage(recipe)
		if usage == 0:
			result.add(recipe)

	return result

def GetRecipeProductUsage(recipe):
	recipeJson = recipesJson[recipe]
	result = 0
	for productJson in recipeJson["products"]:
		result += productUsage.get(productJson["name"], 0)
	return result


def GetBestNewLine(recipes):
	m = 999
	best = ""

	for recipe in recipes:
		usage = GetRecipeProductUsage(recipe)
		if usage < m:
			m = usage
			best = recipe

	return best


def GetAvailableRecipes(recipes, products):
		result = set()
		for recipeName in recipes:
			if recipeName not in recipeRequiredItems or recipeRequiredItems[recipeName].issubset(products):
				ingredients = set()
				
				recipeJson = recipesJson[recipeName]
				for ingredientJson in recipeJson["ingredients"]:
					ingredients.add(ingredientJson["name"])

				if ingredients.issubset(products):
					result.add(recipeName)

		return result


		
## udpate bus
## find out aviable recipes with current products, including scinence packs
## add leaf recipes
## add new line recipe
##     with most consumers? -- no
##     1 добавлять сталь в начале, пока есть еще много рецептов которые можно стделать без нее - плохо
##     2 добавлять проволоку на бас в начале ради зеленых плат, полохо - она понадобится потом не скоро!
## ...

if __name__ == '__main__':
	main()