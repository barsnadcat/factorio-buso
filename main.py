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
"rocket-silo",
"satellite",
"electric-furnace",
"solid-fuel-from-heavy-oil",
"radar"])

# pump
# flame trower ammo
# landfill

resourceList = set(["raw-wood", "water", "iron-ore", "copper-ore", "coal", "crude-oil", "stone"])

recipesJson = None

def main():
	with open('recipes.json') as recipefp:
		global recipesJson
		recipesJson = json.load(recipefp)
		
		productUsage = {}
		recipes = set(allowedRecipes)

		for recipe in recipes:
			recipeJson = recipesJson[recipe]
			for ingredientJson in recipeJson["ingredients"]:
				ingreidentName = ingredientJson["name"]
				productUsage[ingreidentName] = productUsage.get(ingreidentName, 0) + 1

		while len(productUsage) > 10:
			uslessProduct = min(productUsage, key=productUsage.get)		
			print("Removing", uslessProduct)
			RemoveFromBus(uslessProduct, productUsage)

		for product in sorted(productUsage, key=productUsage.get):
			print(productUsage[product],  '\t', product)



			

	
def RemoveFromBus(product, productUsage):

	if product in resourceList:
		del productUsage[product]
	else:
		recipe = FindRecipeByProduct(product)
		recipeJson = recipesJson[recipe]

		for productJson in recipeJson["products"]:
			productName = productJson["name"]
			usage = productUsage[product]
			## Adding ingredients to bus for each usage of each product
			for ingredientJson in recipeJson["ingredients"]:
				ingreidentName = ingredientJson["name"]
				productUsage[ingreidentName] = productUsage.get(ingreidentName, 0) + usage
			## Removing product from bus
			del productUsage[productName]


def FindRecipeByProduct(product):
	for recipe in allowedRecipes:
		recipeJson = recipesJson[recipe]
		for productJson in recipeJson["products"]:
			if product == productJson["name"]:
				return recipe
		




if __name__ == '__main__':
	main()
