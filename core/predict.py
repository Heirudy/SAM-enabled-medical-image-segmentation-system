import os
import sys
from importlib import import_module
import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from importlib import import_module

import argparse
import torch
from flask import *

from CTAI_flask.segment_anything import sam_model_registry


import cv2
import torch

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from torchvision.transforms import transforms

from CTAI_flask.metrics.metric import Metric
import os
from pathlib import Path
import matplotlib

from CTAI_flask.segment_anything import sam_model_registry

matplotlib.use('Agg')  # 防止 GUI 线程问题
import matplotlib.pyplot as plt

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
torch.set_num_threads(4)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

import os
rate = 0.5
import torch.nn.functional as F
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
#     # 归一化处理
#     # img_float = img_array.astype(np.float32) / 255.0
#     # mean = np.array(pixel_mean, dtype=np.float32)
#     # std = np.array(pixel_std, dtype=np.float32)
#     # normalized_img = (img_float - mean) / std
#     # # 调整维度顺序为 (C, H, W)
#     # if normalized_img.ndim == 3:
#     #     x = np.transpose(normalized_img, (2, 0, 1))
#     # else:
#     #     x = np.expand_dims(normalized_img, axis=0)
#     # # 转换为张量
#     # x_tensor = torch.from_numpy(x)
#     # # 将处理后的图像添加到列表
#
#
#     return x_tensor
def predict(image_path,model_path):


    parser = argparse.ArgumentParser()
    parser.add_argument('--root_path', type=str,
                        default=r"D:\2024\ssr\DATA\ACDC", help='Name of Experiment')
    parser.add_argument('--config', type=str, default=None, help='The config file provided by the trained model')
    parser.add_argument('--dataset', type=str, default='MoNuseg', help='Experiment name')
    parser.add_argument('--num_classes', type=int, default=1)
    parser.add_argument('--output_dir', type=str, default='./output')
    parser.add_argument('--img_size', type=int, default=1024, help='Input image size of the network')
    parser.add_argument('--input_size', type=int, default=224, help='The input size for training SAM model')
    parser.add_argument('--seed', type=int,
                        default=1337, help='random seed')
    parser.add_argument('--is_savenii', action='store_true', default=False,
                        help='Whether to save results during inference')
    parser.add_argument('--deterministic', type=int, default=1, help='whether use deterministic training')
    parser.add_argument('--ckpt', type=str, default='./checkpoints/sam_vit_b_01ec64.pth',
                        help='Pretrained checkpoint')

    parser.add_argument('--lora_ckpt', type=str,
                        default=r"D:\2024\ssr\BSAM-main\output\CXR_1024multiaug_maskatt\iter_600.pth",
                        help='The checkpoint from LoRA')
    parser.add_argument('--vit_name', type=str, default='vit_b_dualmask_same_prompt_class_random_large',
                        help='Select one vit model')
    parser.add_argument('--rank', type=int, default=4, help='Rank for LoRA adaptation')
    parser.add_argument('--module', type=str, default='sam_lora_image_encoder_prompt')
    parser.add_argument('--exp', type=str, default='2label_custom')
    parser.add_argument('--promptmode', type=str, default='point', help='prompt')

    args = parser.parse_args()

    sam, img_embedding_size = sam_model_registry[args.vit_name](image_size=args.img_size,
                                                                num_classes=args.num_classes,
                                                                checkpoint=args.ckpt, pixel_mean=[0, 0, 0],
                                                                pixel_std=[1, 1, 1])
    pkg = import_module(args.module)
    net = pkg.LoRA_Sam(sam, args.rank).cuda()
    assert args.lora_ckpt is not None
    net.load_lora_parameters(model_path)

    path =image_path
    print(f"Opening image at path: {path}")
    from PIL import Image
    import numpy as np
    import torch
    from albumentations import Compose, Resize, Normalize

    # 加载图像并调整大小
    img = Image.open(path).convert("RGB")  # 确保图像是 RGB 格式
    img = np.asarray(img)
    img_size = 1024
    pixel_mean = [0.5] * 3
    pixel_std = [0.5] * 3
    transform = Compose([
        Resize(img_size, img_size),  # 将 NumPy 数组转换为 PyTorch 张量并归一化到 [0, 1]
        Normalize(mean=pixel_mean, std=pixel_std)  # 进一步归一化
    ])
    aug_data = transform(image=img)
    x = aug_data["image"]
    if img.ndim == 3:
        x = np.transpose(x, axes=[2, 0, 1])
    elif img.ndim == 2:
        x = np.expand_dims(x, axis=0)
    image = torch.from_numpy(x)
    import matplotlib.pyplot as plt

    image = image.cuda()
    # metric = Metric(num_classes=2)

    image = image.unsqueeze(0)
    if len(image.shape) != 3:
        net.eval()
        with torch.no_grad():
            patch_size = [256, 256]
            outputs = net(image, multimask_output=True, image_size=1024)
            output_masks1 = outputs['masks']
            output_masks2 = outputs['masks2']
            output_masks1 = torch.softmax(output_masks1, dim=1)
            output_masks2 = torch.softmax(output_masks2, dim=1)

            # output_masks = custom_mask(output_masks1, output_masks2)
            output_masks = torch.softmax(output_masks1, dim=1)
            out = output_masks1

            pred = torch.max(out, dim=1)[1]



            test_save_path = r"D:\2024\ssr\CTAI-master\CTAI_flask\tmp\draw"
            predname = os.path.basename(path)
            print(predname)
            pred_path = os.path.join(test_save_path, predname)
            pred_image = pred.cpu().permute(1, 2, 0).detach().numpy()
            plt.figure(figsize=(10, 10))
            plt.imshow(pred_image, cmap='gray', interpolation='none')
            plt.axis('off')
            plt.savefig(pred_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
            image_path= path
            mask_path=pred_path
            return image_path,mask_path



# def predict(dataset,model):
#
#     # unet = torch.load('./core/0.5unet.pkl').to(device)
#     # torch.save(unet.state_dict(), "model_new.pth")
#
#     global res, img_y, mask_arrary
#     with torch.no_grad():
#         x = dataset[0][0].to(device)
#         file_name = dataset[1]
#         y = model(x)
#         img_y = torch.squeeze(y).cpu().numpy()
#         img_y[img_y >= rate] = 1
#         img_y[img_y < rate] = 0
#         img_y = img_y * 255
#         cv2.imwrite(f'./tmp/mask/{file_name}_mask.png', img_y,
#                     (cv2.IMWRITE_PNG_COMPRESSION, 0))

# def predict(image, net,image_path, multimask_output= True,  patch_size=[256, 256]):
#
#     image = image.cuda()
#     # metric = Metric(num_classes=2)
#     print(image.shape)
#     image=image.unsqueeze(0)
#     if len(image.shape) != 3:
#
#         net.eval()
#         with torch.no_grad():
#             outputs = net(image, multimask_output, patch_size[0])
#             output_masks1 = outputs['masks']
#             output_masks2 = outputs['masks2']
#             output_masks1=torch.softmax(output_masks1, dim=1)
#             output_masks2 = torch.softmax(output_masks2, dim=1)
#
#             output_masks=custom_mask(output_masks1,  output_masks2)
#             output_masks=torch.softmax(output_masks, dim=1)
#             out = output_masks1
#
#
#             pred = torch.max(out, dim=1)[1]
#             # pred1 = torch.max(output_masks1, dim=1)[1]
#             # pred2 = torch.max(output_masks2, dim=1)[1]
#             # # _, axs = plt.subplots(1, 2, figsize=(25, 25))
#             # axs[0].imshow(pred.cpu().permute(1, 2, 0).detach().numpy(), cmap='gray')
#             # axs[1].imshow(target.cpu().permute(1, 2, 0).detach().numpy(), cmap='gray')
#             # plt.subplots_adjust(wspace=0.01, hspace=0)
#             # filename = f"./target{i + 1}.png"
#             # full_path = os.path.join(test_save_path, filename)
#             # plt.figure(figsize=(8, 8))
#             # target_image = target.cpu().permute(1, 2, 0).detach().numpy()
#             # plt.imshow(target_image, cmap='gray', interpolation='none')
#             # plt.axis('off')
#             # plt.savefig(full_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
#             #
#             # filename = f"./image{i + 1}.png"
#             # full_path = os.path.join(test_save_path, filename)
#             # plt.figure(figsize=(10, 10))
#             # if len(image.shape) == 4 and image.shape[0] == 1:
#             #     target_image = image[0].cpu().permute(1, 2, 0).detach().numpy()
#             # else:
#             #     target_image = image.cpu().permute(1, 2, 0).detach().numpy()
#             # plt.imshow(target_image, interpolation='none')
#             # plt.axis('off')
#             # plt.savefig(full_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
#             #
#
#             test_save_path=r"D:\2024\ssr\CTAI-master\CTAI_flask\tmp\draw"
#             predname = os.path.basename(image_path)
#             print(predname)
#             pred_path = os.path.join(test_save_path, predname)
#             pred_image = pred.cpu().permute(1, 2, 0).detach().numpy()
#             plt.figure(figsize=(10, 10))
#             plt.imshow(pred_image, cmap='gray', interpolation='none')
#             plt.axis('off')
#             plt.savefig(pred_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
#
#
#             #
#             # pred1name = f"./pred{i + 1}_1.png"
#             # pred1_path = os.path.join(test_save_path, pred1name)
#             # pred1_image = pred1.cpu().permute(1, 2, 0).detach().numpy()
#             # plt.figure(figsize=(10, 10))
#             # plt.imshow(pred1_image, cmap='gray', interpolation='none')
#             # plt.axis('off')
#             # plt.savefig(pred1_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
#             #
#             # pred2name = f"./pred{i + 1}_2.png"
#             # pred2_path = os.path.join(test_save_path, pred2name)
#             # pred2_image = pred2.cpu().permute(1, 2, 0).detach().numpy()
#             # plt.figure(figsize=(10, 10))
#             # plt.imshow(pred2_image, cmap='gray', interpolation='none')
#             # plt.axis('off')
#             # plt.savefig(pred2_path, bbox_inches='tight', pad_inches=0, dpi=300, format='png')
#             #
#             # plt.close('all')
def fourier_transform(x):
    """
    对输入的图像张量进行傅里叶变换，并将频谱中心化。

    :param x: 输入的图像张量，形状为 [batch_size, channels, height, width]
    :return: 傅里叶变换后的频域图像，形状为 [batch_size, channels, height, width]
    """
    # 对每个通道进行傅里叶变换
    fft_image = torch.fft.fft2(x)  # 对图像进行傅里叶变换
    fft_image = torch.fft.fftshift(fft_image)  # 将频谱中心化
    return fft_image


def custom_mask(outputs1, outputs2, kernel_size=5):
    # 2. 进行频域处理：对输出进行傅里叶变换提取频域特征
    fft1 = fourier_transform(outputs1)
    fft2 = fourier_transform(outputs2)

    # 设定低频和高频的掩码
    low_freq_mask1 = torch.zeros_like(fft1)
    low_freq_mask1[:, :, fft1.shape[2] // 4:fft1.shape[2] // 2, fft1.shape[3] // 4:fft1.shape[3] // 2] = 1

    high_freq_mask1 = torch.ones_like(fft1)
    high_freq_mask1[:, :, fft1.shape[2] // 2:fft1.shape[2] // 4 * 3, fft1.shape[3] // 2:fft1.shape[3] // 4 * 3] = 0

    low_freq_mask2 = torch.zeros_like(fft2)
    low_freq_mask2[:, :, fft2.shape[2] // 4:fft2.shape[2] // 2, fft2.shape[3] // 4:fft2.shape[3] // 2] = 1

    high_freq_mask2 = torch.ones_like(fft2)
    high_freq_mask2[:, :, fft2.shape[2] // 2:fft2.shape[2] // 4 * 3, fft2.shape[3] // 2:fft2.shape[3] // 4 * 3] = 0

    # 获取低频部分
    low_freq1 = fft1 * low_freq_mask1
    low_freq2 = fft2 * low_freq_mask2

    # 获取高频中的低频部分
    high_freq_low_freq1 = fft1 * high_freq_mask1 * low_freq_mask1
    high_freq_low_freq2 = fft2 * high_freq_mask2 * low_freq_mask2

    # 合成：低频 * (高频中的低频) + 低频
    enhanced_fft1 = low_freq1 + 0.5*high_freq_low_freq1
    enhanced_fft2 = low_freq2 + 0.5*high_freq_low_freq2

    # 将频域转换回图像空间
    enhanced_fft1_shifted = torch.fft.ifftshift(enhanced_fft1)
    enhanced_image1 = torch.fft.ifft2(enhanced_fft1_shifted)
    enhanced_image_real1 = 0.5*torch.real(enhanced_image1)+outputs1

    enhanced_fft2_shifted = torch.fft.ifftshift(enhanced_fft2)
    enhanced_image2 = torch.fft.ifft2(enhanced_fft2_shifted)
    enhanced_image_real2 = 0.5*torch.real(enhanced_image2)+outputs2

    # 结合两种增强后的图像
    enhanced_fft = 0.5 * (enhanced_image_real1 + enhanced_image_real2)

    # 卷积操作以保持图像大小
    kernel_size = int(kernel_size)  # 获取卷积核大小
    kernel_size = max(kernel_size, 3)  # 最小卷积核大小为3
    kernel = torch.ones(1, 1, kernel_size, kernel_size) / (kernel_size ** 2)
    kernel = kernel.to(outputs1.device)

    padding = (kernel_size - 1) // 2
    kernel = kernel.expand(enhanced_fft.size(1), -1, -1, -1)

    # 执行卷积操作，确保输出尺寸与原图一致
    aver_vector = F.conv2d(enhanced_fft, kernel, padding=padding, groups=enhanced_fft.size(1))

    return aver_vector

if __name__ == '__main__':
    # 写保存模型
    sam, img_embedding_size = sam_model_registry["vit_b"](image_size=1024,
                                                                    num_classes=2,
                                                                    checkpoint=r"D:\2024\ssr\CTAI-master\CTAI_flask\checkpoints\sam_vit_b_01ec64.pth", pixel_mean=[0, 0, 0],
                                                                    pixel_std=[1, 1, 1])



    # predict(input,model,path)
