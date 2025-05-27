import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import json

# 热门tag类型列表
type_list = ["douga", "music", "dance", "game", "knowledge", "tech", "sports", "car", "life", "food", "animal", "kichiku",
             "fashion", "ent", "cinephile"]


def get_video_bv(type_name):
    url = f"https://www.bilibili.com/v/popular/rank/{type_name}"
    options = Options()

    # options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    driver = webdriver.Edge(options=options)

    print(f"正在获取{type_name}的bv")
    try:
        driver.get(url)
        time.sleep(5)  # 等待页面加载完成，可根据实际情况调整等待时间

        bv_numbers = []
        for i in range(1, 21):  # 取前20个视频
            try:
                bv_element = driver.find_element(By.CSS_SELECTOR, f'li.rank-item:nth-child({i}) a.title')
                bv_link = bv_element.get_attribute('href')
                bv_number = bv_link.split('/')[-1]
                bv_numbers.append(bv_number)
            except:
                break  # 如果找不到元素，说明已经没有更多视频，退出循环

        print("bv获取成功")
        return bv_numbers
    finally:
        driver.quit()


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 用于存储最终结果的字典
result_dict = {}

for type_name in type_list:
    bv_numbers = get_video_bv(type_name)
    result_dict[type_name] = {i + 1: bv for i, bv in enumerate(bv_numbers)}

# 将结果字典保存为JSON文件
save_to_json(result_dict, 'hot_videos_bv.json')