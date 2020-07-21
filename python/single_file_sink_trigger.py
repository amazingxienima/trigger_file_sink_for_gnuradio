#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 gnuradio.org.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class single_file_sink_trigger(gr.sync_block):
    """
    docstring for block single_file_sink_trigger
    """
    def __init__(self, filedir,trigger,threshold):
        gr.sync_block.__init__(self,
            name="single_file_sink_trigger",
            in_sig=[ numpy.complex64 ],
            out_sig=None)
        self.fd0 = open( filedir, "wb" )
        self.threshold = threshold
        self.trigger = trigger
        self.unpass_counter = 0

    def if_input_items_pass( self, input_items ):
        if input_items.max() > self.trigger:
            self.unpass_counter = 0
            return True           
        self.unpass_counter += 1
        if self.unpass_counter <= self.threshold:
            return True
        return False

    def work(self, input_items, output_items):
        in0 = input_items[0]
        if self.if_input_items_pass( in0 ):
            data0 = in0.tostring()
            self.fd0.write( data0 )
        return len(input_items[0])

