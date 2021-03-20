from image_extraction import StreetViewer
from __init__ import api_key, pic_base, meta_base

gwu = StreetViewer(api_key,location='800 21st St NW, Washington, DC 20052')
gwu.get_meta()

