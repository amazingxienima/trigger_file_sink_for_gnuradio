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

    def __init__(self, filedir0, filedir1, trigger, threshold, reserved_points ):
        gr.sync_block.__init__(self,
            name="multi_file_sink_trigger",
            in_sig=[ numpy.complex64, numpy.complex64 ],
            out_sig=None)
        if trigger < 0 or threshold < 0 or reserved_points <= 0:
            raise Exception("[multi_file_sink_trigger]:illegal input")
        self.fd0 = open( filedir0, "wb" )
        self.fd1 = open( filedir1, "wb" )
        self.threshold = threshold
        self.trigger = trigger
        self.keywords=numpy.array( [10,10,-10,10], dtype = numpy.complex64 )
        self.reserved_points = reserved_points
        self.unpass_counter = 0
        self.last_drop_items0 = numpy.array( [], dtype = numpy.complex64 )
        self.last_drop_items1 = numpy.array( [], dtype = numpy.complex64 )
        self.drop_num = numpy.array( [0], dtype = numpy.complex64 )

    def if_input_items_pass( self, input_items1, data_lenth ):
        if input_items1.max() > self.trigger:
            self.unpass_counter = 0
            return True
        if self.unpass_counter == 0 and data_lenth < 100:
            print( input_items1.size ) 
            return True
        self.unpass_counter += 1
        if self.unpass_counter < self.threshold:
            return True
        return False
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        if self.unpass_counter == 0:
            writd_idx = self.if_input_items_pass( numpy.concatenate( (in0[-5:], in1[-5:]) ), in0.size)
        else:
            writd_idx = self.if_input_items_pass( numpy.concatenate( ( in0[0:-1:500],in0[1:-1:500],in0[2:-1:500],in0[3:-1:500],in0[4:-1:500],in1[-10:],in1[0:-1:500],in1[1:-1:500],in1[2:-1:500],in1[3:-1:500],in1[4:-1:500] , in1[-10:]) ) ,in0.size)
        if writd_idx:
            if self.last_drop_items0.size != 0:
                in0 = numpy.concatenate(( self.keywords , self.drop_num , self.last_drop_items0, in0))
                in1 = numpy.concatenate(( self.keywords , self.drop_num , self.last_drop_items1, in1))
                self.last_drop_items0 = numpy.array( [], dtype = numpy.complex64 ) 
                self.last_drop_items1 = numpy.array( [], dtype = numpy.complex64 ) 
                self.drop_num[0]=0
            s_data0 = in0.tostring()
            self.fd0.write( s_data0 )
            s_data1 = in1.tostring()
            self.fd1.write( s_data1 )
        else:
            self.last_drop_items0 = numpy.concatenate( ( self.last_drop_items0, in0 ) )
            self.last_drop_items1 = numpy.concatenate( ( self.last_drop_items1, in1 ) )
            dr0 = self.last_drop_items0.size
            cut_index = -1 * min( self.reserved_points, self.last_drop_items0.size )
            self.last_drop_items0 = self.last_drop_items0[ cut_index: ]
            self.last_drop_items1 = self.last_drop_items1[ cut_index: ]
            dr1 = self.last_drop_items0.size 
            self.drop_num[0] = self.drop_num[0] + dr0 - dr1 
        return len(input_items[0])