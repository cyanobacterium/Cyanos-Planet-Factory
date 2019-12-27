#!/usr/bin/python3

import sys, os, shutil
from os import path
from urllib.request import pathname2url
import subprocess
from subprocess import call
import sys
import re

import config

os.chdir(config.root_dir)

SUPPORTED_OPERATING_SYSTEMS = ('windows_x64', 'linux_x64', 'mac')#, 'linux-arm32', 'linux-arm64')


def make_dir(dir_path):
	"""
	make_dir(dir_path)

	creates a directory if it does not already exist, including parent 
	directories.

	dir_path - directory to create
	"""
	if not path.exists(dir_path):
		os.makedirs(dir_path)
def make_parent_dir(file_path):
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
def _del(filepath):
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
def del_contents(dirpath):
	""" 
	del_contents(dirpath)
	
	Recursively deletes the contents of a directory, but not the directory itself
	
	dirpath - path to directory to clean-out
	"""
	if(path.isdir(dirpath)):
		for f in os.listdir(dirpath):
			del_file(path.join(dirpath,f))
def list_files(dirpath):
	"""
	list_filetree(dirpath)
	
	Returns a list of all files inside a directory (recursive scan)
	
	dirpath - filepath of directory to scan
	"""
	if(type(dirpath) == str):
		dir_list = [dirpath]
	else:
		dir_list = dirpath
	file_list = []
	for _dir_ in dir_list:
		for base, directories, files in os.walk(_dir_):
			for f in files:
				file_list.append(path.join(base,f))
	return file_list
def safe_quote_string(text):
	"""
	safe_quote_string(text)
	
	returns the text in quotes, with escapes for any quotes in the text itself
	
	text - input text to quote
	
	returns: text in quotes with escapes
	"""
	text2 = text.replace('\\', '\\\\')
	text3 = text2.replace('"', '\"')
	return '"'+text3+'"'
def copy_tree(file_list, src_root, dest_root):
	"""
	copy_tree(file_list, src_root, dest_root)
	
	Copies all files to directory dest_root (creating it if necessary), 
	preserving the folder structure relative to src_root
	"""
	for f in file_list:
		rel_path = path.relpath(f, src_root)
		dst_path = path.join(dest_root, rel_path)
		make_parent_dir(dst_path)
		shutil.copy(f, dst_path)

# make dirs
make_dir(config.local_cache_dir)
make_dir(config.compile_dir)
make_dir(config.jar_dir)
make_dir(config.deploy_dir)
make_dir(config.deploy_image_dir)
make_dir(config.run_dir)
make_dir(config.src_dir)
make_dir(config.resource_dir)

# clean
del_contents(config.run_dir)
del_contents(config.jar_dir)
del_contents(config.compile_dir)
del_contents(config.deploy_dir)
del_contents(config.deploy_image_dir)

# compile (with jmods)
for release_OS in SUPPORTED_OPERATING_SYSTEMS:
	print('\n',release_OS,'\n')
	module_src_path = path.join(config.src_dir, config.module_name)
	if(release_OS == 'windows_x64'):
		java_home = 'D:\\CCHall\\Documents\\Programming\\OpenJDK_Distros\\windows-x64\\jdk-13.0.1'
		jmod_dirs = [java_home+os.sep+'jmods'] + config.jmod_dirs_windows_x64
	elif(release_OS == 'linux_x64'):
		java_home = 'D:\\CCHall\\Documents\\Programming\\OpenJDK_Distros\\linux-x64\\jdk-13.0.1'
		jmod_dirs = [java_home+os.sep+'jmods'] + config.jmod_dirs_linux_x64
	elif(release_OS == 'mac'):
		java_home = 'D:\\CCHall\\Documents\\Programming\\OpenJDK_Distros\\osx-x64\\jdk-13.0.1'
		jmod_dirs = [java_home+os.sep+'jmods'] + config.jmod_dirs_mac
	else:
		print('UNSUPPORTED OS: %s' % release_OS)
	arg_file = path.join(config.local_cache_dir, 'javac-args.txt')
	command_list = []
	command_list += ['-encoding', 'utf8']
	command_list += ['-d', config.compile_dir]
	command_list += ['--module-source-path', config.src_dir]
	command_list += ['--module', config.module_name]
	module_paths = jmod_dirs + [f for f in list_files(config.dependency_dirs) if str(f).endswith('.jar')] # a .jmod file is auto-discoverable by --module-path
	command_list += ['--module-path',  os.pathsep.join(['%s/jmods' % java_home]+module_paths)]
	with open(arg_file, 'w') as fout:
		file_content = ' '.join(map(safe_quote_string, command_list))
		fout.write(file_content)
		print('@%s: %s' % (arg_file, file_content))
	call([config.javac_exec, '@'+str(arg_file)], cwd=config.root_dir)
	# need to copy resources separately
	resource_files = list_files(config.resource_dir)
	resource_files += [f for f in list_files(config.src_dir) if str(f).endswith('.java') == False]
	copy_tree(
			list_files(config.resource_dir), 
			config.src_dir,
			config.compile_dir
	)
	copy_tree(
			[f for f in list_files(module_src_path) if str(f).endswith('.java') == False], 
			config.src_dir,
			config.compile_dir
	)

	# jlink
	arg_file = path.join(config.local_cache_dir, 'jlink-args.txt')
	command_list = []
	command_list += ['--module-path', os.pathsep.join(module_paths + [config.compile_dir])]
	command_list += ['--add-modules', config.module_name]
	image_dir = path.join(config.deploy_image_dir, release_OS, config.module_name)
	command_list += ['--output', image_dir]
	with open(arg_file, 'w') as fout:
		file_content = ' '.join(map(safe_quote_string, command_list))
		fout.write(file_content)
		print('@%s: %s' % (arg_file, file_content))
	call([config.jlink_exec, '@'+str(arg_file)], cwd=config.root_dir)
	# launch scripts
	if release_OS == 'windows_x64':
		with open(path.join(image_dir, 'launch.bat'), 'w') as fout:
			fout.write('"%~dp0/bin/javaw.exe" -m '+config.module_name+'/'+config.main_class+'\r\n')
	if release_OS == 'linux_x64':
		with open(path.join(image_dir, 'launch.sh'), 'w') as fout:
			fout.write('#!/bin/bash\nTHIS_DIR="`dirname "$0"`"\n"${THIS_DIR}/bin/java" -m '+config.module_name+'/'+config.main_class+'\n')
	if release_OS == 'mac':
		with open(path.join(image_dir, 'launch.sh'), 'w') as fout:
			fout.write('#!/bin/bash\nTHIS_DIR="`dirname "$0"`"\n"${THIS_DIR}/bin/java" -m '+config.module_name+'/'+config.main_class+'\n')
	
