import threading
import requests

class Download:
    def download(self, url,callback_world_count):
        print(f"线程{threading.get_ident()}开始下载:{url}")
        response = requests.get(url)
        response.encoding = 'utf-8'
        callback_world_count(url,response.text)#调用回调函数
    
    def start_download(self, url, callback_world_count):
        thread = threading.Thread(target=self.download, args=(url, callback_world_count))
        thread.start()

def world_count(url,result):
    content = result
    count = len(content.split())
    print(f"URL: {url}:{len(result)}-> Word Count: {count}")


def main():
    url = "https://www.baidu.com"
    download = Download()
    download.start_download(url, world_count)