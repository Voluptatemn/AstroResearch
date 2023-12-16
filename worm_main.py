from crontab import CronTab
cron = CronTab(user=True)
job = cron.new(command='echo hello_world')
cron.write() 

