import data_extraction
import numpy as np


repo = "/home/ytliu/linux-next"
subsys = ["fs/afs/", "drivers/video/", "kernel/printk/", "net/nfc/", "tools/usb/"]
range = "v4.4"
file_static = {}
feature_static = {}


for sname in subsys:
    extractor = data_extraction.FeatureAddExtractor(repo, sname, range)
    cl = extractor.get_feature()
    dl = extractor.get_time(cl)
    feature_static[sname] = np.mean(dl)

    extractor = data_extraction.FileAddExtractor(repo + sname)
    fl = extractor.get_file()
    td = extractor.get_timediff(fl)
    file_static[sname] = np.mean(td)


print(feature_static)
print(file_static)
