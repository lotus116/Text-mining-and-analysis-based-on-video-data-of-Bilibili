import json
from CommentScraper import CommentScraper
from DanmakuScraper import DanmakuScraper

# 读取hot_videos_bv_.txt中的数据
with open('hot_videos_bv.json', 'r', encoding='utf-8') as f:
    bv_data = json.load(f)

# 初始化评论爬虫和弹幕爬虫
comment_scraper = CommentScraper()
danmaku_scraper = DanmakuScraper()

# 用于存储最终结果的字典
result_dict = {}

# 遍历每个分区和对应的BV号
for category, videos in bv_data.items():
    category_result = {}
    for rank, bv in videos.items():
        print(f"正在爬取 {category} 分区，BV号：{bv} 的评论和弹幕...")
        # 爬取评论
        comment_result = comment_scraper.get_reply(bv, 500)  # 这里设置爬取500条评论，你可以根据需要调整
        # 爬取弹幕
        cid = danmaku_scraper.get_cid(bv)
        danmaku_result = danmaku_scraper.get_danmaku(cid)
        print("获取弹幕成功")
        category_result[bv] = {
            "所有评论": comment_result["所有评论内容"],
            "所有弹幕": danmaku_result
        }
    result_dict[category] = category_result


    # 将结果保存为JSON文件
    with open(f'video_info_{category}.json', 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)

# 将结果保存为JSON文件
with open('video_info.json', 'w', encoding='utf-8') as f:
    json.dump(result_dict, f, ensure_ascii=False, indent=4)