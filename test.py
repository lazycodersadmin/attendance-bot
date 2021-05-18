from notify import Notify
import time

from bot import Bot
from logger import Logger
from api import Api

# Instatiating Logger
logger = Logger()


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
        logger.info('Done for {}({})'.format(student['Name'], student['Id']))
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
logger.success('Starting script in test mode at {}'.format(time.asctime()))

scheduled_job()
