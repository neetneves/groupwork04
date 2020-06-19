import os, re, subprocess, csv

a = "/Users/dell/Documents/GitHub/linux-stable"  # The address of the linux-stable.


def get_subsystem(address):
    """For get the files and folders in the linux-stable and write it into file_name."""
    file_name = os.listdir(address)
    names = [name for name in file_name if os.path.isfile(os.path.join(address,name))]  # To get files.

    subsystem = []  # To get the folders and locate the subsystems.
    for j in file_name:
        if j not in names:
            subsystem.append(j)
    return subsystem


def get_feature_num(git_cmd):
    """The purpose of function is to find branches in the log of linux-stable which have some specfic
    features.
    """
    cnt = 0
    counts = git_cmd.communicate()[0]
    cnt = re.findall('feature', str(counts))  # By using regular expression to define "features".
    return len(cnt)


if __name__ == "__main__":
    n = get_subsystem(a)  # The data
    csvFile = open("C://Users//donsherk//Desktop//test.csv", 'w', encoding='utf-8',newline='')
    # Create a csvFile for saving data
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('row 1', 'row 2', 'row 3'))
        for m in n:
            git_address = "git log --oneline " + m + "/"
            git_commit = subprocess.Popen(git_address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            num = get_feature_num(git_commit)
            writer.writerow(m, "feature number:", num)
    finally:
        csvFile.close()

