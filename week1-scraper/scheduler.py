# -*- coding: utf-8 -*-
import schedule 
import time
import scraper_v1 

def job():
    print("开始跑任务.....")
    scraper_v1.run()
    print("任务完成")

schedule.every(10).minutes.do(job)

job() #在这里直接启动是因为上面设置了每10分钟启动，也就是10分钟之后启动需要等，在这里直接启动最快

print("调度器启动，等待下次执行...")
while True:
    schedule.run_pending()
    time.sleep(30)
