from apscheduler.schedulers.background import BackgroundScheduler
from catalog_parser import parse_catalog, update_database

def scheduled_job():
    teas = parse_catalog()
    update_database(teas)

def schedule_catalog_update():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', hours=24)
    scheduler.start() 