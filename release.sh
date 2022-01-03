#!/bin/bash

name="keyswitch-kicad-library"
output_dir="release"
lib_files="library/footprints library/3dmodels"


# TODO write metadatas dynamically,
# (pack side and kicad repo side)
# rewrite in python

# make output dir
mkdir -p $output_dir/footprints $output_dir/3dmodels $output_dir/resources

# Generate icon
cairosvg --output-width 64 --output-height 64 assets/icon.svg -o ${output_dir}/resources/icon.png

# Copy metadata
cp metadata.json ${output_dir}/metadata.json

# Copy lib files
cp -r ${lib_files} ${output_dir}

# Pack
cd ${output_dir}
zip -r ./${name}.zip ./footprints ./3dmodels ./resources ./metadata.json

# Compute checksum
echo -n '"download_sha256": ' > ./${name}_info.txt
sha256sum ./${name}.zip | sed -E 's/\s(.*)//;t;d' >> ./${name}_info.txt

# Compute download size
echo -n '"download_size": ' >> ./${name}_info.txt
du -csb ./${name}.zip | grep total | sed 's/ *\stotal* *\(.*\)/\1/' >> ./${name}_info.txt

# Compute install size
echo -n '"install_size": ' >> ./${name}_info.txt
# du -csb ${lib_files} | grep total | sed 's/ *\stotal* *\(.*\)/\1/' >> ./${name}_info.txt

# Return to root
cd ..