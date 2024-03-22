#!/usr/bin/env python

"""
written by: Oliver Cordes 2024-03-22
changed by: Oliver Cordes 2024-03-22

mkgimage.py - create a disk image with FAT12 partitions

"""

import os
import sys
import math

"""
Documentation (german):

https://de.wikipedia.org/wiki/GUID_Partition_Table

"""


from gpt_image.disk import Disk
from gpt_image.partition import Partition, PartitionType 

from pyfat12 import FloppyImage, FAT12

import argparse

__version__ = '0.99.0'


def prepare_floppy_partition(nr, disk):
    start = (1536*2)*nr # 1.5 MB
    size = 1536 # kb
    label = f'FDISK{nr:03d}'
    disk_part = Partition(
        label,
        1024 * size,
        PartitionType.BASIC_DATA_PARTITION.value,
        first_lba = start,
        last_lba = start + (size * 2) - 1
        )
    disk.table.partitions.add(disk_part)

    # write the partition content to disk
    floppy = FloppyImage()
    fs = FAT12.format(floppy, label)
    disk_part.write_data(disk, floppy.get_data())

    return disk_part


def prepare_disk(filename, number_of_partitions):
    # create a new, 16 MB disk, size is in bytes
    disk = Disk(filename, overwrite=True)

    # calculate the size of the disk image
    # roughly take 1.5MB per disk and then round up to the next power of 2
    # take one additional partition in the beginning for the GPT
    min_size_mb = (number_of_partitions+1) * 1536 / 1024
    size_mb = 2**(int(math.log2(min_size_mb))+1)
    disk.create(size_mb * 1024 * 1024)

    print(f'Create disk image: "{filename}" ({size_mb}MB) with {number_of_partitions} partitions:')
    # create a new partition
    for nr in range(1, number_of_partitions+1):
        part = prepare_floppy_partition(nr, disk)
        print(f'{nr}',end=' ') 
    print()
    print('Done.')    

    # commit the change to disk
    disk.commit()

    # dump the current GPT information:
    #print(disk)

    return disk


if __name__ == '__main__':

    # parse the command line arguments

    parser = argparse.ArgumentParser(description='Create a disk image with FAT12 partitions.', 
                                    epilog=f'Version: {__version__} (C) 2024 Oliver Cordes')
    parser.add_argument('filename', help='the name of the disk image file') 
    parser.add_argument('number_of_partitions', type=int, help='the number of partitions to create')

    args = parser.parse_args()

    prepare_disk(args.filename, args.number_of_partitions)

    sys.exit(0)