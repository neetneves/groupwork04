import re,os
import unicodedata
from subprocess import Popen,PIPE


class FileAddExtractor:
    def __init__(self,subsys):
        self.subsys = subsys


    def get_file(self):
        file_list = []
        for root,dirs,files in os.walk(self.subsys):
            for f in files:
                file_list.append(os.path.join(self.subsys,f))
        return file_list

    def get_timediff(self):

        time_list = []
        time_diff = []

        for file_path in file_list:
            cmd = ["git","log" ,"--follow" ,'--pretty=format:\"%ct\"' ,"--reverse",file_path]
            p = Popen(cmd,cwd=self.subsys,stdout=PIPE)
            data = p.communicate()[0]
            data = unicodedata.normalize(u'NFKD',data.decode(encoding="utf-8",errors="ignore"))
            data = re.split(r'\"(.*)\"\s+',data)
            time_list.append(int(data[1]))
     
        time_list.sort()
        if len(time_list) == 1:
            return None
        if len(time_list) == 2:
            time_diff.append(time_list[1] - time_list[0])
        else:
            for i in range(len(time_list) - 1):
                time_diff.append(time_list[i + 1] - time_list[i])

        return time_diff


if __name__ == "__main__":
    extractor = FileAddExtractor("/home/wyc/project/linux-next/fs/adfs")
    file_list = extractor.get_file()
    #print(file_list)
    timediff = extractor.get_timediff()
    print(timediff)                                       