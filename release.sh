#!/bin/bash

name="openinput-kicad-library"
lib_files="./footprints ./3dmodels ./resources ./metadata.json"

# TODO write metadatas dynamically,
# (pack side and kicad repo side)
# rewrite in python

# Pack
zip -r ./${name}.zip ${lib_files}

# Compute checksum
echo -n '"download_sha256": ' > ./${name}_info.txt
sha256sum ./${name}.zip | sed -E 's/\s(.*)//;t;d' >> ./${name}_info.txt

# Compute download size
echo -n '"download_size": ' >> ./${name}_info.txt
du -csb ./${name}.zip | grep total | sed 's/ *\stotal* *\(.*\)/\1/' >> ./${name}_info.txt

# Compute install size
echo -n '"install_size": ' >> ./${name}_info.txt
du -csb ${lib_files} | grep total | sed 's/ *\stotal* *\(.*\)/\1/' >> ./${name}_info.txt
