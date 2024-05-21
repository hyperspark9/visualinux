#!/bin/bash

dir_scripts=$(cd $(dirname $0); pwd)
dir_project=$(dirname $dir_scripts)
dir_workload=$dir_project/workload
dir_busybox=$dir_workload/busybox

version="1.36.1"

# get busybox tarball

wget -P $dir_workload https://busybox.net/downloads/busybox-$version.tar.bz2

# cleanup

rm -rf $dir_workload/busybox-$version
rm -rf $dir_kernel

# setup

echo "decompressing tarball..."
tar -xf $dir_workload/busybox-$version.tar.bz2 -C $dir_workload
rm $dir_workload/busybox-$version.tar.bz2

mv $dir_workload/busybox-$version $dir_busybox
cp $dir_workload/scripts/busybox.config $dir_busybox/.config
