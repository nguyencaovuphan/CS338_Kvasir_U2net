import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
import numpy as np
from skimage import transform, io as skio
from model.u2net import U2NET
import cv2
import io

# 1. Thiết bị
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Load mô hình
model = U2NET(3, 1)
model_path = r"C:\Users\vuben\Desktop\cs338\u2net_best.pth"
state_dict = torch.load(model_path, map_location=device)
model.load_state_dict(state_dict)
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)
model.to(device)
model.eval()

def normalize_prediction(pred):
    pred_min = pred.min()
    pred_max = pred.max()
    return (pred - pred_min) / (pred_max - pred_min + 1e-8)

def predict(image_bytes):
    """
    Nhận diện vùng khối u từ ảnh đầu vào (dưới dạng bytes)
    Trả về: ảnh gốc, mask nhị phân, ảnh overlay
    """

    # Đọc ảnh từ bytes → numpy array (BGR)
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError("Không thể đọc ảnh từ input.")

    orig_img = img_bgr.copy()
    orig_h, orig_w = img_bgr.shape[:2]

    # Resize & convert to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = transform.resize(img_rgb, (512, 512), mode='constant') # skimage đã đưa về [0, 1]

    # Normalize
    img_normalized = (img_resized - np.array([0.485, 0.456, 0.406])) / \
                     np.array([0.229, 0.224, 0.225])

    # To tensor
    input_tensor = torch.tensor(img_normalized, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        prediction = output[0][0][0].cpu().numpy()  # [batch=0][channel=0]
        prediction = normalize_prediction(prediction)

    # Resize về kích thước ảnh gốc
    pred_resized = cv2.resize(prediction, (orig_w, orig_h))

    # Tạo mask nhị phân
    binary_mask = (pred_resized > 0.5).astype(np.uint8) * 255

    # Tạo ảnh overlay
    overlay = orig_img.copy()
    overlay[binary_mask > 0] = [0, 0, 255]
    overlay = cv2.addWeighted(orig_img, 0.7, overlay, 0.3, 0)

    return orig_img, binary_mask, overlay
