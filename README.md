# Artifact Evaluation for Visualinux

## Overview

Visualinux is a debugging framework that can simplify the program state of Linux kernel to the extent that one can visually understand with low programming complexity and efforts.
This repo provides the source code of our prototype implementation.
We also provide an online environment to reproduce the evaluation results of our paper submission.

## Deployment

### Online Evaluation

We have provided an online server for online artifact evaluation:

```
IP:     47.100.130.248
user:   visualinux
passwd: eurosys@25
```

You can also deploy Visualinux on your own debugging environment.

### Requirements

Visualinux is fully compatible to gdb and it is available as long as one can debug the Linux kernel through gdb with python extension enabled.
The tool has been tested on Ubuntu 22.04 and Python 3.10.12, with both gdb (QEMU) and kgdb (rpi-400) targeting on Linux kernel 5.15 and 6.1.

### Fresh Build

This repo provides several scripts for a quick fresh build:

```
./scripts/initdev.sh
./scripts/get-busybox.sh
./scripts/get-kernel.sh default
cp ./scripts/kernel.config/linux-6.1.25.config ./kernel/.config
make build
```

These scripts are not necessary to use; you can prepare a debugging environment for Linux kernel by yourself, with the following requirements satisfied:

- Python 3.10+ with Python packages listed in `scripts/pu-requirements.txt` installed.

- Node.js 18.20+ with npm package requirements in `visualizer/` installed.

Make sure your gdb is able to auto-load gdb scripts and extensions (`scripts/config.gdb`, `visualinux-gdb.py` and `kernel/vmlinux-gdb.py`), e.g. check if they are in your gdb auto-load safe-path. Otherwise you have to manually load these scripts in each new debugging session.

Also note that the kernel should be compiled with debug info enabled, and compiled/runned with KASLR disabled.

## Run

### start a debug session

This repo provides vscode configuration files, so you can open the vscode workspace in `.vscode/visualinux.code-workspace` and launch a gdb-qemu debugging task directly.

Alternatively, you can start a pure gdb in shell command:

```
make start    # in terminal 1
make attach   # in terminal 2
```

### start the visualizer

In another terminal:

```
cd visualizer/
npm run dev
```

### try Visualinux

At any gdb breakpoint, you can execute the gdb command `vl-update <file>` (with a `-exec` prefix in vscode environment) to extract the kernel state view according to a specified DSL program `dsl/<file>.vl`. If `<file` is not provided, `dsl/default.vl` will be used.

The visualizer polls the latest extracted data and updates the displayed object graphs.

## Reproduce the Evaluation

If you use our init image and workload (see `workload/init.sh`), you can set a breakpoint on the syscall `getsid()` (at `kernel/sys.c:1168` in Linux 6.1.25) and run the executable file `/workload/test/summation`.
When the kernel execution first pauses, execute `vl-update evaluation` to reproduce the textbook evaluation results of our paper submission.

The first time of object graph extraction might be slow since gdb needs to cache several statical information in a cold start.

Note that the evaluation `dsl/textbook/14_kernfs.vl` requires a short hacking into Linux kernel source code. If you deployed the Visualinux by youself, You should manually patch the code in `scripts/kernel.patch/fs.kernfs.dir.c.patch` into the end of `kernel/fs/kernfs/dir.c`.
