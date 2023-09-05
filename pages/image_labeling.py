import json
import streamlit as st
from google.cloud import vision

# 定数の定義部分

# Google のAPIキーを読み取り
credentials_dict = json.loads(st.secrets["google_credentials"])
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)

# 関数の定義部分

@st.cache_data
def load_sample_image():
    img_path = "./assets/img/family.png"
    with open(img_path, "rb") as f:
        img = f.read()

    return img

@st.cache_data
def get_response(content):

    image = vision.Image(content=content)

    response =  client.label_detection(image=image)

    return response

# 以下、表示部分

st.markdown("# 画像認識")

file = st.file_uploader("画像ファイルをアップロードしてください")

if file is not None:
    # 画像の表示
    content = file.getvalue()
    st.image(content)

    # 画像解析
    if st.button("解析をする"):
        response = get_response(content)
        labels = response.label_annotations
        st.write("Labels:")
        # 検出されたラベルを表示
        for label in labels:
            st.write(label.description)
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
