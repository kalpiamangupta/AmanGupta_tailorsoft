from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from database import DbConnection as db
import sys

class Edit(QFrame):

    def __init__(self):
        super().__init__()
        loadUi('gui\Edit.ui', self)
        # self.setFixedSize(465, 305)
        self.con = db.createConnection()
        self.cursor = self.con.cursor()
        self.cmb.setPlaceholderText("Select Employee ID")
        self.radioButtonupdate.setChecked(True)
        self.check()
        self.radioButtonupdate.toggled.connect(self.check)
        self.radioButtondelete.toggled.connect(self.check)
        self.populateCombo()
        self.btnupdate.clicked.connect(self.update)
        self.btndelete.clicked.connect(self.delete)
        self.cmb.currentTextChanged.connect(self.fetchData)


    def check(self):
        if self.radioButtonupdate.isChecked():
            self.btndelete.setVisible(False)
            self.btnupdate.setVisible(True)
            self.fnametxt.setEnabled(True)
            self.lnametxt.setEnabled(True)
            self.agetxt.setEnabled(True)
            self.locationtxt.setEnabled(True)
            self.emailtxt.setEnabled(True)
        elif self.radioButtondelete.isChecked():
            self.btnupdate.setVisible(False)
            self.btndelete.setVisible(True)
            self.fnametxt.setEnabled(False)
            self.lnametxt.setEnabled(False)
            self.agetxt.setEnabled(False)
            self.locationtxt.setEnabled(False)
            self.emailtxt.setEnabled(False)

    def populateCombo(self):
        strsql = 'select empid from empdetails'
        self.cursor.execute(strsql)
        self.dataset = self.cursor.fetchall()
        for data in self.dataset:
            self.cmb.addItem(str(data[0]))

    def fetchData(self):
        self.eid=self.cmb.currentText()
        query1='select empid, first_name, last_name,age,location,email from empdetails where empid=%s'
        self.cursor.execute(query1, (int(self.eid),))
        self.data=self.cursor.fetchone()
        self.fnametxt.setText(self.data[1])
        self.lnametxt.setText(self.data[2])
        self.agetxt.setText(str(self.data[3]))
        self.locationtxt.setText(self.data[4])
        self.emailtxt.setText(self.data[5])

    def update(self):
        self.fname=self.fnametxt.text()
        self.lname=self.lnametxt.text()
        self.age=self.agetxt.text()
        self.location=self.locationtxt.text()
        self.email=self.emailtxt.text()

        if self.fname == '' or self.lname == '' or self.age == '' or self.location == '' or self.email == '' or self.cmb.currentIndex()==-1:
            self.showDialog("Please enter details after selecting employee id")
        else:
            query2 = 'update empdetails set first_name=%s, last_name=%s, age=%s, location=%s, email=%s where empid=%s'
            self.cursor.execute(query2,
                                (self.fname, self.lname, int(self.age), self.location, self.email, self.eid,))
            self.con.commit()
            self.showDialog("Data Updated!!")
            self.fnametxt.setText('')
            self.lnametxt.setText('')
            self.agetxt.setText('')
            self.locationtxt.setText('')
            self.emailtxt.setText('')

    def delete(self):
        if self.cmb.currentIndex()==-1:
            self.showDialog('Please select employee ID')
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle('Deletion')
            msg.setText('Do you wish to delete record??')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            btnstatus = msg.exec_()
            if btnstatus == QMessageBox.Yes:
                strdelete = 'delete from empdetails where empid=%s'
                self.cursor.execute(strdelete, (self.eid,))
                self.con.commit()
                self.showDialog('Data deleted Successfully')
                self.fnametxt.setText('')
                self.lnametxt.setText('')
                self.agetxt.setText('')
                self.locationtxt.setText('')
                self.emailtxt.setText('')

    def showDialog(self, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = Edit()
    edit.show()
    app.exec_()