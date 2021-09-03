# shrink-zotero-library

## Introduction

`shrink-zotero-library` aims to decrease the total disk space used by a Zotero library by compressing the PDF attachments.
This is useful because the [storage plans provided by Zotero.org](https://www.zotero.org/storage?id=storage) are limited by disk space, rather than by the number of items.
The PDF version of articles provided by publishers are often poorly compressed and raster figures are generally optimised for print instead of for viewing with a screen.
This means that some simple compression can often reduce file sizes significantly, with little reduction in the quality of the PDF.

## Warning
THIS TOOL OVERWRITES YOUR PDFS, USE IT AT YOUR OWN RISK. The code is poorly written and tested, and could easily corrupt your Zotero library or worse. Backup everything first.

## How does it work?

PDF compression uses `ghostscript` with the following command, borrowed from [firstdoit](https://gist.github.com/firstdoit/6390547).

    ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf

Notice that there are some options to tweak (notably `-dPDFSETTINGS=/ebook`). Probably these will become command line flags in future versions.

## Requirements

You should have the following installed:
- Python 3
- [Ghostscript](https://www.ghostscript.com/), executable as `ghostscript`

Tested with Python 3.8.10 and Ghostscript 9.50 on Ubuntu 20.04.

## Usage

First steps
- Make `crawl.py` executable and copy it into your path
- Close any running instances of Zotero
- Make a backup of your Zotero library ([default locations](https://www.zotero.org/support/zotero_data))
- Change directory to the root folder of your Zotero library

By default `crawl.py` will do a dry run (will not write anything to disk), simply compressing each PDF one by one and reporting the possible disk space savings. Check the output to get an idea of how many PDFs will be compressed, and how much space this will save.

>```crawl.py```

The output will show the filename, the file size of the original PDF, the file size of the PDF if we compress it and the new file size as a percentage of the old one. By default, if the compressed file is 90% or less of the size of the original, the tool performs the compression:

    ./storage/IT84I2DP/Alsop-Marco-slope-Tectonophysics-2013.pdf    original: 10.0 MiB      3.0 MiB 34.4%   [would overwrite]
    ./storage/9WJ5TGG4/Cheraghi et al. - 2013 - Scaling behavior and the effects of heterogeneity .pdf      original: 6.0 MiB       5.0 MiB 83.6%   [would overwrite]
    ./storage/WXSIGYIZ/Micallef et al. - 2007 - Fractal statistics of the Storegga Slide.pdf        original: 1.0 MiB       0.0 MiB 41.1%   [would overwrite]
    ./storage/Y4AGT88D/Carpentier and Roy-Chowdhury - 2009 - Conservation of lateral stochastic structure of a .pdf original: 0.0 MiB       0.0 MiB 98.0%   [no action]
    ./storage/V2UCQIKX/Azevedo et al. - 2018 - Strike-slip deformation reflects complex partition.pdf       original: 3.0 MiB       1.0 MiB 35.6%   [would overwrite]

If you would like to overwrite the original files with the compressed files, run:

>```crawl.py --overwrite```

In `--overwrite` mode the tool leaves behind a hidden file called `.compressed` in each sub-directory, which prevents the tool from performing any analysis or compression again if the tool is run twice (for performance reasons, and in case you would like to re-run the tool in future).

The original files will be copied to a file called `infile__original__.pdf`.
If you are brave and would like to delete the originals, you could (very carefully) try running something like

>```find . -name '*__original__.pdf' -exec rm "{}" \;```

Finally, restart Zotero. You may need to reset the file sync history to persuade Zotero to re-sync the new PDFs (Edit->Preferences->Sync->Reset->Reset File Sync History, read carefully the [Sync Reset Options](https://www.zotero.org/support/kb/sync_reset_options) first).

## Performance

I was able to reduce the size of my Zotero library (729 items) from 2.8 GiB to 1.8 GiB, enough to allow me to sync new items.
    
