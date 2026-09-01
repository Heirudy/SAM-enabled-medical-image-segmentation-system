import os

import SimpleITK as sitk
import cv2
import numpy as np
import torch
from torchvision.transforms import transforms


def data_in_one(inputdata):
    if not inputdata.any():
        return inputdata
    inputdata = (inputdata - inputdata.min()) / (inputdata.max() - inputdata.min())
    return inputdata


def pre_process(data_path):
    global test_image, test_mask
    image_list, mask_list, image_data, mask_data = [], [], [], []

    image = sitk.ReadImage(data_path)
    image_array = sitk.GetArrayFromImage(image)

    ROI_mask = np.zeros(shape=image_array.shape)
    ROI_mask_mini = np.zeros(shape=(1, 160, 100))
    ROI_mask_mini[0] = image_array[0][270:430, 200:300]
    ROI_mask_mini = data_in_one(ROI_mask_mini)
    ROI_mask[0][270:430, 200:300] = ROI_mask_mini[0]
    test_image = ROI_mask
    image_tensor = torch.from_numpy(ROI_mask).float().unsqueeze(1)
    # print(image_tensor.shape)
    image_data.append(image_tensor)
    file_name = os.path.split(data_path)[1].replace('.dcm', '')

    # 转为图片写入image文件夹

    image_array = image_array.swapaxes(0, 2)
    image_array = np.rot90(image_array, -1)
    image_array = np.fliplr(image_array).squeeze()
    # ret, image_array = cv2.threshold(image_array, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'./tmp/image/{file_name}.png', image_array, (cv2.IMWRITE_PNG_COMPRESSION, 0))

    return image_data, file_name


def last_process(file_name):
    image = cv2.imread(f'./tmp/image/{file_name}.png')
    mask = cv2.imread(f'./tmp/mask/{file_name}_mask.png', 0)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found in the mask image.")
        # 可以在这里处理没有找到轮廓的情况，例如跳过绘制步骤或记录错误信息
    else:
        draw = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # thresh, contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # draw = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # cv2.imwrite(f'./tmp/draw/{file_name}.png', draw)


import numpy as np
from PIL import Image
import torch

from PIL import Image
import numpy as np
import torch
from albumentations import Compose, Resize, Normalize

def process_images(img_path, pixel_mean=[0.5] * 3, pixel_std=[0.5] * 3, img_size=1024):
    """
    处理单张图像，加载、调整大小、归一化并转换为张量。

    参数:
        img_path (str): 图像路径。
        pixel_mean (list): 像素均值，用于归一化。
        pixel_std (list): 像素标准差，用于归一化。
        img_size (int): 调整图像大小的目标尺寸。

    返回:
        torch.Tensor: 处理后的图像张量。
    """
    print(f"Opening image at path: {img_path}")

    # 加载图像并调整大小
    img = Image.open(img_path).convert("RGB")  # 确保图像是 RGB 格式
    img = np.asarray(img)

       # 定义转换操作
    transform =Compose([
        Resize(img_size,img_size),  # 将 NumPy 数组转换为 PyTorch 张量并归一化到 [0, 1]
        Normalize(mean=pixel_mean, std=pixel_std)  # 进一步归一化
    ])
    aug_data = transform(image=img)
    x = aug_data["image"]
    if img.ndim == 3:
        x = np.transpose(x, axes=[2, 0, 1])
    elif img.ndim == 2:
        x = np.expand_dims(x, axis=0)


    return torch.from_numpy(x)
# def process_images(img_paths,pixel_mean=[0.5] * 3, pixel_std=[0.5] * 3, img_size=1024):
#     """
#     处理图像数据集，加载、调整大小、归一化并转换为张量。
#
#     参数:
#         img_paths (list): 图像路径列表。
#         mask_divide (bool): 是否对掩码进行划分（此功能未使用，保留参数）。
#         divide_value (int): 划分值（此功能未使用，保留参数）。
#         pixel_mean (list): 像素均值，用于归一化。
#         pixel_std (list): 像素标准差，用于归一化。
#         img_size (int): 调整图像大小的目标尺寸。
#
#     返回:
#         list: 包含处理后的图像张量的字典列表。
#     """
#
#     # 加载图像并调整大小
#     print(f"Opening image at path: {img_paths}")
#     img = Image.open(img_paths).convert("RGB")
#     img = img.resize((img_size, img_size))
#     img_array = np.asarray(img,dtype=np.float32)
#     # 转换为 PyTorch 张量
#     img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)  # 调整维度顺序为 (C, H, W)
#
#     # 定义归一化操作
#     normalize = transforms.Normalize(mean=pixel_mean, std=pixel_std)
#
#     # 应用归一化
#     normalized_tensor = normalize(img_tensor / 255.0)  # 先将像素值归一化到 [0, 1]
#
#     return normalized_tensor
    # 归一化处理
    # img_float = img_array.astype(np.float32) / 255.0
    # mean = np.array(pixel_mean, dtype=np.float32)
    # std = np.array(pixel_std, dtype=np.float32)
    # normalized_img = (img_float - mean) / std
    # # 调整维度顺序为 (C, H, W)
    # if normalized_img.ndim == 3:
    #     x = np.transpose(normalized_img, (2, 0, 1))
    # else:
    #     x = np.expand_dims(normalized_img, axis=0)
    # # 转换为张量
    # x_tensor = torch.from_numpy(x)
    # # 将处理后的图像添加到列表


    return x_tensor

if __name__ == '__main__':
    path = r"D:\2024\ssr\CTAI-master\CTAI_flask\tmp\image\image1.png"
    process_images(path)
