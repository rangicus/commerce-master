# Imports

import PySimpleGUI as sg
import re, math
from typing import List

# Classes

class Item:
	def __init__ (self, name: str, stackSize: int, weight: int):
		self.name = name
		self.stackSize = stackSize
		self.weight = weight
		self.prices = None

class TradingPost:
	def __init__ (self, name: str, items: List[Item]):
		self.name = name
		self.items = items

class Vehicle:
	def __init__ (self, name: str, slots: int, maxWeight: int, speed: float, snowSpeed: float = None, sandSpeed: float = None):
		self.name = name
		self.slots = slots
		self.maxWeight = maxWeight

		self.speed = speed
		self.snowSpeed = snowSpeed if snowSpeed != None else speed
		self.sandSpeed = sandSpeed if sandSpeed != None else speed

class Route:
	def __init__ (self, dest: TradingPost, vehicle: Vehicle, item: Item, quantity: int):
		self.dest = dest
		self.vehicle = vehicle
		self.item = item
		self.quantity = quantity

		self.totalProfit = self.getTotalProfit()

	def getTotalProfit (self):
		singleProfit = int(self.item.prices[self.dest.name])
		return singleProfit * self.quantity

# Data

TRADING_POSTS = [
	TradingPost("Tir Chonaill", [
		Item("Baby Potion", 80, 1),
		Item("Diet Potion", 100, 1),
		Item("Snore Prevention Potion", 60, 2),
		Item("Wild Ginseng Potion", 40, 3)
	]),
	TradingPost("Dunbarton", [
		Item("Spider Gloves", 10, 5),
		Item("Wool Boots", 10, 8),
		Item("Ogre Executioner Mask", 45, 4),
		Item("Incubus Suit", 5, 25),
	]),
	TradingPost("Bangor", [
		Item("Bangor Coal", 10, 8),
		Item("Marble", 10, 20),
		Item("Topaz", 6, 20),
		Item("Highlander Ore", 8, 25)
	]),
	TradingPost("Emain Macha", [
		Item("Berry Granola", 40, 3),
		Item("Butter Beer", 30, 4),
		Item("Smoked Wild Animal", 40, 3),
		Item("Triple Pasta", 50, 4),
	]),
	TradingPost("Taillteann", [
		Item("Heat Crystal", 60, 2),
		Item("Music Box Preservation Stone", 40, 3),
		Item("Palala Crystal", 100, 2),
		Item("Circle Barrier Spikes Crystal", 60, 3),
	]),
	TradingPost("Tara", [
		Item("Mini Dressing Table", 12, 9),
		Item("Tea Table", 5, 25),
		Item("Rocking Chair", 5, 25),
		Item("Bunk Bed", 3, 60),
	]),
	TradingPost("Cobh", [
		Item("Cobh Seaweed", 50, 2),
		Item("Cobh Oyster", 40, 3),
		Item("Shark Fin", 30, 4),
		Item("Jellyfish", 30, 6),
	]),
	TradingPost("Belvast", [
		Item("Iron Whip", 15, 8),
		Item("Dark Sword", 10, 12),
		Item("Safe", 1, 160),
		Item("Skeleton Ogre Armor", 1, 160),
	]),
	TradingPost("Qilla", [
		Item("Mint Chocolate Powder", 100, 1),
		Item("Fresh Pomegranate", 100, 1),
		Item("Mana Tunnel Figure", 80, 2),
		Item("Exploration Rescue Kit", 50, 3),
	]),
	TradingPost("Filia", [
		Item("Small Glass Chunk", 60, 10),
		Item("Cinnamon Perfume", 50, 30),
		Item("Dried Saffron", 10, 25),
		Item("Longa Natural Rock Salt", 5, 40),
	]),
	TradingPost("Cor", [
		Item("Courcle Ruins Souvenir", 50, 2),
		Item("Large Ritual Mask", 40, 3),
		Item("La Terra Raspberry", 60, 2),
		Item("Artifact Restoration Tool Set", 70, 2),
	]),
	TradingPost("Vales", [
		Item("Vales Padded Coat", 50, 1),
		Item("Natural Glacial Water", 35, 2),
		Item("Ice Skates", 50, 1),
		Item("Snowboard", 20, 3)
	]),
]

VEHICLES = [
	Vehicle("[P] Backpack", 5, 500, 0.91),
	Vehicle("[P] Handcart", 7, 900, 1),
	Vehicle("[A] Wagon", 10, 1100, 1.9),
	Vehicle("[P] Pack Elephant", 8, 1800, 1.37),
	Vehicle("[P] Swift Dog Sled", 12, 900, 1.86, 3.09),
	Vehicle("[P] Stalwart Camel", 8, 1600, 2.15, 1.33, 3.07),
	Vehicle("[P] Magnate's Skiff", 9, 1400, 2.4)
]

selectedTradingPost = None
selectedItem: Item | None = None

# Functions

def createLayout ():
	colSelect = sg.Column(
		expand_y=True,
		layout=[
			[
				sg.Text("Trading Post:"),
				sg.Combo(
					values=getTradingPostNames(),
					key="optionTradingPost",
					enable_events=True,
					default_value=TRADING_POSTS[0].name
				),
			],

			[sg.Frame(
				title="Items",
				key="frameItems",
				expand_x=True,
				expand_y=True,
				visible=False,
				layout=[ [sg.Button("", key=f"buttonItem{i}", expand_x=True)] for i in range(5) ]
			)],

			[sg.Button("Exit", expand_x=True)]
		]
	)

	colPrices = sg.Column([
		[sg.Frame(
			title="Prices",
			key="framePrices",
			expand_x=True,
			element_justification="right",
			visible=False,
			layout=[
				*[
					[
						sg.Text("Post Name:", key=f"textPrice{i}"),
						sg.Input("", key=f"inputPrice{i}", enable_events=True, size=(6, 1))
					]
					for i in range(len(TRADING_POSTS)-1)
				],
				[sg.Button("Clear", expand_x=True, k="buttonClear")]
			]
		)]
	])

	colResults = sg.Column(
		expand_x=True,
		expand_y=True,
		layout=[
			[sg.Table([["", ""]], k="tableRoutes", expand_x=True, expand_y=True, headings=["Destination", "Item", "Amount", "Total Profit"])],
			[sg.Button("Calculate", k="buttonCalc", expand_x=True)]
		]
	)

	return [
		[colSelect, colPrices, colResults],
	]

