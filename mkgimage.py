#!/usr/bin/env python

import os
import sys

"""
Documentation (german):

https://de.wikipedia.org/wiki/GUID_Partition_Table

"""


from gpt_image.disk import Disk
from gpt_image.partition import Partition, PartitionType 


if __name__ == '__main__':
    # create a new, 16 MB disk, size is in bytes
    disk = Disk("disk-image.raw")
    disk.create(16 * 1024 * 1024)

    disk_part1 = Partition(
        "FDISK001",
        1024 * 1536,
        PartitionType.BASIC_DATA_PARTITION.value
    )
    disk.table.partitions.add(disk_part1)

    # commit the change to disk
    disk.commit()

    # dump the current GPT information:

    print(disk)
