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

        # Login
        bot.login(student['Id'], student['Password'], student['Clg'])

        # Mark Attendance
        bot.mark_attendance()

        # Notify
        logger.info('Done for {}'.format(student['Id']))
        bot.notify_stud(contact=student['Contact'])

    # Terminate after marking all attendance
    bot.close_window()
    logger.success('Successfully terminated at {}'.format(time.asctime()))


# Logs
logger.success('Starting script in test mode at {}'.format(time.asctime()))

scheduled_job()
