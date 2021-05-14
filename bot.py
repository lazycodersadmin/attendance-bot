import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from logger import Logger
from notify import Notify

# Fetching env vars
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
server_ip_deemed = '45.116.207.203'
server_ip_hill = '45.116.207.79'

chrome_options = Options()
chrome_options.binary_location = os.environ.get(
    'GOOGLE_CHROME_BIN')    # For Heroku
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-sh-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--proxy-server="direct://"')
chrome_options.add_argument('--proxy-bypass-list=*')


class Bot:
    def __init__(self):
        self.bot = webdriver.Chrome(
            executable_path=chromedriver_path, chrome_options=chrome_options)
        self.logger = Logger()
        self.notify = Notify()
        self.att_count = 0
        self.marked_count = 0
        self.server_ip = ''

    def login(self, username, password, clg):
        bot = self.bot
        logger = self.logger

        self.server_ip = server_ip_hill if clg == 'hill' else server_ip_deemed
        server_ip = self.server_ip

        logger.info('Opening Moodle')
        bot.get(
            'http://{}/moodle/login/index.php'.format(server_ip))
        bot.implicitly_wait(5)

        username_field = bot.find_element_by_id('username')
        password_field = bot.find_element_by_id('password')

        logger.info('Typing username and password')
        username_field.send_keys(username)
        password_field.send_keys(password)

        logger.info('Logging in {}'.format(username))
        password_field.send_keys(Keys.RETURN)
        bot.implicitly_wait(5)

    def logout(self):
        bot = self.bot
        logger = self.logger
        server_ip = self.server_ip

        logger.info('Logging Out')
        bot.get('http://{}/moodle/login/logout.php'.format(server_ip))
        bot.implicitly_wait(3)
        bot.find_element_by_class_name('btn-primary').click()
        bot.implicitly_wait(3)

    def close_window(self):
        bot = self.bot

        bot.close()

    def mark_present(self, index):
        bot = self.bot
        logger = self.logger
        server_ip = self.server_ip

        if (index != 0):
            bot.get('http://{}/moodle/my/'.format(server_ip))
            bot.implicitly_wait(3)

        # Find event
        eventsList = bot.find_elements_by_class_name('event')
        todaysEvents = list(filter(
            lambda x: 'Today' in x.get_attribute('innerText') and 'Attendance' in x.get_attribute('innerText'), eventsList))
        e = todaysEvents[index]

        # Open Modal and click
        e.find_element_by_tag_name('a').click()
        bot.implicitly_wait(5)
        bot.find_element_by_class_name(
            'modal-footer').find_element_by_tag_name('a').click()
        bot.implicitly_wait(5)

        # Find unmarked attendance
        general_table = bot.find_element_by_class_name('generaltable')
        all_att = general_table.find_elements_by_tag_name('tr')
        unmarked_att = list(
            filter(lambda x: 'Submit' in x.get_attribute('innerText'), all_att))
        if len(unmarked_att) == 0:
            logger.info('Attendance {} already marked'.format(index+1))
            return
        else:
            att = unmarked_att[0]
            # Get to marking page
            att.find_element_by_tag_name('a').click()
            bot.implicitly_wait(5)

            # Find present option
            options = bot.find_elements_by_class_name('form-check-inline')
            present_option = list(
                filter(lambda x: 'Present' in x.get_attribute('innerText'), options))[0]
            present_option.click()

            # Mark present
            submit_btn = bot.find_element_by_id('id_submitbutton')
            submit_btn.click()
            logger.success('Attendance {} marked present'.format(index+1))
            self.marked_count += 1
            bot.implicitly_wait(2)

    def find_count(self):
        bot = self.bot
        logger = self.logger

        logger.info("Finding today's attendance")
        eventsList = bot.find_elements_by_class_name('event')
        todaysEvents = list(filter(
            lambda x: 'Today' in x.get_attribute('innerText') and 'Attendance' in x.get_attribute('innerText'), eventsList))
        logger.success(
            'Found {} attendance for today'.format(len(todaysEvents)))

        return len(todaysEvents)

    def mark_attendance(self):
        bot = self.bot
        logger = self.logger

        att_count = self.find_count()
        self.att_count = att_count

        if (att_count == 0):
            self.logout()
            return

        logger.info('Ready to mark present')
        for i in range(att_count):
            self.mark_present(i)

        self.logout()

    def notify_stud(self, contact):
        logger = self.logger
        notify = self.notify
        marked_count = self.marked_count

        if (marked_count == 0):
            logger.info('Skipping notification by whatsapp')
            return

        message_body = 'Marked {} attendance for today. Keep Hacking. 😁'.format(
            self.att_count)
        notify.send_whatsapp(
            contact=contact, message=message_body)
        logger.info('A notification sent to user at his whatsapp')


if __name__ == '__main__':
    print('Attendance Bot - by guy07')
