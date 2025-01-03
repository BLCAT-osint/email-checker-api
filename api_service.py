from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from main import EmailChecker

app = FastAPI(
    title="Email Account Checker API",
    description="检查邮箱在各大社交平台的注册情况和数据泄露信息",
    version="1.0.0"
)

class EmailRequest(BaseModel):
    email: str

class EmailResponse(BaseModel):
    social_media: List[str]
    data_breaches: List[str]

@app.post("/check_email", response_model=EmailResponse)
async def check_email(request: EmailRequest):
    try:
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
            result = check(request.email)
            if result:
                results['social_media'].append(result)
        
        # 检查数据泄露
        breaches = checker.hudsonrock_api(request.email)
        if breaches:
            results['data_breaches'].extend(breaches)
            
        pastebin = checker.check_pastebin_dumps(request.email)
        if pastebin:
            results['data_breaches'].append(pastebin)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 