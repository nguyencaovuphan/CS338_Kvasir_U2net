# Tumor Segmentation Web App (U2-Net + FastAPI)

A simple web application for segmenting tumors in medical images using the **U²-Net** architecture. Built with **FastAPI**, **OpenCV**, and **PyTorch**.

## Features

- Upload an image and get:
  - Original image
  - Binary tumor mask
  - Overlay image
- Runs prediction using pre-trained **U²-Net**
- Web interface powered by **FastAPI** + **Jinja2 templates**

## Model

- Architecture: [U²-Net](https://arxiv.org/abs/2005.09007)
- Trained on: [Kvasir-SEG Dataset](https://datasets.simula.no/kvasir-seg/)

## Installation

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate

pip install -r requirements.txt
```
## Run the App
```bash
uvicorn main:app --reload
```
