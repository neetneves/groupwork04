"""
Get data for bug-fix distance analysis of linux kernel subsystems.
-------------------------------------------------------------------
Implement data-extraction classes:

FixDistanceExtractor: 
get bug-fix distance of subsystems in repo linux-next;

"""
__author__ = "Liu Yutian"
__copyright__ = "Copyright 2020, Lanzhou University"
__credits__ = ["Group04"]
__license__ = "MIT"
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

        cmd = ["git", "log", "-P", "--no-merges", self.range]
        p = Popen(cmd, cwd=self.subsys, stdout=PIPE)
        data, res = p.communicate()
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


if __name__ == "__main__":
    extractor = FixDistanceExtractor("/root/linux-next", "v4.4")
    fl, cl = extractor.get_fix()
    print(len(fl))
    print(len(cl))
