from PyQt6.QtWidgets import *
from gui import *
import os.path
import csv
import datetime

class TaskList(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_check()
        self.display_list()
        self.retrieve_datetime()
        '''
        Initializing function that creates list object along with date and time being accessed or created.
        Not sure if this will be multi-user or single user.
        '''
        self.submit_button.clicked.connect(lambda : self.submit_task())

    def file_check(self):
        path = './list.csv'

        if os.path.isfile(path) == False:
            with open('list.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Task', 'Priority', 'Date', 'Time'])

    def display_list(self):
        with open('list.csv', 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                format_row = f'{row[0]: <40}{row[1]: <15}{row[2]: <15}{row[3]: <10}'
                self.listWidget.addItem(format_row)

    def submit_task(self):
        priority = ''
        date = self.dateEdit.date().toString('MM-dd-yyyy')
        time = self.timeEdit.time().toString('HH:mm:ss')

        if self.radio_low.isChecked():
            priority = 'Low'
        elif self.radio_medium.isChecked():
            priority = 'Medium'
        elif self.radio_high.isChecked():
            priority = 'High'
        else:
            self.error_label.setText('You must choose a priority!')

        try:
            task = self.input_edit.toPlainText()
            if task == '':
                raise ValueError
            if priority == '':
                raise TypeError
        except ValueError:
            self.error_label.setText('You must enter a task to submit!')
        except TypeError:
            self.error_label.setText('You must choose a priority!')
        except Exception as e:
            print(f'Unexpected error: {e}')
        else:
            with open('list.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([task, priority, date, time])
            self.listWidget.addItem(f'{task: <40}{priority: <15}{date: <15}{time: <10}')
            self.input_edit.setText('')

    def retrieve_datetime(self):
        current_time = datetime.datetime.now()
        formatted_time = f'{current_time.month}/{current_time.day}/{current_time.year} {current_time.hour}:{current_time.minute}'
        self.date_time_label.setText(f'Today is: {formatted_time}')