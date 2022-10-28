import os
import sys
import glob
import subprocess
from astropy.table import Table

sys.path.append('../')
from protofielding import MOSDriverCat, MOSTrackingCat, MOSOBXML


hetdex = MOSDriverCat('/home/sumedha/Documents/Projects/WEAVE/WS2022B1-003-downloaded.fits', xml_template='BlankXMLTemplate.xml')


field_list = Table.read('/home/sumedha/Documents/Projects/WEAVE/WS2022B1-003_fieldcenters-v2.csv')

if not os.path.isdir('output-2'):
    os.mkdir('output-2')

for field in field_list:
    print(field)
    hetdex.process_ob(field['RA'], field['DEC'],
                      field['NAME'],
                      '11331', # Currently the only option in the HETDEX catalog
                      'GAEAD', # Fixed for all MOS WS2022B1-014 targets
                      'PLATE_A', report_verbosity=1,
                      output_dir='output-2')


