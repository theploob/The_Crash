import xml.etree.ElementTree as ET
import csv
import lib.constants

level_tree_root = []
csv_floor_header = '_____Walls_____'
csv_object_header = '_____Objects_____'
csv_enemy_header = '_____Enemies_____'
csv_enum = {csv_floor_header: 0, csv_object_header: 1, csv_enemy_header: 2}
map_layer_enum = {'FLOOR': 0, 'OBJECT': 1, 'ENEMY': 2}
csv_headers = [csv_floor_header, csv_object_header, csv_enemy_header]


class LayeredMap:
	# TODO: Change to take a config number for multiple map setups & configurations
	def __init__(self, layered_maps):
		self.floor_layer = layered_maps[map_layer_enum['FLOOR']]
		self.object_layer = layered_maps[map_layer_enum['OBJECT']]
		self.enemy_layer = layered_maps[map_layer_enum['ENEMY']]

	def get_floor(self):
		return self.floor_layer

	def get_object(self):
		return self.object_layer

	def get_enemy(self):
		return self.enemy_layer


class LevelMap:
	def __init__(self, name, x_size, y_size, layered_maps):
		self.name = name
		self.x_size = x_size
		self.y_size = y_size
		self.layered_map = LayeredMap(layered_maps)

	# Validate that this LevelMap is still good, returns Boolean
	def validate(self):
		m = self.layered_map.get_floor()
		for y in range(0, self.y_size):
			for x in range(0, self.x_size):
				if 0 <= m[y][x] <= 1:
					continue
				return False
		m = self.layered_map.get_object()
		for y in range(0, self.y_size):
			for x in range(0, self.x_size):
				if 0 <= m[y][x] <= lib.constants.MAX_OBJECT_ID_NUMBER:
					continue
				return False
		m = self.layered_map.get_floor()
		for y in range(0, self.y_size):
			for x in range(0, self.x_size):
				if 0 <= m[y][x] <= lib.constants.MAX_ENEMY_ID_NUMBER:
					continue
				return False
		return True


def xml_to_levelmap(xml_level, name):
	x_size = int(xml_level.find('size_x').text)
	y_size = int(xml_level.find('size_y').text)
	csvname = xml_level.find('csv').text
	maps = [None, None, None]
	mode = None
	section_counter = 0

	with open('assets\\' + csvname, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row_text in reader:
			if len(row_text) > 0:
				if row_text[0] in csv_headers:  # New header section
					# print("Found: {}".format(row_text[0][5:-5]))
					mode = csv_enum[row_text[0]]
					maps[mode] = []
					section_counter = 0
				else:  # Row of CSV, add to the map
					if section_counter < y_size:
						maps[mode].append(row_text[:x_size])
						section_counter += 1
	for i in range(0, 3):
		if maps[i] is None:
			print("Issue with map section {}".format(csv_headers[i]))
			return None

	for i in range(0, len(maps)):
		for j in range(0, len(maps[0])):
			for k in range(0, len(maps[0][0])):
				maps[i][j][k] = int(maps[i][j][k])

	ret_levelmap = LevelMap(name, x_size, y_size, maps)

	if ret_levelmap.validate():
		return ret_levelmap
	print("Error validating the created LevelMap")
	return None


def setup_levels():
	global level_tree_root
	level_tree = ET.parse('assets\\level_maps.xml')
	level_tree_root = level_tree.getroot()


# Takes a level name, returns the LevelMap object with the level parameters for the given name
def get_level_map(name):
	global level_tree_root

	if level_tree_root is []:
		setup_levels()
		if level_tree_root is []:
			print("Couldn't get the XML Level Tree Root")
			return

	for level in level_tree_root:
		if level.find('name').text == name:
			return xml_to_levelmap(level, name)
	print("Tried to load level {}: level doesn't exist".format(name))
	return None
