import cv2
import numpy as np


class RGB2GRAY:
    def __init__(self, input_url, output_url):
        self.input_url = input_url
        self.output_url = output_url

    def get_url(self):
        return self.input_url

    def get_GRAY_Image(self):
        img = cv2.imread(self.input_url)
        #####Begin######
        b = img[:, :, 0]
        if np.max(b) > 100:
            b = b * (255 / np.max(b))
        binary_output = np.zeros_like(b)
        binary_output[((b > 90) & (b <= 230))] = 255
        ######End######
        cv2.imwrite(self.output_url, b)
        return (np.sum(binary_output))
