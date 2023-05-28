# TZone Oracle
Script to scrape [Korean site](https://gall.dcinside.com/mgallery/board/lists?id=diablo2resurrected&s_type=search_subject_memo&s_keyword=.EB.8B.A4.EC.9D.8C.20.ED.85.8C.EB.9F.AC.EC.A1.B4) which has a poster that announces next Terror Zone locations for D2R online.

## Requirements
- Python 3.8+
- Scrapy
- discord-webhook
- googletrans==3.1.0a0 (use this version specially)

```
pip install scrapy
pip install discord-webhook
pip install googletrans==3.1.0a0
```

## Configure
Add your discord channel webhook url on line 13 in post_spider.py
```
webhook_url = '<replace with your discord channel webhook>'
```

## How to run
- After installing requirements and configuring webhook just run the **runner.bat**

To automate checking you can setup scheduled tasks, cron, however you want, it's up to you really.

## Disclaimer
This script only works as long as the source korean site is online and that link is still active. This does not interact with blizzard or the D2R game in any capacity.
