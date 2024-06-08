import xml.etree.ElementTree as ET
import base64
from io import BytesIO
from PIL import Image

def restore_image_from_xml(xml_file, image_file):
    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图像数据
    image_data_element = root.find("digital_setup")
    if image_data_element is not None:
        # 解码base64编码的图像数据
        encoded_image_data = image_data_element.text
        decoded_image_data = base64.b64decode(encoded_image_data)

        # 将图像数据保存到文件
        with open(image_file, "wb") as f:
            f.write(decoded_image_data)

        print(f"图像已成功保存到 {image_file}")
    else:
        print("未找到图像数据")

# 指定XML文件和要保存的图像文件
xml_file_path = "SDS2102XPlus_Setup_3.xml"
image_file_path = "1.jpg"

# 恢复图像
restore_image_from_xml("C:/Users/32277/desktop/SDS2102XPlus_Setup_3.xml", "C:/Users/32277/Desktop/1.jpg")

