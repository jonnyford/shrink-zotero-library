#!/usr/bin/env python3

import os
import sys
import glob
import subprocess
import math
import argparse

path = './storage'
targets = []

qualities = ['screen',
             'ebook',
             'printer',
             'prepress',
             'default']

quality = qualities[1]


compression_cmd = ['ghostscript', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dNOPAUSE', '-dQUIET', '-dBATCH', f'-dPDFSETTINGS=/{quality}', '-sOutputFile=-']

minimum_shrink_factor = 0.9 # Only overwrite the original file if compression shrinks the filesize by this factor or greater

def main(args):
    for filename in glob.glob(os.path.join(path, '*',  '*.pdf')):
        if '__original__' in filename:
            continue
        else:
            targets.append(filename)

    for filename in targets:
        dirname = os.path.dirname(filename)
        already_compressed_file = os.path.join(dirname, '.compressed')
        
        try:
            in_size = os.stat(filename).st_size
        except FileNotFoundError:
            raise Exception(f'Input file has disappeared: {filename}')
        
        status = ''

        if os.path.exists(already_compressed_file):
            out_size = float('NaN')
        else:
            cmd = compression_cmd + [filename]
            ghostscript = subprocess.run(cmd, capture_output=True)
            if ghostscript.returncode != 0:
                print(f'Error with ghostscript, skipping this file: {ghostscript.stderr}')
                continue
            
            out_size = sys.getsizeof(ghostscript.stdout)
        
        shrink_factor = out_size / in_size
        
        if shrink_factor <= minimum_shrink_factor:
            # Replace with conversion
            if args.overwrite:
                try:
                    prefix, suffix = os.path.splitext(filename)
                    if suffix.lower() != '.pdf':
                        raise Exception('Problem with file extension {filename}')
                    out_file = prefix + '__compressed__.pdf'
            
                    with open(out_file, 'wb') as f:
                        f.write(ghostscript.stdout)
                        
                    backup_filename = prefix + '__original__.pdf'
                    os.rename(filename, backup_filename)
                    os.rename(out_file, filename)
                    
                    # Create empty file
                    with open(already_compressed_file, 'w') as f:
                        pass
                    
                    status = '[overwritten]'
                except:
                    print(f'Couldn\'t write file: {out_file}')
            else:
                status = '[would overwrite]'
        elif math.isnan(shrink_factor):
            status = '[previously compressed]'
        else:
            # Do nothing
            # Create empty file
            with open(already_compressed_file, 'w') as f:
                pass
            
            status = '[no action]'

        print(filename, f'original: {in_size // 1024 ** 2:.1f} MiB', f'{out_size // 1024 ** 2:.1f} MiB', f'{shrink_factor * 100:.1f}%', status, sep='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', help='Overwrite original files (otherwise don\'t write anything)', action='store_true')
    args = parser.parse_args()
    main(args)
    
