import requests

res = requests.get('http://baidu.com', proxies=dict(http='http://127.0.0.1:9999'))

print(res.text)
