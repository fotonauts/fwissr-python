#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Pierre Baillet'
__email__ = 'pierre@baillet.name'
__version__ = '0.1.0'

import fwissr
import sys
sys.modules['Fwissr'] = fwissr.FwissrModule()
