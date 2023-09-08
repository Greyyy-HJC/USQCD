#!/bin/bash

# folder name
ini_folder=ini_xml
out_folder=out_xml
output_folder=output_file

folders=(${ini_folder} ${out_folder} ${output_folder})

# create the folders if not exist
for folder in "${folders[@]}"; do
    if [ ! -d "./${folder}/" ]; then
        mkdir "${folder}"
    else
        echo "Folder ${folder} already exists"
    fi
done


# generate the ini.xml files
for conf_num in {779..1024}
do
    ini_xml=pure_gauge_meson_2pt_cfg${conf_num}.ini.xml
    ./pure_gauge_meson_2pt.pl ${conf_num} > ${ini_folder}/${ini_xml}
done


# run the Chroma program
for conf_num in {779..1024}
do
    ini_xml=pure_gauge_meson_2pt_cfg${conf_num}.ini.xml
    out_xml=pure_gauge_meson_2pt_cfg${conf_num}.out.xml
    output_txt=output_cfg${conf_num}.txt

    ./chroma_double -i ${ini_folder}/${ini_xml} -o ${out_folder}/${out_xml} > ${output_folder}/${output_txt}
done