def getTradingPostNames () -> List[str]:
	global TRADING_POSTS
	return list(map(lambda x: x.name, TRADING_POSTS))

def getTradingPost (name: str):
	global TRADING_POSTS

	for post in TRADING_POSTS:
		if post.name == name:
			return post

	raise ValueError("Unknown Post")

def chooseTradingPost (name: str):
	global selectedTradingPost, selectedItem, window

	selectedItem = None
	window["framePrices"].update(visible=False)

	selectedTradingPost = getTradingPost(name)
	print("Trading Post:", selectedTradingPost.name)

	window["frameItems"].update(visible=True)
	updateItems()

def chooseItem (item: Item):
	global selectedItem, window

	selectedItem = item
	print("Item:", item.name)

	window["framePrices"].update(value=f"Prices - {item.name}", visible=True)
	updatePrices()

def updateItems ():
	# Hide all buttons.
	for i in range(0, 5):
		window[f"buttonItem{i}"].update(visible=False)
	if selectedTradingPost == None: return
	
	# Update necessary ones
	i = 0
	for item in selectedTradingPost.items:
		window[f"buttonItem{i}"].update(text=item.name, visible=True)
		i += 1

def updatePrices ():
	global selectedTradingPost, selectedItem, window

	if selectedTradingPost == None: return
	if selectedItem == None: return

	# Set default prices.
	if selectedItem.prices == None:
		selectedItem.prices = {}
		for post in TRADING_POSTS:
			if selectedItem not in post.items:
				selectedItem.prices[post.name] = ""

	# Set Display Values
	i = 0
	for post in TRADING_POSTS:
		if selectedItem not in post.items:
			window[f"textPrice{i}"].update(post.name + ":")
			
			inputPrice = window[f"inputPrice{i}"]
			inputPrice.update(selectedItem.prices[post.name])
			inputPrice.metadata = post
			
			i += 1

def calculateRoutes ():
	if selectedTradingPost == None: return

	routes: List[Route] = []
	for post in TRADING_POSTS:
		if post != selectedTradingPost:
			# Each possible destination.
			for vehicle in VEHICLES:
				# Each possible vehicle.
				for item in selectedTradingPost.items:
					if item.prices == None: continue
					
					# Profit per Item?
					rawSingleProfit = re.sub("\D", "", item.prices[post.name])
					if len(rawSingleProfit) == 0: continue

					# How many?
					maxBySlots = item.stackSize * vehicle.slots
					maxByWeight = math.floor(vehicle.maxWeight / item.weight)
					itemQuantity = min(maxBySlots, maxByWeight)

					routes.append(
						Route(post, vehicle, item, itemQuantity)
					)

	routes.sort(key=(lambda r: -r.getTotalProfit()))
	window["tableRoutes"].update(values=tableFromRoutes(routes))

def clearCurrentItem ():
	if selectedItem == None: return

	for post in TRADING_POSTS:
		if selectedItem not in post.items:
			selectedItem.prices[post.name] = ""

	i = 0
	for post in TRADING_POSTS:
		if selectedItem not in post.items:
			window[f"textPrice{i}"].update(post.name + ":")
			
			inputPrice = window[f"inputPrice{i}"]
			inputPrice.update(selectedItem.prices[post.name])
			inputPrice.metadata = post
			
			i += 1

def tableFromRoutes (routes: List[Route]):
	rows = []
	for route in routes:
		rows.append([
			route.dest.name,
			route.item.name,
			numberComma(route.quantity),
			numberComma(route.totalProfit)
		])
	return rows

def numberComma (x: float):
	isNegative = (x < 0)
	if isNegative:
		x = -x
	
	decimal = x % 1
	x -= decimal
	if decimal == 0: decimal = ""
	else: decimal = f".{decimal}"

	x = str(x)[::-1]
	parts = []
	for i in range(0, len(x), 3):
		parts.append(x[i:i+3])
	x = ",".join(parts)[::-1] + decimal
	if isNegative: x = f"-{x}"
	return x

# Setup

layout = createLayout()
window = sg.Window("CommerceMaster", layout, finalize=True, resizable=True)

chooseTradingPost(TRADING_POSTS[0].name)
chooseItem(selectedTradingPost.items[0])

# Event Loop

DEBUG = False
while True:
	event, values = window.read()
	if DEBUG:
		print("Event:", event, values)

	if event == "Exit" or event == sg.WIN_CLOSED: break
	elif event == "optionTradingPost": chooseTradingPost(values["optionTradingPost"])
	elif event == "buttonCalc": calculateRoutes()
	elif event == "buttonClear": clearCurrentItem()
	elif str.startswith(event, "buttonItem"):
		index = int(re.sub("\D", "", event))
		chooseItem(selectedTradingPost.items[index])
	elif str.startswith(event, "inputPrice"):
		if selectedItem != None and selectedTradingPost != None:
			inputPrice = window[event]
			targetPost = inputPrice.metadata
			selectedItem.prices[targetPost.name] = values[event]
	else:
		print("Unknown Event:", event, values)

# Exit

print("Exiting...")
window.close()
