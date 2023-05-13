import os
import sys

import win_p_dump

def get_windows_info():
	system_info = os.popen("systeminfo")

	system_data = {}
	need = ['Host Name', 'OS Name', 'System Type', 'Total Physical Memory', 'Available Physical Memory']
	for i in system_info:
		i=i.split(":")
		if i[0] in need:
			system_data[i[0]] = i[1].strip(" \n")

	# print(system_data)
	return system_data

def get_linux_info():
	system_data={}

	a = os.popen("uname --all")
	for j in a:
		j = j.split(" ")
		system_data['OS Name'] = j[0]
		system_data['Host Name'] = j[1]
		system_data['System Type'] = j[-2]

	need = ['MemTotal', 'MemAvailable']
	with open(r"/proc/meminfo", "r+") as ff:
		content = ff.readlines()
	
	for i in content:
		i = i.split(":")
		if i[0] in need:
			system_data[i[0]] = i[1].strip(" \n")

	# print(system_data)
	return system_data

def get_mac_info():
	pass


basic_os = sys.platform
if "win" in basic_os:
	system_info = get_windows_info()
	win_p_dump.main(meta_data = system_info)

elif "linux" in basic_os:
	get_linux_info()

elif "darwin" in basic_os:
	get_mac_info()


input()