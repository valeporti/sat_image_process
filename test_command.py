import subprocess
import os
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps, loads
from xml.dom import minidom
from collections import OrderedDict
from xmljson import BadgerFish              # import the class

output_dir = '/home/valeporti/Documents/test/'

def runSumo():

  sumo_dir = '/home/valeporti/Documents/SUMO'
  s1_file = '/mnt/12564BAC564B8F81/code/learn/ps4/peps_download/S1A_IW_GRDH_1SDV_20151108T214342_20151108T214407_008519_00C0F6_BB56.SAFE/manifest.safe'
  
  thh = tvv = 1.5
  thv = tvh = 1.2

  if (not os.path.isdir(sumo_dir) or not os.path.exists(s1_file) or not os.path.isdir(output_dir)) :
    print('error, directory does not exist')
    print(os.path.isdir(sumo_dir))
    print(os.path.exists(s1_file))
    print(os.path.isdir(output_dir))
    return 

  subprocess.run(f'cd {sumo_dir}/ && {sumo_dir}/start_batch.sh -i {s1_file} -thh {thh} -thv {thv} -tvh {tvh} -tvv {tvv} -sh {sumo_dir}/resources/coastline/OSMLandPoly_20141001_250/OSMLandPoly_20141001_250m.shp -b 0 -o {output_dir}',
    shell=True)

  
def getJsonDetections():

  path_xml = ''
  for file in os.listdir(output_dir):
    if file.endswith(".xml"):
      path_xml = os.path.join(output_dir, file) # should be just one
  
  xml_string = ''
  with open(path_xml, 'r') as myfile:
    xml_string = myfile.read().replace('\n', '')
  
  bf = BadgerFish(dict_type=OrderedDict, xml_fromstring=True)
  json = loads(dumps(bf.data(fromstring(xml_string))))

  detections_arr = json['analysis']['vds_target']['boat']
  

getJsonDetections()



