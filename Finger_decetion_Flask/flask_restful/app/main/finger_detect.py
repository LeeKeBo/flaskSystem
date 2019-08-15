import tensorflow as tf
from PIL import Image
import numpy as np
import os
import cv2


class detect_model():
    def __init__(self, model_path, top_b=10, bottom_b=30, left_b=0, right_b=0):
        # 读取模型
        output_graph_def = tf.GraphDef()
        # 打开.pb模型
        with open(model_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            tensors = tf.import_graph_def(output_graph_def, name="")
        self.__sess = tf.Session()
        self.__sess.run(tf.global_variables_initializer())
        graph = tf.get_default_graph()
        self.__image_tensor = graph.get_tensor_by_name("image_tensor:0")
        self.__detection_boxes = graph.get_tensor_by_name("detection_boxes:0")
        self.__detection_scores = graph.get_tensor_by_name("detection_scores:0")
        self.__detection_classes = graph.get_tensor_by_name("detection_classes:0")
        self.__num_detections = graph.get_tensor_by_name("num_detections:0")
        # 截取子图时，离底部边的上偏差和下偏差
        self.top_b = top_b
        self.bottom_b = bottom_b
        self.left_b = left_b
        self.right_b = right_b

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    # 截取出指尖附近的图像框
    def get_patch(self, out_put, image_path):
        ymax = out_put["ymax"]
        xmin = out_put["xmin"]
        xmax = out_put["xmax"]
        # print(ymax, xmin, xmax)
        img = cv2.imread(image_path)
        # 防止越界处理
        y1 = ymax - self.top_b if (ymax - self.top_b)>0 else ymax
        y2 = ymax + self.bottom_b if (ymax + self.bottom_b)<img.shape[0] else ymax
        x1 = xmin - self.left_b if (xmin - self.left_b)>0 else xmin
        x2 = xmax + self.right_b if (xmax + self.right_b)<img.shape[1] else xmax
        img_patch = img[y1:y2, x1:x2]  # x,y为常见坐标轴, 截取的行对应y, 截取的列对应x
        img_patch = cv2.resize(img_patch, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        return img_patch

    def inference(self, file_path, patch_folder, top_b=10, bottom_b=30, left_b=0, right_b=0):
        self.bottom_b = bottom_b
        self.top_b = top_b
        self.left_b = left_b
        self.right_b = right_b
        # 输入的图片数据
        image = Image.open(file_path)
        width, height = image.size
        image_np = self.load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # 推理
        (boxes, scores, classes, num) = self.__sess.run(
            [self.__detection_boxes, self.__detection_scores, self.__detection_classes, self.__num_detections],
            feed_dict={self.__image_tensor: image_np_expanded})
        s_boxes = boxes[scores > 0.5]
        s_classes = classes[scores > 0.5]
        s_scores = scores[scores > 0.5]
        # result
        # 模型没有检测到结果
        if len(s_classes) == 0:
            return None
        out_put = []
        for i in range(len(s_classes)):
            y_1 = s_boxes[i][0] * height  # ymin
            x_1 = s_boxes[i][1] * width  # xmin
            y_2 = s_boxes[i][2] * height  # ymax
            x_2 = s_boxes[i][3] * width  # xmax
            if y_1 > y_2:
                ymax = int(round(y_1))
                ymin = int(round(y_2))
            else:
                ymax = int(round(y_2))
                ymin = int(round(y_1))
            if x_1 > x_2:
                xmax = int(round(x_1))
                xmin = int(round(x_2))
            else:
                xmax = int(round(x_2))
                xmin = int(round(x_1))
            out_put.append({"ymin": ymin, "xmin": xmin, "ymax": ymax, "xmax": xmax,
                            "score": s_scores[i], "class": s_classes[i]})
            img_patch = self.get_patch(out_put[i], file_path)
            # save
            if os.path.exists(patch_folder) is False:
                os.mkdir(patch_folder)
            save_dir = os.path.join(patch_folder, file_path.split("/")[-1].split(".")[0])
            if os.path.exists(save_dir) is False:
                os.mkdir(save_dir)
            save_name = str(i) + '.jpg'
            save_path = os.path.join(save_dir, save_name)
            cv2.imwrite(save_path, img_patch)
        return out_put


