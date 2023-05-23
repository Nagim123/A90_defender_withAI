import cv2
import numpy as np


class ModelRunner():
    def __init__(self, img_size: int) -> None:
        self.net = cv2.dnn.readNetFromONNX("best.onnx")
        self.img_size = img_size

    def detect(self, img: cv2.Mat):
        img = cv2.resize(img, (256,256))
        img = self._normalize(img)
        self.net.setInput(img)
        predictions = self.net.forward()
        if not predictions is None:
            if predictions[0][0] > predictions[0][1]:
                return True
            return False
        return None

    def _normalize(self, img: cv2.Mat):
        MEAN = 255 * np.array([0.485, 0.456, 0.406])
        STD = 255 * np.array([0.229, 0.224, 0.225])
        x = np.array(img)
        x = x.transpose(-1, 0, 1)
        x = (x - MEAN[:, None, None]) / STD[:, None, None]
        return x.reshape(1, 3, self.img_size, self.img_size)