import os,re,subprocess

a = "/Users/dell/Documents/GitHub/linux-stable"#The address of the linux-stable.

def get_subsystem(address):
    file_name = os.listdir(address)#Find all the files in the linux-stable, both files and folders.
    names = [name for name in file_name if os.path.isfile(os.path.join(address,name))]#Find all the files.

    subsystem = []#Find all the folders, no files. These are the subsystems that we need.
    for j in file_name:
        if j not in names:
            subsystem.append(j)
    return subsystem

def get_feature_num(git_cmd):#Find all the branches in the log that add features.
   cnt = 0
   counts = git_cmd.communicate()[0]
   cnt = re.findall('feature', str(counts))#Using regular expression to find "features".
   return len(cnt)

if __name__ == "__main__":
    n = get_subsystem(a)
    for m in n:
        git_address = "git log --oneline " + m + "/"
        git_commit = subprocess.Popen(git_address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        num = get_feature_num(git_commit)
        print(m,"feature number:",num)