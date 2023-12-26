import tempfile
import streamlit as st
import numpy as np
from PIL import Image
import cv2
from python_color_transfer.color_transfer import ColorTransfer

ss = st.session_state
ss.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))


def clahe_image(img):
    # Разделяем изображение на каналы
    b, g, r = cv2.split(img)
    # Применяем CLAHE к каждому каналу
    b_clahe = ss.clahe.apply(b)
    g_clahe = ss.clahe.apply(g)
    r_clahe = ss.clahe.apply(r)
    # Объединяем каналы обратно
    img_clahe = cv2.merge([b_clahe, g_clahe, r_clahe])

    return img_clahe


def load_file(label, file_types):
    uploaded_file = st.sidebar.file_uploader(label=f'{label}:', type=file_types)
    return uploaded_file


def process_image(img_data, ref_image):
    img_arr_in = cv2.cvtColor(np.array(img_data, dtype=np.uint8), cv2.COLOR_RGB2BGR)
    img_arr_ref = cv2.cvtColor(np.array(ref_image, dtype=np.uint8), cv2.COLOR_RGB2BGR)

    PT = ColorTransfer()
    img_arr_mt = PT.mean_std_transfer(img_arr_in=img_arr_in, img_arr_ref=img_arr_ref)

    # Применение CLAHE к каждому каналу
    img_arr_mt_clahe = clahe_image(img_arr_mt)

    ss.win2.image(
        cv2.cvtColor(img_arr_mt_clahe, cv2.COLOR_BGR2RGB), use_column_width=True
    )


def load_video(video_data):
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file_path = temp_video_file.name
    temp_video_file.write(video_data.read())
    temp_video_file.close()
    cap = cv2.VideoCapture(temp_video_file_path)
    return cap


def process_video(video, ref_image):
    while True:
        # Читаем кадр из видео
        ret, frame = video.read()
        # Если кадр не удалось прочитать, выходим из цикла
        if not ret:
            break
        process_image(frame, ref_image)


def main():
    ext_img = ["jpg", "jpeg", "png"]
    ext_vid = ["mp4"]
    img_arr_ref = load_file('Выберите изображение референс', ext_img)
    img_arr_in = load_file('Выберите изображение или видео', ext_img + ext_vid)

    st.header('Результат коррекции:')
    win1 = st.empty()
    ss.win2 = st.empty()

    if (img_arr_in is not None) and (img_arr_ref is not None):
        if "image" in img_arr_in.type:
            img_arr = Image.open(img_arr_in)
            img_arr_ref = Image.open(img_arr_ref)
            win1.image(img_arr, use_column_width=True)
            process_image(img_arr, img_arr_ref)
        elif "video" in img_arr_in.type:
            video = load_video((img_arr_in))
            img_arr_ref = Image.open(img_arr_ref)
            win1.image(img_arr_ref, use_column_width=True)
            process_video(video, img_arr_ref)


if name == 'main':
    main()
