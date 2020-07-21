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

class single_file_sink(gr.sync_block):
    """
    docstring for block single_file_sink
    """
    def __init__(self, filedir):
        gr.sync_block.__init__(self,
            name="single_file_sink",
            in_sig=[ numpy.complex64 ],
            out_sig=None)
        self.fd = open( filedir, "wb")

    def work(self, input_items, output_items):
        in0 = input_items[0]
        data = in0.tostring()
        self.fd.write( data )
        return len(input_items[0])

