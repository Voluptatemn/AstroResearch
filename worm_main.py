from crontab import CronTab

def add_cron_job(command, schedule = '0 * * * *'):
    cron = CronTab(user=True)  
    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()

command = '/Users/qiangangsamwang/opt/anaconda3/bin/python3 YSEScrape.py > /Users/qiangangsamwang/Documents/GitHub/AstroResearch/log_file.log 2>&1'
add_cron_job(command=command)


