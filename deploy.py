#!/usr/bin/python3

import sys, os, shutil
from os import path
from urllib.request import pathname2url
import subprocess
from subprocess import call
import sys
import re
os.chdir(config.root_dir)
	OPERATING_SYSTEM = 'windows'
	COLORS_ENABLED = False # PowerShell does not support \...[...m color codes
elif 'linux' in sys.platform:
	OPERATING_SYSTEM = 'linux'
elif 'darwin' in sys.platform:
	OPERATING_SYSTEM = 'mac'
else:
	OPERATING_SYSTEM = 'unknown'
	"""
	make_parent_dir(file_path)
	
	Creates the parent directory for the specified filepath if it does not 
	already exist.
	
	file_path - path to some file
	"""
	parent_dir = path.dirname(file_path)
	if parent_dir == '': # means parent is working directory
		return
	if not path.isdir(parent_dir):
		os.makedirs(parent_dir)
make_dir(config.local_cache_dir)
make_dir(config.compile_dir)
make_dir(config.jar_dir)
make_dir(config.deploy_dir)
make_dir(config.deploy_image_dir)
make_dir(config.run_dir)
make_dir(config.src_dir)
make_dir(config.resource_dir)
	"""
	Deletes a file or recursively deletes a directory. Use with caution.
	"""
	if(path.isdir(filepath)):
		for f in os.listdir(filepath):
			_del(path.join(filepath,f))
		os.rmdir(filepath)
	elif(path.exists(filepath)):
		os.remove(filepath)
def del_file(filepath):
	"""
	del_file(filepath):
	
	Deletes a file or recursively deletes a directory. Use with caution.
	
	filepath - path to file or directory to delete
	"""
	if(path.isdir(filepath)):
		for f in os.listdir(filepath):
			_del(path.join(filepath,f))
		os.rmdir(filepath)
	elif(path.exists(filepath)):
		os.remove(filepath)
	""" 
	del_contents(dirpath)
	
	Recursively deletes the contents of a directory, but not the directory itself
	
	dirpath - path to directory to clean-out
	"""
	if(path.isdir(dirpath)):
		for f in os.listdir(dirpath):
			del_file(path.join(dirpath,f))
del_contents(config.run_dir)
del_contents(config.jar_dir)
del_contents(config.compile_dir)
del_contents(config.deploy_dir)
del_contents(config.deploy_image_dir)
def list_files(dirpath):
	"""
	list_filetree(dirpath)
	
	Returns a list of all files inside a directory (recursive scan)
	
	dirpath - filepath of directory to scan
	"""
	file_list = []
		for base, directories, files in os.walk(_dir_):
			for f in files:
				file_list.append(path.join(base,f))
	return file_list
	"""
	safe_quote_string(text)
	
	returns the text in quotes, with escapes for any quotes in the text itself
	
	text - input text to quote
	
	returns: text in quotes with escapes
	"""
	text2 = text.replace('\\', '\\\\')
	text3 = text2.replace('"', '\"')
	return '"'+text3+'"'
command_list += ['-d', config.compile_dir]
command_list += ['--module-source-path', config.src_dir]
command_list += ['--module', config.module_name]
command_list += ['--module-path',  os.pathsep.join(module_paths)]
call([config.javac_exec, '@'+str(arg_file)], cwd=config.root_dir)
		list_files(config.resource_dir), 
		config.src_dir,
		config.compile_dir
)
command_list += ['--module-path', os.pathsep.join(module_paths + [config.compile_dir])]
command_list += ['--add-modules', config.module_name]
command_list += ['--output', image_dir]
	file_content = ' '.join(map(safe_quote_string, command_list))
	fout.write(file_content)
	print('@%s: %s' % (arg_file, file_content))
call([config.jlink_exec, '@'+str(arg_file)], cwd=config.root_dir)
if OPERATING_SYSTEM == 'linux':
	with open(path.join(image_dir, 'launch.sh'), 'w') as fout:
		fout.write('#!/bin/bash\nTHIS_DIR="`dirname "$0"`"\n"${THIS_DIR}bin/java" -m '+config.module_name+'/'+config.main_class+'\n')
if OPERATING_SYSTEM == 'mac':
	with open(path.join(image_dir, 'launch.sh'), 'w') as fout:
		fout.write('#!/bin/bash\nTHIS_DIR="`dirname "$0"`"\n"${THIS_DIR}bin/java" -m '+config.module_name+'/'+config.main_class+'\n')