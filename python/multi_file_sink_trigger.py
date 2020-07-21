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

class multi_file_sink_trigger(gr.sync_block):
    """
    docstring for block multi_file_sink_trigger
    """
    def __init__(self, filedir0,filedir1,trigger,threshold):
        gr.sync_block.__init__(self,
            name="multi_file_sink_trigger",
            in_sig=[ numpy.complex64, numpy.complex64 ],
            out_sig=None)
        self.fd0 = open( filedir0, "wb" )
        self.fd1 = open( filedir1, "wb" )
        self.threshold = threshold
        self.trigger = trigger
        self.unpass_counter = 0
        self.last_drop_items0 = numpy.array( [], dtype = numpy.complex64 )
        self.last_drop_items1 = numpy.array( [], dtype = numpy.complex64 )

    def if_input_items_pass( self, input_items1, input_items2 ):
        if input_items1.max() > self.trigger or input_items2.max() > self.trigger:
            self.unpass_counter = 0
            return True
        self.unpass_counter += 1
        if self.unpass_counter <= self.threshold:
            return True
        return False

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        if self.if_input_items_pass( in0, in1 ):
            data0 = numpy.concatenate( ( self.last_drop_items0, in0 ) )
            data1 = numpy.concatenate( ( self.last_drop_items1, in1 ) )
            s_data0 = data0.tostring()
            self.fd0.write( s_data0 )
            s_data1 = data1.tostring()
            self.fd1.write( s_data1 )
            self.last_drop_items0 = numpy.array( [], dtype = numpy.complex64 )
            self.last_drop_items1 = numpy.array( [], dtype = numpy.complex64 )
        else:
            self.last_drop_items0 = in0.copy()
            self.last_drop_items1 = in1.copy()
        
        return len(input_items[0])

