from apscheduler.schedulers.background import BackgroundScheduler
from home.task import Taskone
scheduler = BackgroundScheduler()
scheduler.add_job(Taskone, 'interval', seconds=1)
scheduler.start()
