#!/usr/bin/env bash

echo "DD test program"

# Spin up drive
echo "Spinning up drive"
dd if=/dev/sr0 of=/dev/null count=10 iflag=nocache oflag=nocache,dsync bs=1M 
sleep 5

# Alternate between long an short flashes 
echo "Begining test"
echo "Alternate long and short reads"
dd if=/dev/sr0 of=/dev/null count=5 iflag=nocache oflag=nocache,dsync bs=1M 
sleep 1
dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=5 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=5 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=5 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=5 iflag=nocache oflag=nocache,dsync bs=1M
sleep 1
dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M