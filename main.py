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
"science-pack-1",
"science-pack-2",
"science-pack-3",
"high-tech-science-pack",
"production-science-pack",
"military-science-pack",
"steam-engine",
"steel-chest",
"iron-chest",
"steel-furnace"])


resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone", "radar"])

recipesJson = None
technologiesJson = None
productUsage = {}
recipeRequiredItems = {}
productRecipes = {}

minScore = 999999
bestPlan = None

def main():
	with open('technologies.json') as techfp:
		with open('recipes.json') as recipefp:
			global recipesJson
			recipesJson = json.load(recipefp)
			
			global productUsage
			global productRecipes

			for name in allowedRecipes:
				recipeJson = recipesJson[name]
				for productJson in recipeJson["products"]:
					productRecipes[productJson["name"]] = name
			print (productRecipes)

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

			print("Go!")
			GoDeeper(GetLeafRecipes(necessaryRecipes), set(resourceList), {}, [], 0)
			print("Best plan", minScore, bestPlan)
	


def GoDeeper(recipes, products, bus, plan, score):
	global minScore
	global bestPlan
	if recipes == set():
		
		if score < minScore or bestPlan == None:
			minScore = score
			bestPlan = plan
			print("New best plan", score, plan)
			
	else:
		for recipe in recipes:
			if IsValid(recipe, products):
				
				newPlan = list(plan)
				newBus = dict(bus)
				newProducts = set(products)
				newRecipes = set(recipes)

				newRecipes = newRecipes.difference(AddToBus(recipe, newProducts, newBus))

				newPlan.append(recipe)
				newScore = score + len(newBus)

				#print("Depth", len(newPlan), "score", score, plan)

				GoDeeper(newRecipes, newProducts, newBus , newPlan, newScore)


def IsValid(recipe, products):
	if recipe in recipeRequiredItems and not recipeRequiredItems[recipe].issubset(products):
		return False

	recipeJson = recipesJson[recipe]
	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		if ingredientName not in products:
			if not IsValid(productRecipes[ingredientName], products):
				return False
	return True


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
			result = result.union(AddToBus(productRecipes[ingredientName], products, bus))


	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		usage = productUsage[ingredientName]
		## Introducing new resource
		if ingredientName not in bus and ingredientName in resourceList:			
			bus[ingredientName] = usage
			#print("New line", ingredientName, len(bus))
		## Using stuff on bus
		bus[ingredientName] -= 1
		## Droping stuff from bus
		if bus[ingredientName] == 0:
			del bus[ingredientName]
			#print("Close line", ingredientName, len(bus))

	#print("Do", recipe)

	for productJson in recipeJson["products"]:
		productName = productJson["name"]
		products.add(productName)
		usage = productUsage.get(productName, 0)
		if usage > 0:
			bus[productName] = usage
			#print("New line", productName, len(bus))


	return result

	
	
def IsAllResearched(recipes, products):
	for recipeName in recipes:
		if recipeName in recipeRequiredItems and not recipeRequiredItems[recipeName].issubset(products):
			return False
	return True


def GetSubRecipes(recipe, products):
	result = set()
	result.add(recipe)

	recipeJson = recipesJson[recipe]
	for ingredientJson in recipeJson["ingredients"]:
		ingredientName = ingredientJson["name"]
		if ingredientName not in products:
			result = result.union(GetSubRecipes(productRecipes[ingredientName], products))

	return result

def GetRecipeProductUsage(recipe):
	recipeJson = recipesJson[recipe]
	result = 0
	for productJson in recipeJson["products"]:
		result += productUsage.get(productJson["name"], 0)
	return result



if __name__ == '__main__':
	main()