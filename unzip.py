import zipfile

zip_file_path = ".\data-clean\snapshot.zip"  # 输入你的ZIP文件路径
output_folder = ".\data-clean"     # 输入你想要解压到的文件夹路径

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(output_folder)

# print("ZIP file extracted to", output_folder)
