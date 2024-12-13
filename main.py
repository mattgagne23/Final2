from todo_list import *

def main():
    '''
    This will be used to initialize window and run program
    '''

    application = QApplication([])
    window = TaskList()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()