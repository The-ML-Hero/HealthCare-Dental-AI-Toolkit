from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import secrets
import requests
from .models import CBCT_Model
import cv2
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import PIL
import numpy as np
from detectron2.utils.visualizer import ColorMode
import urllib
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.data.datasets import register_coco_instances
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog,DatasetCatalog
# Create your views here.
 
o = int(np.random.randint(low=10301319,high=9987869996)) 
cfg = get_cfg()
cfg.MODEL.DEVICE='cpu'
cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
register_coco_instances(f"tooth_segmentation_maskrcnn{o}",{},str(f"{settings.BASE_DIR}/InstanceSegmentationSegmentationTooth/ann/instances_default.json"),str(f"{settings.BASE_DIR}/InstanceSegmentationSegmentationTooth/img"))
meta_teeth = MetadataCatalog.get(f"tooth_segmentation_maskrcnn{o}")
cfg.DATASETS.TRAIN = (f"tooth_segmentation_maskrcnn{o}",)
cfg.DATASETS.TEST = ()
cfg.DATASETS.NUM_WORKERS = 2
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = 1200
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
cfg.MODEL.WEIGHTS = str(f'{settings.BASE_DIR}/mask rcnn.pth')  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1   # set a custom testing threshold
predictor = DefaultPredictor(cfg)

file_random_name = secrets.token_hex(32)

def root_mask(request):
    context = {}
    if request.method == 'POST':
        uploaded_file_input = request.FILES.get('cbct_input_image')
        fs = FileSystemStorage()
        name = fs.save(uploaded_file_input.name, uploaded_file_input)
        context['URL_Input'] = fs.url(name)
        input_image_url = requests.get(f'https://healthcare-toolkit-dental-ai.herokuapp.com{fs.url(name)}')
        CBCT_Model.objects.create(CBCT_file=uploaded_file_input,CBCT_name='Uploaded File')

        image_input = urllib.request.urlopen(f'https://healthcare-toolkit-dental-ai.herokuapp.com{fs.url(name)}')
        arr_input = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
        Image_input =  cv2.imdecode(arr_input, -1)
        output = predictor(Image_input)
        v = Visualizer(Image_input[:, :, ::-1],
                  metadata=meta_teeth, 
                  scale=0.5, 
                  instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
        )

        out = v.draw_instance_predictions(output["instances"].to("cpu"))
        cv2.imwrite(f'./media/images/root_segmentation/output_MASK_DETECTRON{file_random_name}.png',out.get_image()[:, :, ::-1])

        CBCT_Model.objects.create(CBCT_image =f'./images/root_segmentation/output_MASK_DETECTRON{file_random_name}.png' ,CBCT_name='Output File')
        
        context['URL_Output'] = f'https://healthcare-toolkit-dental-ai.herokuapp.com/media/images/root_segmentation/output_MASK_DETECTRON{file_random_name}.png'

        if int(output["instances"].pred_classes[0]) == 0:
             context['classes_pred'] = 'CShaped'
        else:
            context['classes_pred'] = 'Normal'
    return render(request,'root_mask.html',context)
