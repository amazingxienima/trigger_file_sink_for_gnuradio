# File Sink Blocks for gnuradio

include:  single_file_sink, single_file_sink_trigger, multi_file_sink, multi_file_sink_trigger.

## Installation

```shell
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
$ sudo ldconfig
```

## Uninstallation

```shell
$ rm -rf build ##if exists
$ mkdir build
$ cd build
$ sudo make uninstall
$ sudo ldconfig
```

## Verson
v 1.0(2020/7/21) first release
v 1.1(2020/7/21) multi_file_sink_trigger save the last "reserved points"

