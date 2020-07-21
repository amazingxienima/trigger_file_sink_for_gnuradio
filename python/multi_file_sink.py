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

class multi_file_sink(gr.sync_block):
    """
    docstring for block multi_file_sink
    """
    def __init__(self, filedir0,filedir1):
        gr.sync_block.__init__(self,
            name="multi_file_sink",
            in_sig=[ numpy.complex64, numpy.complex64 ],
            out_sig=None)
        self.fd0 = open( filedir0, "wb" )
        self.fd1 = open( filedir1, "wb" )

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]

        data0 = in0.tostring()
        self.fd0.write( data0 )

        data1 = in1.tostring()
        self.fd1.write( data1 )
        # <+signal processing here+>
        return len(input_items[0])

