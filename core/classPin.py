import os
import pymysql
import pymysql.cursors

from core.app_var import *
from core.app_config import *

class Pin:

    def __init__(self):
        pass

    def updateStateTxt(self, num_pin, value):
        tmpValue = 0
        if (value % 2 != 0):
            tmpValue = 1

        currentPath = os.path.dirname(os.path.realpath(__file__))
        os.system("echo {0} > {1}/state/state_arduino_pin_{2}.txt".format(tmpValue, currentPath, num_pin))

    def recordLog(self, num_pin, value):
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        currentCursor = conn.cursor()
        query = "INSERT INTO log_pin(pin_num, user_id, pin_value) VALUES ('{}', '{}', '{}')".format(num_pin, CURRENT_USER, value)
        currentCursor.execute(query)
        conn.commit()

    def send(self, num_pin, value):
        tmpval = 0
        if (value % 2 != 0):
            tmpval = 1

        self.updateStateTxt(num_pin, value)
        self.recordLog(num_pin, value)
        managerArduino.write(str.encode(str(value)))

    def createTaskStandard(self, initialHour, initialMinute, finalHour, finalMinute):
        currentPath = os.path.dirname(os.path.realpath(__file__))
        pOn = "{0}/task/taskStandardOn.py >> /var/log/a1.log 2>&1".format(currentPath)
        pOff = "{0}/task/taskStandardOff.py >> /var/log/a1.log 2>&1".format(currentPath)

        print("createTaskStandard")

        self.createTaskCron("poon", pOn, initialHour, initialMinute, pOff, finalHour, finalMinute)


    def createTaskeverse(self, initialHour, initialMinute, finalHour, finalMinute):
        currentPath = os.path.dirname(os.path.realpath(__file__))
        pOn = "{0}/task/taskReverseOn.py >> /var/log/a1.log 2>&1".format(currentPath)
        pOff = "{0}/task/taskReverseOff.py >> /var/log/a1.log 2>&1".format(currentPath)

        print("createTaskeverse")

        self.createTaskCron("poon", pOn, initialHour, initialMinute, pOff, finalHour, finalMinute)

    def createTaskCron(self, taskName: str, pathOn: str, hi: int, mi: int, pathOff: str, hf: int, mf: int):
        cronStringOn = '{0} {1} * * * root python3 {2}'.format(mi, hi, pathOn)
        cronStringOff = '{0} {1} * * * root python3 {2}'.format(mf, hf, pathOff)
        fileCronStart = 'tarea_{0}_Start'.format(taskName)
        fileCronEnd = 'tarea_{0}_End'.format(taskName)

        print(cronStringOn)
        print(cronStringOff)

        cronTask = open(r"/etc/cron.d/{0}".format(fileCronStart), 'w+')
        cronTask.write(cronStringOn)
        cronTask.write('\n')
        cronTask.close()
        os.system('sudo chmod -R 777 /etc/cron.d/{0}'.format(fileCronStart))

        cronTask = open(r"/etc/cron.d/{0}".format(fileCronEnd), 'w+')
        cronTask.write(cronStringOff)
        cronTask.write('\n')
        cronTask.close()
        os.system('sudo chmod -R 777 /etc/cron.d/{0}'.format(fileCronEnd))

        os.system('sudo chmod -R 755 /etc/cron.d/{0}'.format(fileCronStart))
        os.system('sudo chmod -R 755 /etc/cron.d/{0}'.format(fileCronEnd))

        os.system('sudo /etc/init.d/cron restart &')

        print("Tarea {} programada para HI: {} - MI: {} - HF: {} - MF: {}".format(pathOn, hi, mi, hf, mf))