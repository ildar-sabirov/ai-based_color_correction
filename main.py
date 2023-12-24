import os
import tempfile
import streamlit as st
import numpy as np
from PIL import Image
import cv2
#from moviepy.editor import VideoFileClip
from python_color_transfer.color_transfer import ColorTransfer

ss = st.session_state
# Создаем  CLAHE
ss.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
def clahe_image(img):
    curr_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    # применим CLAHE к каналу яркости 
    y = curr_yuv[:, :, 0]
    y_clahe = clahe.apply(y)
    curr_yuv[:, :, 0] = y_clahe
    return img

def load_file(label, file_types):
    uploaded_file = st.sidebar.file_uploader(label=f'**{label}:**', type=file_types)
    return uploaded_file


def process_image(img_data, ref_image, win2):
    img_arr_in = cv2.cvtColor(np.array(img_data, dtype=np.uint8), cv2.COLOR_RGB2BGR)
    img_arr_ref = cv2.cvtColor(np.array(ref_image, dtype=np.uint8), cv2.COLOR_RGB2BGR)

    PT = ColorTransfer()
    img_arr_mt = PT.mean_std_transfer(img_arr_in=img_arr_in, img_arr_ref=img_arr_ref)
    img_arr_mt = cv2.cvtColor(img_arr_mt, cv2.COLOR_BGR2RGB)
    img_arr_mt = ss.clahe.apply(img_arr_mt)

    win2.image(cv2.cvtColor(img_arr_mt, cv2.COLOR_BGR2RGB), use_column_width=True)

def load_video(video_data):
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file_path = temp_video_file.name
    temp_video_file.write(video_data.read())
    temp_video_file.close()
    cap = cv2.VideoCapture(temp_video_file_path)
    return cap
def process_video(video, ref_image, win):
    # будем перебирать кадры из видео
    while True:
        # читаем кадр из видео
        ret, frame = video.read()   
        # если не але
        if not ret:
            break
        processed_frame = process_image(frame,ref_image, win)
        if not ret:
            break





def main():
    ext_img = ["jpg", "jpeg", "png"]
    ext_vid = ["mp4"]
    img_arr_ref = load_file('Выберите изображение референс', ext_img)
    img_arr_in = load_file('Выберите изображение или видео', ext_img + ext_vid)


    st.header('**Результат коррекции:**')
    #win = st.empty()
    win1 = st.empty()
    win2 = st.empty()
    #col1,col2 = st.columns(2)
    btn = st.button('Обновить результат')
    if (img_arr_in is not None) and (img_arr_ref is not None):
        if "image" in img_arr_in.type:
            img_arr = Image.open(img_arr_in)
            img_arr_ref = Image.open(img_arr_ref)
            win1.image(img_arr, use_column_width=True)
            process_image(img_arr, img_arr_ref, win2)
        elif "video" in img_arr_in.type:
            video = load_video((img_arr_in))            
            img_arr_ref = Image.open(img_arr_ref)
            win1.image(img_arr_ref, use_column_width=True)
            process_video(video, img_arr_ref,win2)



if __name__ == '__main__':
    main()
