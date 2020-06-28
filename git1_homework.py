#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Group04"
__copyright__ = "Copyright 2020, Lanzhou University"
__credits__ = ["Group04"]
__license__ = "GPL V3"
__version__ = "1.0"
__maintainer__ = "Liu Yutian"
__email__ = "ytliu18@lzu.edu.cn"
__status__ = "Production"


import unicodedata
from subprocess import Popen, PIPE


def execute_gitcmd(kernelRange, path, filename):
    cmd = ["git", "log", "--stat", "--oneline", "--follow",kernelRange,filename]
    p = Popen(cmd, cwd=path, stdout=PIPE)
    data = p.communicate()[0]
    data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))

    return data


def write_txt(data):
    with open("result.txt", mode="w") as f:
        f.write(data)


if __name__ == "__main__":
    kernelRange = "v4.4..v4.5"
    path = "/home/ytliu/linux-stable"
    filename = "kernel/sched/core.c"
    data = execute_gitcmd(kernelRange, path, filename)
    write_txt(data)
