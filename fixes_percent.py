# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 13:14:12 2020

@author: Administrator
"""

import os
import re
from subprocess import Popen, PIPE
import unicodedata
import csv


filelist = []
path = "D:/linux-next"


for root, dirs, files in os.walk(path):
    for file in files:
        (filename, extension) = os.path.splitext(file)
        if extension == ".c":
            filelist.append(root.replace("D:/linux-next\\", "").replace('\\', '/') + '/' + file)


def gitFixCommits(kernelRange, repo, fileName):
    commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
    fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
    nr_fixes = 0
    total_commits = 0
    
    
    cmd = ["git", "log", "-p", "--no-merges", "--date-order", kernelRange, fileName]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
    #print(data)

    for line in data.split("\n"):
        
        if commit.match(line):
            total_commits += 1
        
        if fixes.match(line):
            nr_fixes += 1

    try:
        fixes_percent = (nr_fixes / total_commits) * 100
    except ZeroDivisionError:

        fixes_percent = 0
       
    print('fixes_percent:'+str(fixes_percent))
    return fixes_percent

if __name__ == '__main__':
    with open('data.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['fixes_percent','path']) 
        for j in range(len(filelist)):
            writer.writerow([str(gitFixCommits('v3.0..HEAD', 'D:/linux-next', filelist[j])),filelist[j]]) #同时写入多行信息
            print(filelist[j],'\n')
    print('ok!')
        