from crontab import CronTab
from YSEScrape import YSE_worm

def add_cron_job(command, user = "Thacher", schedule = '0 * * * *'):
    cron = CronTab(user)  # Specify the username if necessary

    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()

yse_worm = YSE_worm()
add_cron_job(command = f'python -c "from YSEScrape import YSE_worm; YSE_worm.scrape()"')


