# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 21:06:21 2022

@author: Matthew Gunther

This module is the GUI wrapper for SystemMapper and other Shardspace modules.
It is designed to provide the user-facing elements, presenting the inner
and outer system maps as well as menus to select a starting point and a
destination, then show the fastest trajectory.

This script is intended to be compiled by PyInstaller to create an .exe
"""

from tkinter import *
from tkinter import ttk

import SystemMapper