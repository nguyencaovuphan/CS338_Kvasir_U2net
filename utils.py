import numpy as np
from PIL import Image

def preprocess_image(file):
    """Đọc ảnh upload từ web."""
    image = Image.open(file).convert('RGB')
    return image

def postprocess_mask(mask):
    """Từ mask 2D (numpy) tạo ảnh đen trắng."""
    mask = (mask > 0.5).astype(np.uint8) * 255  # Ngưỡng 0.5
    return Image.fromarray(mask)
