'''
Author: dt_4541218930 abcstorms@163.com
Date: 2025-01-13 12:56:33
LastEditors: dt_4541218930 abcstorms@163.com
LastEditTime: 2025-01-14 09:27:02
FilePath: \changedetection.io\changedetectionio\dingtalkrobotnotification.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import hashlib
import hmac
import base64
import urllib.parse
import time
import requests
import json
from urllib.parse import urlparse, parse_qs

def notify_dingtalk(msg, webhook):
    if webhook.startswith("discord://"):
        webhook = webhook.replace("discord://", "")
    parsed_url = urlparse(webhook)
    query_dict = parse_qs(parsed_url.query)
    timestamp = str(round(time.time() * 1000))
    if "secret" in query_dict:
        webhook = webhook.replace("&secret=" + query_dict["secret"][0], "")
        secret = query_dict["secret"][0]  # 这是你的secret值
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # 更新webhook URL 包含签名信息
        webhook_with_sign = f"{webhook}&timestamp={timestamp}&sign={sign}"
    else:
        webhook_with_sign = f"{webhook}&timestamp={timestamp}"
    print(webhook_with_sign)

    # 构建消息体
    message = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }

    # 发送POST请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_with_sign, data=json.dumps(message), headers=headers)

    # 检查响应
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message, status code: {response.status_code}")
        print(response.text)