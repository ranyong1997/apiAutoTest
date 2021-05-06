import requests
import json
from tools.hooks import decrypt, headers

url = "http://soloop-test.wanyol.com/common/setting/getLehuaCategory"
aeskey = "kJrOctnrtdj0obkMkdDMfVptvJYEi9BgiZP/m5T5n84="
r = requests.get(url=url, headers=headers())
result = r.text
print("数据--->" + result)
s = r.json()
s = json.loads(result)
datas = s["data"]
data = decrypt(aeskey, datas)
print("解密--->" + data)
