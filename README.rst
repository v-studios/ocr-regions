==========================
 README Tesseract Regions
==========================

Python Libraries
================

tesserocr
---------

https://pypi.python.org/pypi/tesserocr

Gives access to "several" API calls, uses C++ bindings, threading. Useful call::

    def TesseractRect(self, imagedata,
                      int bytes_per_pixel, int bytes_per_line,
                      int left, int top, int width, int height):
        """Recognize a rectangle from an image and return the result as a string.

    def GetRegions(self):
        """Get the result of page layout analysis as a list of
        image, box bounds {x, y, width, height} tuples in reading order.

Looks promising.


pyocr
-----

https://github.com/openpaperwork/pyocr

Works with command via fork, or directly with Libtesseract.


pytesseract
-----------

https://github.com/madmaze/pytesseract

I can't tell what they are doing for 'boxes'::

  def run_tesseract(input_filename, output_filename_base, lang=None, boxes=False,
                    config=None, nice=0):
  if boxes:
      command += ('batch.nochop', 'makebox')

but I'm guessing it asks to *output* boxes rather than define a
region. It seems to output bboxes for every character it finds. Not
very useful for me.

What can we specify in a ``config``?::

  if config:
      command += shlex.split(config)


pyocr
-----

One reviewer liked this better than pytesseract. 

python-tesseract
----------------

Looks unmaintained since 2014, no README

https://bitbucket.org/3togo/python-tesseract/src/9ce0abe168297513d648406be5482b52d38d883b/src/?at=master

But this says it gives access to the API, which would be useful:

https://www.quora.com/How-do-I-use-PyTesser-and-Tesseract-OCR-in-Ubuntu-with-Python


UZN files
=========

"tesseract.exe pic1.bmp pic1.txt -psm 4" and put a pic1.uzn file in the current directory.

do pytesseract (boxes command?) or pyocr use uzn or bbox files?

tesseract.exe test.png test -psm 4"
with tesseract, test.png and test.uzn in the same directory will result in a test.txt with the content
This is another test

Content of test.uzn: What's the format??
100 130 200 30 Text

I tried to use the numbers from the parse hocr for field 4::

  {'4.': (485, 1107, 545, 1164),
   'Top': (571, 1107, 708, 1179),
   'Assy.': (730, 1107, 924, 1181),
   'Part': (950, 1107, 1097, 1167),
   'Number': (1121, 1109, 1406, 1169)}

tesseract GCAR1.tif --psm 4 GCAROUT with GCAR1.uzn::

  1121 1109 1406 1169 Text

But got::

    Number 5. Top
    38-301 Li-IO
    Asse
    dumber 8. Sub;
    10. Revision Summary: NM
    ation: N/A
    muel Russell

So I think my numbers for the uzn may be diff from the bbox?

With 7 (single line of text)::

  tesseract GCAR1.tif --psm 7 GCAR-psm7

I get::

  muel Russell

Samuel Russel is way below "4. Top assy. Part Number". 

https://github.com/OpenGreekAndLatin/greek-dev/wiki/uzn-format
says the format is::

  left top width height freetext

So I'm gussing the HOCR bbox is xmin ymin xmax ymax.
So if I convert...::

  1121 1109 1406-1121=339 1169-1109=60

or::

  1121 1109 339 60 sometext

and run::

  tesseract GCAR1.tif --psm 7 GCAR-uznfixed-psm7

we get what we exptected::

  Number

Merge our bounding box to include all the field 4. Take min and max x,
y of all fields in the HOCR bbox::

  {'4.': (485, 1107, 545, 1164),
   'Top': (571, 1107, 708, 1179),
   'Assy.': (730, 1107, 924, 1181),
   'Part': (950, 1107, 1097, 1167),
   'Number': (1121, 1109, 1406, 1169)}

So bbox::

  485 1107 1406 1181

Convert to uzn::

  485 1107 921 74 field "4. Top Assy. Part Number"

and we get what we expect::

  4. Top Assy. Part Number

Is there a way we can use Tesseract's own "image segmentation" to get
locations of (say) outlined field boxes and such so we don't have to
guess this stuff?

