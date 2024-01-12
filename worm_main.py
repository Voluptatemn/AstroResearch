from crontab import CronTab
from YSEScrape import YSE_worm

def add_cron_job(command, schedule = '0 * * * *'):
    cron = CronTab(user=True)  
    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()

command = '0 * * * * YSEScrape.py > logfile.log 2>&1'
add_cron_job(command=command)


