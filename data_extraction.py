#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get data for bug-fix distance analysis of linux kernel subsystems.
-------------------------------------------------------------------
Implement data-extraction classes:

FixDistanceExtractor: 
get bug-fix distance of subsystems in repo linux-next;

FeatureAddExtractor:
get the development speed of features;

BugDensityExtractor:
get the bug density of one file in the subsystem specified


"""
__author__ = "Group04"
__copyright__ = "Copyright 2020, Lanzhou University"
__credits__ = ["Group04"]
__license__ = "GPL V3"
__version__ = "1.0"
__maintainer__ = "Liu Yutian"
__email__ = "ytliu18@lzu.edu.cn"
__status__ = "Production"


import re
import unicodedata
from subprocess import Popen, PIPE


class FixDistanceExtractor:
    """
    Parameters:
    subsys: The subsystem at file level;
    range: The range of system version's sublevels, such as 'v4.9..v4.9.216'.
    """
    def __init__(self, subsys, range):
        self.subsys = subsys
        self.range = range

    def get_fix(self):
        """
        Returns the list of bug-fix commits.
        """
        fix_list = []
        cmt_list = []

        cmd = ["git", "log", "-P", "--no-merges", self.range, self.subsys]
        p = Popen(cmd, cwd=self.subsys, stdout=PIPE)
        data = p.communicate()[0]
        # Clean and normalize the data.
        data = unicodedata.normalize(u"NFKD", data.decode(encoding="utf-8", errors="ignore"))

        commit = re.compile("^commit [0-9a-z]{40}$", re.IGNORECASE)
        fix = re.compile("^\W+Fixes: [a-f0-9]{8,40} \(.*\)$", re.IGNORECASE)
        for line in data.split("\n"):
            if (commit.match(line)):
                cur_commit = line
            if (fix.match(line)):
                fix_list.append(cur_commit[7:19])
                cmt_list.append(line.strip()[7:30].split(" ")[0])

        return fix_list, cmt_list


class FeatureAddExtractor:
    """
    Parameters:
    subsys: The subsystem at file level;
    range: The range of system version's sublevels, such as 'v4.9..v4.9.216'.
    """
    def __init__(self, subsys, range):
        self.subsys = subsys
        self.range = range

    def get_feature(self):
        """
        Returns the list of commits that add new features.
        """
        cmt_list = []

        cmd = ["git", "log", "--oneline", self.range, self.subsys]
        p = Popen(cmd, cwd=self.subsys, stdout=PIPE)
        data = p.communicate()[0]
        # Clean and normalize the data.
        data = unicodedata.normalize(u"NFKD", data.decode(encoding="utf-8", errors="ignore"))

        for line in data.split("\n"):
            if (re.findall("feature", str(line))):
                cmt_list.append(line[0:11])

        return cmt_list

    def get_time(self, cmt_list):
        """
        Returns the list of difference of time between every features are added.
        """
        time_list = []
        diff_list = []

        for cmt in cmt_list:
            cmd = ["git", "log", "-1", '--pretty=format:\"%ct\"', cmt]
            p = Popen(cmd, cwd=self.subsys, stdout=PIPE)
            data = p.communicate()[0]
            data = unicodedata.normalize(u"NFKD", data.decode(encoding="utf-8", errors="ignore"))
            time_list.append(int(data.strip('"')))

        time_list.sort()
        if len(time_list) == 1:
            return None
        if len(time_list) == 2:
            diff_list.append(time_list[1] - time_list[0])
        else:
            for i in range(len(time_list) - 1):
                diff_list.append(time_list[i + 1] - time_list[i])

        return diff_list


class BugDensityExtractor:
    """
    Parameters:
    subsys: The subsystem at file level;
    range: The range of system version's sublevels, such as 'v4.9..v4.9.216'.
    """
    def __init__(self, subsys, range):
        self.subsys = subsys
        self.range = range

    def get_density(self, file_name):
        """
        Returns the ratio of number of commits with fix tag
        to the number of commits in total.
        """
        commits = re.compile("^commit [0-9a-z]{40}$", re.IGNORECASE)
        fixes = re.compile("^\W+Fixes: [a-f0-9]{8,40} \(.*\)$", re.IGNORECASE)
        nr_fixes = 0
        total_commits = 0

        cmd = ["git", "log", "-p", "--no-merges", "--date-order", self.range, file_name]
        p = Popen(cmd, cwd=self.subsys, stdout=PIPE)
        data = p.communicate()[0]
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))

        for line in data.split("\n"):
            if commits.match(line):
                total_commits += 1
            if fixes.match(line):
                nr_fixes += 1

        try:
            fixes_percent = (nr_fixes / total_commits) * 100
        except ZeroDivisionError:
            fixes_percent = 0

        return fixes_percent


if __name__ == "__main__":
    extractor = BugDensityExtractor("/home/ytliu/linux-next/fs", "v4.4")
    bug_density = extractor.get_density("/home/ytliu/linux-next/fs/afs/cache.c")
    print(bug_density)
