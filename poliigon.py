import os
import json

poliigon = "D:/CG/Library/materials/poliigon"
infos_fp = "C:/users/edward/Desktop/poliigon_infos.json"
types_fp = "C:/users/edward/Desktop/poliigon_types.json"
types_exclusive_fp = "C:/Users/edward/Desktop/poliigon_types_exclusive.json"

infos = []
types = []

for root, directory, files in os.walk(poliigon):
    dir = root[len(poliigon)+1:].replace("\\", "/")
    if files:
        for file in files:
            f = file
            ext = f.split(".")[-1]
            f = f.replace("."+ext, "")
            f = f.split("_")
            f.pop(0)
            res = f[-1]
            f.pop(-1)
            type = ""
            for word in f:
                type += word +"_"
            type = type[0:-1]
            # if type in ("VAR1", "VAR2", "VAR3", "VAR4", "VAR5"):
            #     __fp_src = os.path.join(poliigon, dir, file)
            #     a = file.split("_")[0]
            #     b = file.split("_")[1]
            #     c = file.split("_")[2]
            #     __fp_dst = a + "_COL_"+b+"_"+c
            #     __fp_dst = os.path.join(poliigon, dir, __fp_dst)
            #     os.rename(__fp_src, __fp_dst)
#             info = {
#                 "type": type,
#                 "resolution": res,
#                 "extension": ext,
#                 "directory": dir,
#             }
#
#             infos.append(info)
#             types.append(type)
#
# jsoninfos = open(infos_fp, "w")
# json.dump(infos, jsoninfos, indent=4)
# jsoninfos.close()
#
# jsontypes = open(types_fp, "w")
# json.dump(types, jsontypes, indent=4)
# jsontypes.close()
#
# all_types = json.load(open(types_fp, "r"))
#
# types = []
# for type in all_types:
#     if type not in types: types.append(type)
#
# types = sorted(types)
# json.dump(types, open(types_exclusive_fp, "w"), indent=4)

#['6K', '3K', 'HIRES', '4K', '1K']