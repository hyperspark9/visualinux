# Artifact Evaluation for Visualinux

## Overview

Visualinux is a debugging framework that can simplify the program state of Linux kernel to the extent that one can visually understand with low programming complexity and efforts.
This repo provides the source code of our prototype implementation.
We also provide an online environment to reproduce the evaluation results of our paper submission (the online site will come soon).

## Requirements

Visualinux is fully compatible to gdb and it is available as long as one can debug the Linux kernel through gdb with python extension enabled.
The tool has been tested on Ubuntu 22.04 and Python 3.10.12, with both gdb-qemu and kgdb targeting on Linux kernel 5.15 and 6.1.

## Fresh Build

This repo provides several scripts for a quick fresh build:

```
./scripts/initdev.sh
./scripts/get-kernel.sh default
cp ./scripts/kernel.config/linux-6.1.25.config ./kernel/.config
./scripts/get-busybox.sh
make build
```

Or you can config a debugging environment for Linux kernel by yourself, with the following installation:

- Python 3.10+ with Python packages listed in `scripts/pu-requirements` installed.

- Node.js 18.20+ with `npm install` executed in `visualizer/`.

## Run

### start a debug session

This repo provides vscode configuration files, so you can open the vscode workspace in `.vscode/visualinux.code-workspace` and launch a gdb-qemu debugging task directly.

Also, you can start a pure gdb in shell command:

```
make start    # in terminal 1
make attach   # in terminal 2
```

### start the visualizer server

In another terminal:

```
cd visualizer
npm run dev
```

### try Visualinux

At any gdb breakpoint, you can execute the gdb command `vl-update <file>` (with a `-exec` prefix in vscode environment) to extract the kernel state view according to a specified DSL program `dsl/<file>.vl`. If `<file` is not provided, `dsl/default.vl` will be used.

## Reproduce the Evaluation

If you use our init image and workload (see `workload/init.sh`), you can set a breakpoint on the syscall `getsid()` and run the executable file `/workload/test/summation`.
When the kernel execution first pauses, execute `vl-update evaluation` to reproduce the evaluation results of our paper submission.

Note that the evaluation `dsl/textbook/14_kernfs.vl` requires a short hacking into Linux kernel source code. You should patch the code in `scripts/kernel.patch/fs.kernfs.dir.c.patch` into the end of `kernel/fs/kernfs/dir.c`.
