import time
from apscheduler.schedulers.blocking import BlockingScheduler

from bot import Bot
from logger import Logger
from api import Api

# Script Schedule config
days = 'mon-sat'
hour = '09-17'
minute = '00'

# Instatiating Logger
logger = Logger()

# Instantiating Scheduler
sched = BlockingScheduler(timezone="Asia/Kolkata")

# Job to be run on scheduled config


@sched.scheduled_job('cron', day_of_week=days, hour=hour, minute=int(minute))
def scheduled_job():
    logger.info('Starting execution at {}'.format(time.asctime()))

    bot = Bot()
    api = Api()

    students = api.get_students()

    for student in students:

        try:
            # Login
            bot.login(student)
        except:
            logger.error('An error occured while trying to login. Skipping...')
            continue

        try:
            # Mark Attendance
            bot.mark_attendance()
        except:
            logger.error(
                'An error occured while trying to mark attendance. Skipping...')
            continue

        # Notify
        logger.info('Done for {}({})\n'.format(student['Name'], student['Id']))
        try:
            bot.notify_stud(contact=student['Contact'])
        except KeyError:
            logger.error('No contact found to notify person. Skipping...')
        except:
            logger.error('An error occured notifying user')

    # Terminate after marking all attendance
    bot.close_window()
    logger.success('Successfully terminated at {}'.format(time.asctime()))


# Logs
logger.success('Script deployed successfully at {}'.format(time.asctime()))
logger.info('Configuration : day: {}, hour: {}, minute: {}'.format(
    days, hour, minute))

# Starting the scheduler
sched.start()
