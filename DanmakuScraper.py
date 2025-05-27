import re
import requests
import xml.etree.ElementTree as ET
import json


class DanmakuScraper:
    def __init__(self):
        self.headers = {
            'cookie': "buvid3=13689FCF-F9E5-B70D-798C-59776222F6E234771infoc; b_nut=1712022934; i-wanna-go-back=-1; b_ut=7; _uuid=2E62EAF9-9252-72B4-18DE-895FBDC6B8E635409infoc; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; buvid4=32F7A723-2D25-B194-3777-7F2E3D6F4CF235365-024040201-1NQ617oas%2FjOmUT9eQPCew%3D%3D; rpdid=|(k|k)mkuulu0J'u~uk|kkmYu; header_theme_version=CLOSE; CURRENT_QUALITY=80; fingerprint=39a1a0e5d810702629251926066728aa; buvid_fp_plain=undefined; SESSDATA=96447eca%2C1748763065%2C43804%2Ac1CjASXcyUQc31CINk-wa_ID2W1FmwtjwKhghHLkEhfF6ELd5tAj1yeVJ3tQHzRPcEwpUSVkhXRklwWWtnWGtvQWFPemYySERTQ09QSnhNR1FvaTQ2SkQ0MWwwV0QwTEVhQXVvWXNTU2dDTmJOeWRlS0N3RjhseEZ0NnRzbWktOXJMaXkyd1lMQ0x3IIEC; bili_jct=75df593d3e05cd6698d669ed3231b6ae; DedeUserID=30669100; DedeUserID__ckMd5=10cd8a7b56357a96; sid=6oa6n2a6; buvid_fp=af852e650373b29ee36d157b724195b4; LIVE_BUVID=AUTO6917338218818044; PVID=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ1MDU2NTgsImlhdCI6MTczNDI0NjM5OCwicGx0IjotMX0.OeS0k2aNcDSCv_MgKwkf2asJYk0OqEnqK7WBumc2SHs; bili_ticket_expires=1734505598; bp_video_offset_30669100=1011070451490750464; home_feed_column=4; browser_resolution=1270-1354; bp_t_offset_30669100=1011904955046428672; bsource=search_bing; CURRENT_FNVAL=4048; b_lsid=7410D391E_193D74C2D5A",
            'Referer': 'https://www.bilibili.com/video/BV1UqB2YUEfa/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=af32fbc38e2e1fd69040dfbf0a190747',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'content-Type': 'application/json; charset=utf-8'
        }

    def get_cid(self, bv):
        url = f'https://www.bilibili.com/video/{bv}'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        content = html.text
        cid_regx = '"bvid":"{}","cid":(.*?),"p":'.format(bv)
        cid = re.findall(cid_regx, content)[0]
        return cid

    def get_danmaku(self, cid):
        url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + cid

        try:
            html = requests.get(url, headers=self.headers)
            html.encoding = 'utf-8'
            content = html.text
            root = ET.fromstring(content)
            danmaku_list = []
            for index, danmaku in enumerate(root.findall('d')):
                danmaku_text = danmaku.text.strip()
                danmaku_list.append(danmaku_text)
            return danmaku_list
        except Exception as e:
            print(f"获取弹幕失败: {e}")
            return []

    def save_danmaku_to_json(self, bv, danmaku_list, file_path='danmaku_test.json'):
        try:
            # 尝试读取已有的JSON文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            # 如果文件不存在，初始化一个空列表
            existing_data = []

        result_dict = {
            "bv号": bv,
            "所有弹幕内容": danmaku_list
        }
        existing_data.append(result_dict)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    scraper = DanmakuScraper()
    # bv_list = ['BV1ucBqYpEAG', 'BV1r8UaYpEPa', 'BV1NeULY2EV2']  # 这里替换为你实际要爬取的BV号列表
    bv_list = ['BV1C7qdYbEYU', 'BV1e8B5YPEVm', 'BV1mYySYzEsU']  # 这里替换为你实际要爬取的BV号列表
    for bv in bv_list:
        cid = scraper.get_cid(bv)
        print('bv', bv)
        print('cid', cid)
        danmaku_list = scraper.get_danmaku(cid)
        scraper.save_danmaku_to_json(bv, danmaku_list)