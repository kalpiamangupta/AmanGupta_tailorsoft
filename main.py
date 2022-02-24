from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
from database import DbConnection as db

class Main(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\main.ui', self)
        self.setFixedSize(333, 389)
        self.con = db.createConnection()
        self.cursor = self.con.cursor()
        self.btncreate.clicked.connect(self.add)
        self.btnclear.clicked.connect(self.reset)
        self.reset()

    def reset(self):
        self.fnametxt.setText('')
        self.lnametxt.setText('')
        self.agetxt.setText('')
        self.locationtxt.setText('')
        self.emailtxt.setText('')

    def add(self):
        self.fname = self.fnametxt.text()
        self.lname = self.lnametxt.text()
        self.age = self.agetxt.text()
        self.location = self.locationtxt.text()
        self.email = self.emailtxt.text()

        strsql = 'select max(empid) from empdetails'
        self.cursor.execute(strsql)
        self.rowdata = self.cursor.fetchone()
        rowstatus = self.cursor.rowcount

        fn = len(self.fname.strip())
        ln = len(self.lname.strip())
        ag = len(self.age.strip())
        lc = len(self.location.strip())
        em = len(self.email.strip())
        if fn == 0 or ln == 0 or ag == 0 or lc == 0 or em == 0:
            self.showDialog('Please fill all the details.')
        elif rowstatus <= 0:
            self.empid = 1
        else:
            self.empid = self.rowdata[0] + 1
            print(self.empid)
            strinsert = 'insert into empdetails(empid, first_name, last_name, age, location, email) values (%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(strinsert,
                                (int(self.empid), self.fname, self.lname, int(self.age), self.location, self.email))
            self.con.commit()
            self.showDialog('Data inserted successfully.')
            self.reset()

    def showDialog(self, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Details')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()