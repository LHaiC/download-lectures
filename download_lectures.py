import os
import requests
from urllib.parse import urljoin
from tqdm import tqdm

def download_with_progress(url, file_path):
    """带进度条的下载函数"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(file_path, 'wb') as file, tqdm(
        desc=os.path.basename(file_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

def download_lecture_files(base_url, output_dir="cs166_lectures"):
    """下载 lectures/00 到 lectures/18 中的 SlidesXX.pdf 和 SmallXX.pdf"""
    os.makedirs(output_dir, exist_ok=True)
    
    file_templates = [
        "Slides{num:02d}.pdf",
        "Small{num:02d}.pdf"
    ]
    
    for lecture_num in range(0, 19):
        subdir = f"{lecture_num:02d}/"
        subdir_url = urljoin(base_url, subdir)
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
        
        print(f"\n处理目录: {subdir}")
        
        for template in file_templates:
            file_name = template.format(num=lecture_num)
            file_url = urljoin(subdir_url, file_name)
            file_path = os.path.join(output_dir, subdir, file_name)
            
            try:
                if os.path.exists(file_path):
                    print(f"已存在: {subdir}{file_name}")
                    continue
                
                # 检查URL是否存在
                head_response = requests.head(file_url, timeout=10)
                if head_response.status_code != 200:
                    print(f"文件不存在: {file_name}")
                    continue
                
                print(f"下载中: {subdir}{file_name}")
                download_with_progress(file_url, file_path)
                
            except Exception as e:
                print(f"下载失败 {file_name}: {str(e)}")

if __name__ == "__main__":
    base_url = "https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/"
    download_lecture_files(base_url)