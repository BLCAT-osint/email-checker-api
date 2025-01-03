from colorama import Fore, init
from hashlib import md5
from requests import get, exceptions
import json

class EmailChecker:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    # [保持原有的所有检查方法不变]
    # check_github_email, check_spotify_email 等方法保持不变...

def check_email(email):
    """
    插件入口函数
    :param email: 要检查的邮箱地址
    :return: 包含查询结果的字典
    """
    checker = EmailChecker()
    results = {
        'social_media': [],
        'data_breaches': []
    }
    
    # 检查社交媒体账号
    checks = [
        checker.check_github_email,
        checker.check_spotify_email,
        checker.check_twitter_email,
        checker.check_gravatar_email,
        checker.check_pinterest_email,
        checker.check_chess_email,
        checker.check_duolingo_email
    ]
    
    for check in checks:
        result = check(email)
        if result:
            results['social_media'].append(result)
    
    # 检查数据泄露
    breaches = checker.hudsonrock_api(email)
    if breaches:
        results['data_breaches'].extend(breaches)
        
    pastebin = checker.check_pastebin_dumps(email)
    if pastebin:
        results['data_breaches'].append(pastebin)
    
    return results 