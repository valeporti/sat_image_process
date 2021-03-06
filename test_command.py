import subprocess
import os
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps, loads
from xml.dom import minidom
from collections import OrderedDict
from xmljson import BadgerFish 
from xmljson import Abdera 
from xmljson import Yahoo              # import the class

output_dir = '/home/valeporti/Documents/test/'
sumo_dir = '/home/valeporti/Documents/SUMO'
s1_dir = '/mnt/12564BAC564B8F81/code/learn/ps4/peps_download/S1A_IW_GRDH_1SDV_20151108T214342_20151108T214407_008519_00C0F6_BB56.SAFE'

def runSumo():
  
  s1_file = s1_dir + '/manifest.safe'
  
  thh = tvv = 1.5
  thv = tvh = 1.2

  if (not os.path.isdir(sumo_dir) or not os.path.exists(s1_file) or not os.path.isdir(output_dir)) :
    print('error, directory does not exist')
    print(os.path.isdir(sumo_dir))
    print(os.path.exists(s1_file))
    print(os.path.isdir(output_dir))
    return 

  subprocess.check_call(f'cd {sumo_dir}/ && {sumo_dir}/start_batch.sh -i {s1_file} -thh {thh} -thv {thv} -tvh {tvh} -tvv {tvv} -sh {sumo_dir}/resources/coastline/OSMLandPoly_20141001_250/OSMLandPoly_20141001_250m.shp -b 0 -o {output_dir}',
    shell=True)

  
def getJsonDetections(output_dir):

  path_xml = ''
  for file in os.listdir(output_dir):
    if file.endswith(".xml"):
      path_xml = os.path.join(output_dir, file) # should be just one
  
  xml_string = ''
  with open(path_xml, 'r') as myfile:
    xml_string = myfile.read().replace('\n', '')
  
  bf = Yahoo(dict_type=OrderedDict, xml_fromstring=True)
  json = loads(dumps(bf.data(fromstring(xml_string))))

  detections_arr = json['analysis']['vds_target']['boat']
  metadata = json['analysis']['sat_image_metadata']
  vds_analysis = json['analysis']['vds_analysis']
  
  
  return { 'detected': detections_arr, 'metadata': metadata, 'vds_analysis': vds_analysis }

def compatibilityRevision() :
  
  try: 
    where_images = s1_dir + '/measurement'
    if (os.path.isdir(where_images)) :
      # check if tiff file
      for file in os.listdir(where_images):
        if file.endswith(".tiff"):
          return True
      return False
  except:
    print('Error in compatibility Revision')


#if (compatibilityRevision()):
runSumo()
#  results = getJsonDetections()

import json
from PIL import Image, ImageDraw
import numpy as np
import math
Image.MAX_IMAGE_PIXELS = 1000000000

def getBoats():
  results = getJsonDetections(output_dir)
  image = Image.open(s1_dir + '/measurement/s1a-iw-grd-vv-20151108t214342-20151108t214407-008519-00c0f6-001.tiff')
  w, h = image.size
  minimun_size = 60
  count = 1
  for detection in results['detected']:
    x_pixel = detection['xpixel']
    y_pixel = detection['ypixel']
    length = detection['length']
    width = detection['width']
    box = (x_pixel - minimun_size, y_pixel - minimun_size, x_pixel + minimun_size, y_pixel + minimun_size) # The crop rectangle, as a (left, upper, right, lower)-tuple
    cropped_img = image.crop(box)
    cropped_img.save('new', format='tiff')
    im = cropped_img.convert('RGBA')
    draw = ImageDraw.Draw(im)
    one = minimun_size - max([length, width])
    two = minimun_size + max([length, width])
    draw.rectangle(((one, one), (two, two)), outline="#ff8888")
    im.save('./output/' + str(count) + '_img', format='png')
    count += 1

"""
#getBoats()
results = getJsonDetections(output_dir)
#print(json.dumps(results['metadata'], indent=2, sort_keys=True))
#print(json.dumps(results['vds_analysis'], indent=2, sort_keys=True))
image_0 = results['detected'][0]
#print(json.dumps(image_0, indent=2, sort_keys=True))

x_pixel = image_0['xpixel']
y_pixel = image_0['ypixel']
nbr_pixels = image_0['nr_pixels']
reliability = image_0['reliability'] # currently can have the following two values: 0: likely real target; 3: likely false alarm.
lwh_reliability = image_0['lwh_reliability'] # is true if the parameters length, width and heading are deemed to be reliable (e.g. for a large, well-defined, elongated target) and false if not.
length = image_0['length']
width = image_0['width']
lon = image_0['lon']
lat = image_0['lat'] 

matrix_rotation = np.matrix((math))

results = getJsonDetections(output_dir)
#print(json.dumps(results['metadata'], indent=2, sort_keys=True))
#print(json.dumps(results['vds_analysis'], indent=2, sort_keys=True))

#def getXYAngle(heading_north, heading_range):


#*************************************************************************************
#*************************************************************************************
#infoImage = results['metadata']
#infoIntermediaire = results['vds_analysis']
#infoNavire =  image_0
#import collection.OrderedDict
#dictImage = OrderedDict()
#dictImage = {}
#dictDet = {}
#dictImage["ImId"]= infoImage["ImId"]
#dictImage["image_name"]= infoImage["image_name"] 
#dictImage["nr_detections"]= infoIntermediaire["nr_detections"]
#dictDet["ImId"]= infoImage["ImId"]
#dictDet["lat"]= infoNavire["lat"]
#dictDet["lon"]= infoNavire["lon"]
#dictDet["length"]= infoNavire["length"]
#dictDet["reliability"]= infoNavire["reliability"]



#client = MongoClient('localhost', 27017)
#my_db = client["ps4_test_1_May"]
#tableImage = my_db["Image"]
#tableImage.insert_one(dictImage)
#tableDet = my_db["Detection"]
#tableDet.insert_one(dictDet)


import pymongo
from pymongo import MongoClient


def insererInfoImageEtDetectionsSUMO(output_dir):
  results = getJsonDetections(output_dir)
  infoImage = results['metadata']
  infoIntermediaire = results['vds_analysis']
  #infoNavire =  image_0
  #import collection.OrderedDict
  #dictImage = OrderedDict()
  
  #faire dictionnaire dictImage
  dictImage = {}
  dictImage["ImId"]= infoImage["ImId"]
  dictImage["image_name"]= infoImage["image_name"] 
  dictImage["nr_detections"]= infoIntermediaire["nr_detections"]

  #connect avec Mongo
  client = MongoClient('localhost', 27017)
  my_db = client["ps4_test_1_May"]

  #charge database
  tableImage = my_db["Image"]
  tableImage.insert_one(dictImage)
  
  for detection in results['detected']:
    #faire dictionnaire dictDet
    dictDet = {}
    dictDet["target_number"]= detection["target_number"]
    dictDet["lat"]= detection["lat"]
    dictDet["lon"]= detection["lon"]
    dictDet["length"]= detection["length"]
    dictDet["reliability"]= detection["reliability"]
    dictDet["ImId"]= infoImage["ImId"]
    #charge database
    tableImage = my_db["Detection"]
    tableImage.insert_one(dictDet)

#insererInfoImageEtDetectionsSUMO(output_dir) 
"""