# Artifact Evaluation for Visualinux

## Overview

Visualinux is a debugging framework that can simplify the program state of Linux kernel to the extent that one can visually understand with low programming complexity and efforts.
This repo provides the source code of our prototype implementation.
We also provide an online environment to reproduce the evaluation results of our paper submission.

![fig-01](https://github.com/hyperspark9/visualinux/blob/master/docs/readme-images/01-process_tree.png){ width=50% }

![fig-02](https://github.com/hyperspark9/visualinux/blob/master/docs/readme-images/01-process_tree.png){ width=50% }

## Deployment

### Online Evaluation

We have prepared an online site for a quick experience of Visualinux. You can painlessly enter a Linux kernel gdb debugging environment and check out the effect of our visualized debugger. Note that the online site only allows one connection at a time.

```
http://47.100.130.248
```

*Double-blind review: We guarantee that there is no logging activity in the online site and we do not track any visitor's IP address. You can also use a proxy to further hide your identity.*

You can deploy Visualinux in your own debugging environment. Check the following subsections for details.

### Requirements

Visualinux is fully compatible to gdb and it is available as long as one can debug the Linux kernel through gdb with python extension enabled.
The tool has been well-tested on Ubuntu 22.04 and Python 3.10.12, with both gdb (QEMU) and kgdb (rpi-400) targeting on Linux kernel 5.15 and 6.1.

### Fresh Build

This repo provides several scripts for a quick fresh build:

```
./scripts/initdev.sh
./scripts/get-busybox.sh
./scripts/get-kernel.sh default
cp ./scripts/kernel.config/linux-6.1.25.config ./kernel/.config
make build
```

These scripts are not mandatory to use; you can prepare a Linux kernel debugging environment on your own and meet the following requirements:

- An available gdb debugging environment for Linux kernel (e.g. the kernel should be compiled with debug info and booted with KASLR=off, etc.).

- Gdb with python extension enabled (which is the default configuration of gdb).

- Python 3.10+ with Python packages listed in `scripts/pu-requirements.txt` installed.

- Node.js 18.20+ with npm package requirements in `visualizer/` installed.

Moreover, please make sure your gdb is able to auto-load gdb scripts and extensions (`scripts/config.gdb`, `visualinux-gdb.py` and `kernel/vmlinux-gdb.py`), e.g. check if they are in your gdb auto-load safe-path. Otherwise you have to manually load these scripts in each new debugging session.

Also note that the kernel should be compiled with debug info enabled, and compiled/runned with KASLR disabled.

## Run

### Start a Debug Session

This repo provides vscode configuration files, so you can open the vscode workspace in `.vscode/visualinux.code-workspace` and launch a gdb-qemu debugging task directly.

Alternatively, you can start a pure gdb in shell command:

```
make start    # in terminal 1
make attach   # in terminal 2
```

### Start the Visualizer

In another terminal:

```
cd visualizer/
npm run dev
```

### try Visualinux

At any gdb breakpoint, you can execute the gdb command `vl-update <file>` (with a `-exec` prefix in vscode environment) to extract the kernel state view according to a specified DSL program `dsl/<file>.vl`. If `<file` is not provided, `dsl/default.vl` will be used.

The visualizer polls the latest extracted data and updates the displayed object graphs.

## Reproduce the Evaluation

If you use our init image and workload (see `workload/init.sh`), you can set a breakpoint on the function `security_task_getsid` and run the executable file `/workload/test/summation`.
When the kernel execution first pauses, execute `vl-update evaluation` to reproduce the textbook evaluation results of our paper submission.

The first time of object graph extraction might be slow since gdb needs to cache several statical information in a cold start.

*Note that the evaluation `dsl/textbook/14_kernfs.vl` requires a short hacking into Linux kernel source code. If you deployed the Visualinux by youself, You should manually patch the code in `scripts/kernel.patch/fs.kernfs.dir.c.patch` into the end of `kernel/fs/kernfs/dir.c`.*
