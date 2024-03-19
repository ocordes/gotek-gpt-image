# gotek-gpt-image
Gotek floppy emulator gpt image creation


Disk is formatted as a linear sequence
of raw data disks every 1572864 bytes 
(1536kB)! So the idea is to create
a GPT with 128 entries to address all
these raw disks as partitions. This
may destroy the first image, but ... ;-)
