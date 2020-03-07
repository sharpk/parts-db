import xml.etree.ElementTree as ET

root = None

def parse_hierarchy_xml(xml_file):
	global root
	tree = ET.parse(xml_file)
	root = tree.getroot()

def find_child_by_id(id):
	for child in root.iter('child'):
		if child.attrib['id'] == id:
			return child
	return None

# get string of class names starting from root to given id
def get_class_string(id):
	delimiter = '.'
	name_list = list()
	class_iter = find_child_by_id(id)
	while class_iter != None and class_iter.tag == 'child':
		name_list.append(class_iter.attrib['name'])
		class_iter = root.find('.//child[@id="' + class_iter.attrib['id'] + '"]/..')  # get parent node
	name_list.reverse()
	return_str = ""
	for name in name_list:
		return_str = return_str + delimiter + name
	return return_str[1:]

# get list of child id values for given id
def get_class_children(id):
	id_list = list()
	
	start_class = find_child_by_id(id)
	if start_class:
		for child in start_class.iter('child'):
			id_list.append(child.attrib['id'])
	return id_list

# get a sorted list of tuples which contains the id followed by the 
# class string. Sorted by the class string
def get_linear_class_list():
	d = dict()
	for child in root.iter('child'):
		d[int(child.attrib['id'])] = get_class_string(child.attrib['id'])
	return sorted(d.items(), key=lambda kv: kv[1])
