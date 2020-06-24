import re
import unicodedata
from subprocess import Popen, PIPE


commit = re.compile("^commit [0-9a-z]{40}$", re.IGNORECASE)
func_history = ["git", "log", "-L:"+"\\b"+"static int ocfs2_do_flock"+":"+"fs/ocfs2/locks.c", "--", "fs/ocfs2/locks.c"]
p2 = Popen(func_history, cwd="/home/ytliu/linux-next/", stdout=PIPE)
data2 = p2.communicate()[0]
data2 = unicodedata.normalize(u"NFKD", data2.decode(encoding="utf-8", errors="ignore"))

for line in data2.split("\n"):
    if commit.match(line):
        print(line)

