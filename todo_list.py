from PyQt6.QtWidgets import *
from gui import *
import os.path
import csv
import datetime

class TaskList(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        '''
        Initializes TaskList and calls UI. Uses functions to check for existence of task list file, displays the list,
        and retrieves and displays current date / time.
        '''
        self.setupUi(self)
        self.file_check()
        self.display_list()
        self.retrieve_datetime()

        self.submit_button.clicked.connect(lambda : self.submit_task())

    def file_check(self):
        '''
        This function checks for the existence of a to do list file. If it exists, no action.
        If not, it creates the file to be used to store task list data later on.
        :param path: this is used to check for existence of file in file path.
        '''
        path = './list.csv'

        if os.path.isfile(path) == False:
            with open('list.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Task', 'Priority', 'Date', 'Time'])

    def display_list(self):
        '''
        This function displays the existing data in the list.csv file to the screen, pulling
        that information as a record.
        '''
        with open('list.csv', 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                format_row = f'{row[0]: <40}{row[1]: <15}{row[2]: <15}{row[3]: <10}'
                self.listWidget.addItem(format_row)

    def submit_task(self):
        '''
        This function is used when the submit button is clicked. It pulls the data from the input box, priority
        radio buttons, and date and time widgets for recording in csv file and also displays on the to do list screen.
        :param priority: this is the value stored that is determined by the priority radio button selected.
        :param date: this is the formatted date pulled from the dateEdit widget.
        :param time: this is the formatted time pulled from the timeEdit widget.
        '''
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
        '''
        This function pulls the date and time when application is launched so the user knows the time.
        :param current_time: this is the exact date and time as recorded by the system when app is launched.
        :param formatted_time: this uses the data from curren_time but formats it in a user-friendly way.
        '''
        current_time = datetime.datetime.now()
        formatted_time = f'{current_time.month}/{current_time.day}/{current_time.year} {current_time.hour}:{current_time.minute}'
        self.date_time_label.setText(f'Today is: {formatted_time}')