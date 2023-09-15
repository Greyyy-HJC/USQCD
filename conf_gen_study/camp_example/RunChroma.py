#!/bin/env python
# encoding: utf-8
import numpy as np
import xml.etree.ElementTree as ET
import os
import sys


def updataMacros(inputfile, outputfile,  Macros):
    with open(inputfile,'r') as fin:
        lines = fin.readlines()
        for i in range(len(lines)):
            for key, value in Macros.items():
                if key in lines[i]:
                    lines[i] = lines[i].replace(key, value)
    with open(outputfile, 'w') as fout:
        fout.writelines(lines)




#   初始参数
if len(sys.argv) >=1:
    conf_st,conf_ed,conf_int = eval(sys.argv[1]),eval(sys.argv[2]),eval(sys.argv[3])
else:
    conf_st,conf_ed,conf_int = 1000,2000,10
# conf_st,conf_ed,conf_int=eval(input("Please input conf_list: start end interval ...\n"))
#conf_ed = conf_ed + 1
#   产生不同组态的输入文件
# no smearing
SampleFileName = "./purgaug.ini.xml"

#输入输出文件名
OutputPath="./purgauge_wilson_2432_beta6/"
chroma_path="/home/guilongcheng/chroma/chroma_qdpxx_quda/install/chroma_qdpxx-double/bin/"
chroma_path=""
chroma_path="/beegfs/home/sunp/chroma-llvm-gcc5.5-cuda10.1/install/sm_70_omp/chroma-double/bin/"

os.system("mkdir -p %sinput"%OutputPath)
os.system("mkdir -p %soutput"%OutputPath)
os.system("mkdir -p %slog"%OutputPath)

# 进行宏替换
Macros = {"MacroMass":"-0.01"}
Macros = {"MacroMass":"-0.0191"}
Macros = {"Macros_SavePrefix":"%s"%(OutputPath+"/conf/"),"Macros_nrow":"24 24 24 32"}


UpDataSampleFile = "purgauge"
InputFileName = [OutputPath+"input/conf%05i.%s.ini.xml"%(i,UpDataSampleFile) for i in range(conf_st,conf_ed,conf_int)]
OutputFileName = [OutputPath+"output/conf%05i.%s.output.xml"%(i,UpDataSampleFile) for i in range(conf_st,conf_ed,conf_int)]
LogFileName = [OutputPath+"log/conf%05i.%s.log"%(i,UpDataSampleFile) for i in range(conf_st,conf_ed,conf_int)]

UpDataSampleFile = OutputPath + UpDataSampleFile + ".ini.xml"
updataMacros(SampleFileName,UpDataSampleFile, Macros)
jconf=0
for iconf in range(conf_st,conf_ed,conf_int):
    Macros = {"MacroConf":str(iconf)}
    updataMacros(UpDataSampleFile,InputFileName[jconf], Macros)
    jconf=jconf+1
#  调用chroma进行计算
jconf = 0
for iconf in range(conf_st,conf_ed,conf_int):
    #读入模版文件
#    os.system("rungpu %spurgaug -geom 1 1 1 4 -i %s -o %s > %s "%(chroma_path,InputFileName[jconf],OutputFileName[jconf],LogFileName[jconf]))
#    os.system("mpirun -np 4 %spurgaug -envvar OMPI_COMM_WORLD_LOCAL_RANK -geom 1 1 1 4 -i %s -o %s > %s "%(chroma_path,InputFileName[jconf],OutputFileName[jconf],LogFileName[jconf]))
    os.system("%spurgaug  -geom 1 1 1 1 -i %s -o %s > %s "%(chroma_path,InputFileName[jconf],OutputFileName[jconf],LogFileName[jconf]))
    # os.system("mpirun -np 4 chroma -envvar OMPI_COMM_WORLD_LOCAL_RANK -geom 1 1 1 4 -i %s -o %s > %s "%(InputFileName[jconf],OutputFileName[jconf],LogFileName[jconf]))
    print("conf %i done!"%iconf)
    jconf=jconf+1

print("All Done")

