import hashlib
import time
import requests
import re
import random
import json


class CommentScraper:
    def __init__(self):
        # 请求头
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 需定期更换cookie，否则location爬不到
            'cookie': "buvid3=13689FCF-F9E5-B70D-798C-59776222F6E234771infoc; b_nut=1712022934; i-wanna-go-back=-1; b_ut=7; _uuid=2E62EAF9-9252-72B4-18DE-895FBDC6B8E635409infoc; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; buvid4=32F7A723-2D25-B194-3777-7F2E3D6F4CF235365-024040201-1NQ617oas%2FjOmUT9eQPCew%3D%3D; rpdid=|(k|k)mkuulu0J'u~uk|kkmYu; header_theme_version=CLOSE; CURRENT_QUALITY=80; fingerprint=39a1a0e5d810702629251926066728aa; buvid_fp_plain=undefined; SESSDATA=96447eca%2C1748763065%2C43804%2Ac1CjASXcyUQc31CINk-wa_ID2W1FmwtjwKhghHLkEhfF6ELd5tAj1yeVJ3tQHzRPcEwpUSVkhXRklwWWtnWGtvQWFPemYySERTQ09QSnhNR1FvaTQ2SkQ0MWwwV0QwTEVhQXVvWXNTU2dDTmJOeWRlS0N3RjhseEZ0NnRzbWktOXJMaXkyd1lMQ0x3IIEC; bili_jct=75df593d3e05cd6698d669ed3231b6ae; DedeUserID=30669100; DedeUserID__ckMd5=10cd8a7b56357a96; sid=6oa6n2a6; buvid_fp=af852e650373b29ee36d157b724195b4; LIVE_BUVID=AUTO6917338218818044; PVID=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ1MDU2NTgsImlhdCI6MTczNDI0NjM5OCwicGx0IjotMX0.OeS0k2aNcDSCv_MgKwkf2asJYk0OqEnqK7WBumc2SHs; bili_ticket_expires=1734505598; bp_video_offset_30669100=1011070451490750464; home_feed_column=4; browser_resolution=1270-1354; bp_t_offset_30669100=1011904955046428672; bsource=search_bing; CURRENT_FNVAL=4048; b_lsid=7410D391E_193D74C2D5A",
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/video/BV1FG4y1Z7po/?spm_id_from=333.337.search-card.all.click&vd_source=69a50ad969074af9e79ad13b34b1a548',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
        }

    def get_w_rid(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_url_1st(self, oid):
        oid = str(oid)
        wts = str(int(time.time()))
        data = 'mode=3&oid=' + str(oid) + '&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts=' + str(wts) + 'ea1db124af3c7062474693fa704f4ff8'

        w_rid = self.get_w_rid(data)
        w_rid = f"&w_rid={w_rid}"
        wts = f"&wts={wts}"
        url_1st = "https://api.bilibili.com/x/v2/reply/wbi/main?oid=" + str(oid) + "&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875" + w_rid + wts

        return url_1st

    def get_url_2nd(self, oid, session_id):
        oid = str(oid)
        session_id = str(session_id)
        wts = str(int(time.time()))
        y = 'mode=3&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A1%2C%5C%22direction%5C%22%3A1%2C%5C%22session_id%5C%22%3A%5C%22' + session_id + '%5C%22%2C%5C%22data%5C%22%3A%7B%7D%7D%22%7D&plat=1&type=1&web_location=1315875&wts=' + wts

        a = 'ea1db124af3c7062474693fa704f4ff8'
        data = y + a
        w_rid = self.get_w_rid(data)
        url_2nd = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=3&pagination_str=%7B%22offset%22:%22%7B%5C%22type%5C%22:1,%5C%22direction%5C%22:1,%5C%22session_id%5C%22:%5C%22' + session_id + '%5C%22,%5C%22data%5C%22:%7B%7D%7D%22%7D&plat=1&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts

        return url_2nd

    def get_aid(self, bv):
        url = f'https://www.bilibili.com/video/{bv}'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        content = html.text
        aid_regx = '"aid":(.*?),"bvid":"{}"'.format(bv)
        aid = re.findall(aid_regx, content)[0]
        return aid

    def get_reply(self, bv, replies_amount):
        bv = str(bv)
        oid = self.get_aid(bv)
        url_1st = self.get_url_1st(oid)
        print(url_1st)
        response = requests.get(url_1st, headers=self.headers)

        data_json = response.json()
        replies = data_json["data"]["replies"]

        session_id = data_json['data']['cursor']['session_id']

        print("session_id：", session_id)

        replies_list = []
        flag = 1
        print('=============================[第1组]=================================')
        for reply in replies:
            content = reply["content"]["message"]
            # print(f"{flag}. {content}") ######################
            replies_list.append(content)  # 这里只添加评论内容本身，不再添加序号等多余信息
            flag += 1
        n = int(replies_amount / 20)
        for i in range(0, n):
            time.sleep(random.uniform(0.4, 0.6))


            print('=============================[第', i + 2, '/', n+1, '组]=================================')
            url_2nd = self.get_url_2nd(oid, session_id)
            print(url_2nd)
            response = requests.get(url_2nd, headers=self.headers)
            data_json_ = response.json()
            replies = data_json_["data"]["replies"]
            session_id = data_json_['data']['cursor']['session_id']
            print(session_id)
            if replies:
                for reply in replies:
                    content = reply["content"]["message"]
                    # print(f"{flag}. {content}") ##############################
                    replies_list.append(content)
                    flag += 1
            else:
                print("获取评论失败,跳过此次爬取")
                pass

        result_dict = {
            "bv号": bv,
            "爬取评论数": replies_amount,
            "所有评论内容": replies_list
        }

        return result_dict


if __name__ == '__main__':
    crawler = CommentScraper()
    bv_list = ['BV1C7qdYbEYU', 'BV1e8B5YPEVm', 'BV1mYySYzEsU']  # 这里替换为你实际要爬取的BV号列表
    for bv in bv_list:
        评论数 = 500
        result = crawler.get_reply(bv, 评论数)
        try:
            # 尝试读取已有的JSON文件内容
            with open("comments_test.json", "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            # 如果文件不存在，初始化一个空列表
            existing_data = []

        existing_data.append(result)

        with open("comments_test.json", "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)