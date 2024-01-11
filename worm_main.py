from crontab import CronTab
from YSEScrape import YSE_worm

def add_cron_job(command, user = "Thacher", schedule = '0 * * * *'):
    cron = CronTab(user)  # Specify the username if necessary

    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()

command = '0 * * * * /path/to/your/function/script.sh > logfile.log 2>&1'


