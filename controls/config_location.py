#!/usr/bin/env python
## -*- coding: utf-8 -*-
## $Id$
## MODULE

"""
:cfg: -type: SafeConfigParser
:name: -type: str | "default"
"""

import sys
import os
import logging
log = logging.getLogger(__name__)
import configparser as cp
import xdg.BaseDirectory as bd

def cfg_filename(name):
	"""
	"""
	prg_name = os.path.basename(os.path.splitext(sys.argv[0])[0])
	name = name + os.extsep + "cfg"
	cfg_file = os.path.join(bd.xdg_config_home,prg_name,name)
	return cfg_file

def cfg_write(cfg,name = "default"):
	"""
	"""
	cfg_file = cfg_filename(name)
	log.info("writing configuration file %s" % cfg_file)
	if not os.path.exists(os.path.dirname(cfg_file)):
		os.makedirs(os.path.dirname(cfg_file),0o0700)
	fo = open(cfg_file,"w")
	cfg.write(fo)
	fo.close()
	
def cfg_read(cfg,name = "default"):
	"""
	"""
	cfg_file = cfg_filename(name)
	log.info("reading configuration file %s" % cfg_file)
	cfg.read(cfg_file)

def cfg_dict_write(cfg_dict,name = "default"):
	cfg = cp.SafeConfigParser()
	for sect_name,opt_dict in cfg_dict.items():
		cfg.add_section(sect_name)
		for opt_name,opt_value in opt_dict.items():
			cfg.set(sect_name,opt_name,str(opt_value))	
	cfg_write(cfg,name)

def cfg_dict_read(name = "default"):
	cfg_dict = dict()
	cfg = cp.SafeConfigParser()
	cfg_read(cfg,name)
	for sect_name in cfg.sections():
		cfg_dict[sect_name] = dict()
		for opt_name,opt_value in cfg.items(sect_name):
			cfg_dict[sect_name][opt_name] = opt_value
	return cfg_dict


  