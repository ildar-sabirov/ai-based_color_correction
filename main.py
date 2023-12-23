import io

import numpy as np
import streamlit as st
from PIL import Image
import cv2
from python_color_transfer.color_transfer import ColorTransfer


def load_image(label):
    uploaded_file = st.file_uploader(label=f'**{label}:**')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


def perform_color_correction(input_image, ref_image):
    img_arr_in = cv2.cvtColor(np.array(input_image), cv2.COLOR_RGB2BGR)
    img_arr_ref = cv2.cvtColor(np.array(ref_image), cv2.COLOR_RGB2BGR)

    PT = ColorTransfer()
    img_arr_mt = PT.mean_std_transfer(img_arr_in=img_arr_in, img_arr_ref=img_arr_ref)

    st.write('**Результат коррекции:**')
    st.image(cv2.cvtColor(img_arr_mt, cv2.COLOR_BGR2RGB))


def main():
    img_arr_in = load_image('Выберите изображение')
    img_arr_ref = load_image('Выберите изображение референс')

    if img_arr_in is not None and img_arr_ref is not None:
        perform_color_correction(img_arr_in, img_arr_ref)


if __name__ == '__main__':
    main()
