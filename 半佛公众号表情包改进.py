import requests
import re
import os

url_list = ['https://mp.weixin.qq.com/s?__biz=MzI5MTE2NDI2OQ==&mid=2247487015&idx=1&sn=a02264e8f31a8d2882f56085e16a808c&scene=19#wechat_redirect',
'https://mp.weixin.qq.com/s?__biz=MzI5MTE2NDI2OQ==&mid=2247486923&idx=1&sn=c21cea3bed45d88ae0b5a294023f49ad&scene=19#wechat_redirect',
'https://mp.weixin.qq.com/s?__biz=MzI5MTE2NDI2OQ==&mid=2247486767&idx=1&sn=19a274dd5ef3c3637c0489d65ddb613a&scene=19#wechat_redirect']







def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
        return url_list


def mkdir():
    isExists = os.path.exists(r'./banfo')
    if not isExists:
        print('创建目录')
        os.makedirs(r'./banfo')  # 创建目录
        os.chdir(r'./banfo')  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在，即将保存！')
        return False


def download(filename, url):
    try:
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get(url, timeout=30).content)
                print('成功下载图片：', filename)
            except requests.exceptions.SSLError:
                f.write(requests.get(url, verify=False, timeout=30).content)
                print('成功下载图片：', filename)
    except FileNotFoundError:
        print('下载失败，非表情包，直接忽略：', filename)
    except TimeoutError:
        print('下载超时：', filename)
    except Exception:
        print('下载失败：', filename)

if __name__ == '__main__':
    for texturl in url_list:
        url_list = get_urls(texturl)
        mkdir()
        for pic_url in url_list:
            filename = r'./banfo/' + pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]  # 图片的路径
            download(filename, pic_url)


