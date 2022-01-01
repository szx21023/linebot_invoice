import torch
import numpy as np

class AREA_MODEL:
    def __init__(self, weight):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight, force_reload=True)

    def predict(self, image, conf_threshold=0.5):
        self.image = image
        results = self.model(image, size=640)
        pred_l = []
        for pred in results.xyxy[0]:
            xmin, ymin, xmax, ymax, conf, ch = pred
            if float(conf) > conf_threshold:
                pred_l.append((int(xmin), int(ymin), int(xmax), int(ymax), float(conf), int(ch)))

        self.pred_l = sorted(pred_l, key=lambda l:l[4])
        return pred_l

    def parser_image_of_predict(self, index=0):
        xmin, ymin, xmax, ymax, _, _ = self.pred_l[index]
        return np.array(self.image)[ymin:ymax, xmin:xmax]
    
class OBJS_MODEL:
    def __init__(self, weight):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight, force_reload=True)

    def predict(self, image, conf_threshold=0.5):
        results = self.model(image, size=640)
        pred_l = []
        for pred in results.xyxy[0]:
            xmin, ymin, xmax, ymax, conf, ch = pred
            if float(conf) > conf_threshold:
                x, y = convert_result_to_coordinate(int(xmin), int(ymin), int(xmax), int(ymax))
                pred_l.append((x, y, int(ch)))

        return pred_l
    
def convert_result_to_coordinate(xmin, ymin, xmax, ymax):
    x = (xmin + xmax)//2
    y = (ymin + ymax)//2
    return x, y

def predict_of_invoice(img):
    area_model.predict(img)
    img_area = area_model.parser_image_of_predict()
    objs = objs_model.predict(img_area)
    objs = sorted(objs, key=lambda l:l[1])
    date, number = objs[:7], objs[7:]
    date = sorted(date, key=lambda l:l[0])
    number = sorted(number, key=lambda l:l[0])

    date = ''.join([str(d[2]) for d in date])
    number = ''.join([str(n[2]) for n in number])
    return date, number

area_weight = './yolo5_model/invoice.pt'
objs_weight = './yolo5_model/objs.pt'
area_model = AREA_MODEL(area_weight)
objs_model = OBJS_MODEL(objs_weight)
