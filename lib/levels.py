import os
import xml.etree.ElementTree as ET
import csv

level_tree_root = None
csv_floor_header = '_____Walls_____'
csv_object_header = '_____Objects_____'
csv_enemy_header = '_____Enemies_____'
csv_enum = {csv_floor_header: 0, csv_object_header: 1, csv_enemy_header: 2}
csv_headers = [csv_floor_header, csv_object_header, csv_enemy_header]


class LevelMap:
	def __init__(self, name, x_size, y_size, map_layers):
		self.name = name
		self.x_size = x_size
		self.y_size = y_size
		self.setup_map_layers(map_layers)

	def setup_map_layers(self, layers):
		pass

def xml_to_LevelMap(xml_level, name):
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
						maps[mode].append(row_text[:x_size-1])
						section_counter += 1
	for i in range(0, 3):
		if maps[i] is None:
			print("Issue with map section {}".format(csv_headers[i]))
			return None

	ret_levelmap = LevelMap(name, x_size, y_size, maps)






	return ret_levelmap




def setup_levels():
	global level_tree_root
	level_tree = ET.parse('assets\\level_maps.xml');
	level_tree_root = level_tree.getroot()

# Takes a level name, returns the LevelMap object with the level parameters for the given name
def get_level_map(name):
	global level_tree_root

	if level_tree_root is None:
		setup_levels()
		if level_tree_root is None:
			print("Couldn't get the XML Level Tree Root")
			return

	for level in level_tree_root:
		if level.find('name').text == name:
			return xml_to_LevelMap(level, name)
	print("Tried to load level {}: level doesn't exist".format(name))
	return None
