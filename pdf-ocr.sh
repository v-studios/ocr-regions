#!/bin/sh
# Convert pdf to tiff and clean up, then ocr
file_pdf="$1"
file_nosuffix="${file_pdf%\.*}"
file_tif="${file_nosuffix}.tif"
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=tiffgray -r720x720 -sCompression=lzw -sOutputFile=${file_tif} ${file_pdf}
#         source        output_base        output_types_suffixes
tesseract "${file_tif}" "${file_nosuffix}" txt pdf hocr
