#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QLabel,QLineEdit,QPushButton,QLineEdit,QMessageBox,QVBoxLayout,QGridLayout,QFormLayout,\
                            QMenuBar,QMenu,QAction,QToolBar,QFileDialog,QDialog,QSpinBox,QComboBox
from PyQt5.QtGui import QIcon,QPixmap,QFont,QTextDocument,QTextCursor,QTextBlockFormat,QTextCharFormat,QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog
from PyQt5 import sip
import random,datetime,os
from gene_mix_express import gene_express

dayRecordFilePath='day_record.txt'
numRecordFilePath='num_record.txt'
wrongWorkFilePath='wrong_work.txt'

def getLastDay():
    if not os.path.exists(dayRecordFilePath):
        return None
    with open(dayRecordFilePath,"r") as dayRecordFile:
        lines=dayRecordFile.readlines()
    if len(lines):
        line=lines[-1]        
        L=line.split()[0].split("-")
        return datetime.date(int(L[0]),int(L[1]),int(L[2]))
    else:
        return None

def getLastData():

    if not os.path.exists(dayRecordFilePath):
        return (0,0,0)

    with open(dayRecordFilePath,"r") as dayRecordFile:
        lines=dayRecordFile.readlines()

    if len(lines):
        line=lines[-1]
        L=line.split()
        return int(L[1]),int(L[2]),int(L[3])
    else:
        return (0,0,0)    


def fileAddLine(filePath,line):

    with open(filePath,"a") as file:
        file.write(line+"\n")

def replaceLastLine(filePath,line):

    with open(filePath,"r") as file:
        lines=file.readlines()
        lines[-1]=line+"\n"
    with open(filePath,"w") as file:
        file.write("".join(lines))


class ConfigWindow(QDialog):

    '''
    要做弹出窗口，用QWidget是不行的
    QDialog可以
    '''

    def __init__(self,parent=None):
        super().__init__(parent)
        self.questionNum=30
        #self.minNum=None
        self.maxNum=None
        self.max_mix = 5
        self.testMethod=0
        self.initUI()

    def initUI(self):

        

        self.lb0=QLabel("测试模式",self)
        self.lb0.setAlignment(Qt.AlignCenter)

        self.lb1=QLabel("测试题数量",self)
        self.lb1.setAlignment(Qt.AlignCenter)

        self.lb3=QLabel("数值范围上限",self)
        self.lb3.setAlignment(Qt.AlignCenter)
        
        self.cb=QComboBox()
        self.cb.addItems(["练习模式","考试模式"])

        self.sb=QSpinBox()        
        self.sb.setRange(1,999)
        self.sb.setValue(30)
        
        #self.le1.setPlaceholderText("输入整数")
        self.le2=QLineEdit()
        self.le2.setPlaceholderText("输入整数")        

        aIntValidator=QIntValidator()

        #self.le1.setValidator(aIntValidator)
        self.le2.setValidator(aIntValidator)


        self.btn=QPushButton("结束设定，返回主窗口",self)
        self.btn.clicked.connect(self.endConfig)
        
    

        layout=QFormLayout(self)
        layout.addRow(self.lb0,self.cb)
        layout.addRow(self.lb1,self.sb)
        #layout.addRow(self.lb2,self.le1)
        layout.addRow(self.lb3,self.le2)
        layout.addRow(self.btn)


        self.cb.currentIndexChanged.connect(self.setTestStype)        
        self.sb.valueChanged.connect(self.setQuestionNum)
        #self.le1.editingFinished.connect(self.setMinNum)
        self.le2.editingFinished.connect(self.setMaxNum)

    def setTestStype(self,i):

        self.testMethod=i

    def setQuestionNum(self,i):
        
        self.questionNum=i

    #def setMinNum(self):

        #sender=self.sender()
        #self.minNum=int(sender.text())

    def setMaxNum(self):

        sender=self.sender()
        self.maxNum=int(sender.text())

    def endConfig(self):

        #if self.questionNum==None or self.maxNum==None:   # or self.maxNum==None:
            #QMessageBox.about(self,"警告","设定不完整，请完整设定!")
        if self.maxNum==None or self.maxNum<0 or self.maxNum>999:
            self.le2.clear()
            QMessageBox.about(self,"警告","上限要在0-999范围！")
            
        #elif self.minNum>self.maxNum:
            #self.le1.clear()
            #self.le2.clear()
            #QMessageBox.about(self,"警告","设定的上限比下限小，不合法！")
        else:
            self.parent().questionNum=self.questionNum
            #self.parent().minNum=self.minNum
            self.parent().maxNum=self.maxNum
            self.parent().testMethod=self.testMethod
            self.close()

    
        
        
        

class Window(QMainWindow):

    def __init__(self,parent=None):

        super().__init__(parent)

        self.questionNum=70
        
        #testType:出题类型
        # 0: 100以内加减法及连加减
        self.testType=0
        self.testMethod=0
        self.maxNum=100
        self.minNum=0
        self.max_mix = 5
        self.isInTest=False
        self.initUI()

    def initUI(self):


        self.menuBar=self.menuBar()
        self.file=self.menuBar.addMenu("文件")
        self.save=self.file.addAction(QIcon("icons\\save file.ico"),"保存")
        self.print=self.file.addAction(QIcon("icons\\Print File.ico"),"打印")
        self.printPreview=self.file.addAction(QIcon("icons\\Print Priew.ico"),"打印预览")
        self.printToPdf=self.file.addAction(QIcon("icons\\File Export.ico"),"存pdf")
        self.config=self.menuBar.addAction("设定")
        self.tConfig=QAction(QIcon("icons\\Advanced.ico"),"设定",self)

        self.toolBar=self.addToolBar("工具")
        for qa in (self.save,self.print,self.printPreview,self.printToPdf,self.tConfig):
            self.toolBar.addAction(qa)


        self.save.triggered.connect(self.saveFunc)
        self.print.triggered.connect(self.printFunc)
        self.printPreview.triggered.connect(self.printPreviewFunc)
        self.printToPdf.triggered.connect(self.printToPdfFunc)
        self.config.triggered.connect(self.configFunc)
        self.tConfig.triggered.connect(self.configFunc)

        widget=QWidget()
        

        self.btn1=QPushButton("加减法练习",widget)
        self.btn1.resize(100,40)
        self.btn1.clicked.connect(lambda:self.startTest(0))
        
        self.btn2=QPushButton("乘法表练习",widget)
        self.btn2.resize(100,40)
        self.btn2.clicked.connect(lambda:self.startTest(1))
        
        self.btn3 = QPushButton("多位数乘法",widget)
        self.btn3.resize(100,40)
        self.btn3.clicked.connect(lambda:self.startTest(2))
        
        self.btn4 = QPushButton("多位数除法",widget)
        self.btn4.resize(100,40)
        self.btn4.clicked.connect(lambda:self.startTest(3))
        
        self.btn5 = QPushButton("四则混合",widget)
        self.btn5.resize(100,40)
        self.btn5.clicked.connect(lambda:self.startTest(4))
        

        width=600
        height=800
        self.btn1.move((width-100)//2,(height-40)//6)
        self.btn2.move((width-100)//2,2*(height-40)//6)
        self.btn3.move((width-100)//2,3*(height-40)//6)
        self.btn4.move((width-100)//2,4*(height-40)//6)        
        self.btn5.move((width-100)//2,5*(height-40)//6)
        self.setCentralWidget(widget)

        

        self.setWindowIcon(QIcon("icons\\title.jpg"))      
        self.setGeometry(0,0,width,height)
        self.show()

    def startTest(self,testType):

        lastDay=getLastDay()
        today=datetime.date.today()
        #print(lastDay,today)
        if lastDay is not None:
            dtDay=(today-lastDay).days
            #print(dtDay)
            if dtDay>1:
                #print("不应该哦，已经"+str(dtDay-1)+"天没有做数学作业了！")
                QMessageBox.about(self,"严重警告","不应该哦，已经"+str(dtDay-1)+"天没有做数学作业了！")
            elif dtDay==0:
                reply=QMessageBox.information(self,"选择","今天已经做过作业，是否继续做作业?",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                #print(reply)
                if reply==QMessageBox.No:
                    QApplication.instance().quit()
                    
        widget=self.centralWidget()
        if widget is not None:
            widget.deleteLater()
            
        widget=QWidget()
        self.setCentralWidget(widget)
        
        
        self.isMakeUp=False
        self.isInTest=True
        self.errorQuestionNum=0
        self.errorTimes=0
        
        self.qlb=QLabel(widget)
        self.qle=QLineEdit(widget)
        if self.questionNum==1:
            self.qbtn=QPushButton("完成",widget)
        else:
            self.qbtn=QPushButton("下一题",widget)
        if testType != 4:
            self.qlb.setFont(QFont("SanFrancisco",36))
            self.qle.setFont(QFont("SanFrancisco",36))
            self.qbtn.setFont(QFont("黑体",24))
        else:
            self.qlb.setFont(QFont("SanFrancisco",18))
            self.qle.setFont(QFont("SanFrancisco",18))
            self.qbtn.setFont(QFont("黑体",12))
        self.qlb.resize(400,80)
        self.qle.resize(160,80)
        self.qbtn.resize(160,80)
        self.qlb.move(20,200)
        self.qle.move(430,200)
        self.qbtn.move(430,500)
        self.qlb.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.qle.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        
        self.testType=testType
        
        self.quesList=[]
        self.ansList=[]
        self.isErrorInQues=[False for i in range(self.questionNum)]
        for i in range(self.questionNum):
            self.generateAQuestion()
        
        self.currentQuesIdx=0
        self.errorTimes=0
        self.qlb.setText(self.quesList[self.currentQuesIdx])
        self.qbtn.clicked.connect(self.checkAns)
        
    def checkAns(self):
        
        '''
        print(self.qle.text(),self.ansList[self.currentQuesIdx])
        print(type(self.qle.text()),type(self.ansList[self.currentQuesIdx]))
        print(len(self.qle.text()),len(self.ansList[self.currentQuesIdx]))
        print(self.qle.text()==self.ansList[self.currentQuesIdx])
        print(self.currentQuesIdx)
        '''
        myAns=self.qle.text()
        if myAns!=self.ansList[self.currentQuesIdx]:
            self.errorTimes+=1
            fileAddLine(wrongWorkFilePath,self.qlb.text()+str(myAns))
            self.isErrorInQues[self.currentQuesIdx]=True
            QMessageBox.about(self,"错误！","计算错误，请重新计算!")
            if self.testType != 4:
                self.qlb.setFont(QFont("SanFrancisco",36,QFont.Bold))
            self.qlb.setStyleSheet("color:red;")
        else:            
            self.currentQuesIdx+=1
            if self.testType != 4:
                self.qlb.setFont(QFont("SanFrancisco",36))
            self.qlb.setStyleSheet("color:black;")
            if self.currentQuesIdx==self.questionNum-1:
                self.qbtn.setText("完成")
                self.qlb.setText(self.quesList[self.currentQuesIdx])
                self.qle.clear()
            elif self.currentQuesIdx==self.questionNum:
                self.endTest()
            else:
                self.qlb.setText(self.quesList[self.currentQuesIdx])
                self.qle.clear()
        
         
    
    
    def generateAQuestion(self):

        if self.testType==0:


            #这一大段是得到题目
            nStep=random.randint(1,1)
            signList=["+","-"]
            if nStep==1:
                while True:
                    sign1=random.choice(signList)
                    a=random.randint(self.minNum,self.maxNum)
                    b=random.randint(self.minNum,self.maxNum)
                    res=eval("a"+sign1+"b")
                    if res<=self.maxNum and res>=self.minNum:
                        break
                text=str(a)+sign1+str(b)+"="
                #print(text)
            elif nStep==2:
                while True:
                    sign1,sign2=random.choices(signList,k=2)
                    a=random.randint(self.minNum,self.maxNum)
                    b=random.randint(self.minNum,self.maxNum)
                    c=random.randint(self.minNum,self.maxNum)
                    res1=eval("a"+sign1+"b")
                    res2=eval("a"+sign1+"b"+sign2+"c")
                    if res1<=self.maxNum and res1>=self.minNum and res2<=self.maxNum and res2>=self.minNum:
                        break
                res=res2
                text=str(a)+sign1+str(b)+sign2+str(c)+"="
                if len(self.quesList)>1 and text==self.quesList[-1]:
                    self.generateAQuestion()
                #print(text)

        elif self.testType==1:
            
            n1=random.randint(1,9)
            n2=random.randint(1,9)
            text="{0}×{1}=".format(n1,n2)
            res=n1*n2
            if len(self.quesList)>1:
                pn1,pn2=self.quesList[-1][:-1].split("×")
                pn1=int(pn1)
                pn2=int(pn2)
                if set((n1,n2))==set((pn1,pn2)):
                    self.generateAQuestion()
                    
        elif self.testType==2:
            n1 = random.randint(10, 999)
            n2 = random.randint(10, 999)
            for m in [1, 10]:
                if random.randint(0, 9) < 2 and n1 > 10 * m:
                    n1 = n1 // (m * 10) * 10 * m + n1 % m
            for m in [1, 10]:
                if random.randint(0, 9) < 2 and n2 > 10 * m:
                    n2 = n2 // (m * 10) * 10 * m + n2 % m
            text="{0}×{1}=".format(n1,n2)
            res=n1*n2
            if len(self.quesList)>1:
                pn1,pn2=self.quesList[-1][:-1].split("×")
                pn1=int(pn1)
                pn2=int(pn2)
                if set((n1,n2))==set((pn1,pn2)):
                    self.generateAQuestion()  
        
        elif self.testType==3:            
            n1 = random.randint(100, 9999)
            n2 = random.randint(10, n1)
            if random.randint(0, 9) < 9 and n1 // n2 < 10:
                n2 = n2 // 10
            for m in [1, 10, 100]:
                if random.randint(0, 9) < 2 and n1 > 10 * m:
                    n1 = n1 // (m * 10) * 10 * m + n1 % m
            for m in [1, 10, 100]:
                if random.randint(0, 9) < 2 and n2 > 10 * m:
                    n2 = n2 // (m * 10) * 10 * m + n2 % m
            text="{0}÷{1}=".format(n1,n2)
            if n1 % n2 == 0:
                res = n1 // n2
            else:
                res=f"{n1 // n2} {n1%n2}"
            if len(self.quesList)>1:
                pn1,pn2=self.quesList[-1][:-1].split("÷")
                pn1=int(pn1)
                pn2=int(pn2)
                if set((n1,n2))==set((pn1,pn2)):
                    self.generateAQuestion()
        elif self.testType == 4:
            print(self.testType)
            num_op = random.randint(2, self.max_mix)
            text, res = gene_express(num_op)
            
        else:
            raise NotImplementedError("加减法和乘法表之外的出题方式尚未实现")
            
            
        self.quesList.append(text)
        self.ansList.append(str(res))

    '''
    def showQuestions(self):


        widget=self.centralWidget()
        if widget is not None:
            widget.deleteLater()
    

        widget=QWidget()
        self.setCentralWidget(widget)


        layout=QGridLayout()

        
        for i in range(len(self.lbList)):
            m=i//2
            n=i-2*m
            if self.isMakeUp:
                self.lbList[i].setFont(QFont("SanFrancisco",18,QFont.Bold))
                self.lbList[i].setStyleSheet("color:red;")
            else:
                self.lbList[i].setFont(QFont("SanFrancisco",18))
            layout.addWidget(self.lbList[i],m,n*4,1,3)
            layout.addWidget(self.leList[i],m,n*4+3,1,1)

        btn=QPushButton("提交答案")
        btn.setFont(QFont("宋体",18,QFont.Bold))        
        btn.clicked.connect(self.checkAndMakeUp)
        layout.addWidget(btn,(self.questionNum+1)//2,5,1,2)       
            

        widget.setLayout(layout)


    def checkAndMakeUp(self):

        ansList=[]
        for le in self.leList:
            text=le.text()
            try:
                n=int(text)
            except:
                if text=="":
                    n=None
                else:
                    n="nan"
            finally:
                ansList.append(n)
        noneNum=ansList.count(None)
        if noneNum==len(self.lbList):
            QMessageBox.about(self,"警告","未给出任何答案!")
            return

        

        errorLbList=[]
        errorLeList=[]
        errorStList=[]
        for i in range(len(self.leList)):
            
            
            realAns=eval(self.lbList[i].text()[:-1])
            if ansList[i]==None or ansList[i]=="nan" or realAns!=ansList[i]:
                errorLbList.append(self.lbList[i])
                errorLeList.append(self.leList[i])
                if isinstance(ansList[i],int):

                    self.errorTimes+=1
                    fileAddLine(wrongWorkFilePath,self.lbList[i].text()+str(ansList[i]))
                    errorStList.append(True)
                    if self.stList[i]==False:
                        self.errorQuestionNum+=1  
                else:
                    errorStList.append(False)
                        
                    
                    
            self.leList[i].clear()
       

        self.lbList=errorLbList
        self.leList=errorLeList
        self.stList=errorStList

        if len(self.lbList)==0:

            self.endTest()
            #QApplication.instance().quit()
            

        

        self.showQuestions()
                

        
        

        

    
    '''


    def endTest(self):

        
        today=datetime.date.today()
        if self.testType==0:
            text="{} 进行100以内加减法及连加减练习:".format(today)
        elif self.testType==1:
            text="{} 进行乘法表练习:".format(today)
        '''
        print(text)
        print(self.questionNum)
        print(type(self.isErrorInQues),self.isErrorInQues)
        print(self.errorTimes)
        '''
        text+=" 习题数:{0},错题数:{1},错误次数:{2}   ".format(self.questionNum,sum(self.isErrorInQues),self.errorTimes)
        #print(text)
        fileAddLine(dayRecordFilePath,text)
        #print(self.questionNum,self.errorQuestionNum,self.errorTimes)
        QMessageBox.about(self,"恭喜全部完成","一共{0}道算术题，有{1}道算错过,累计算错过{2}回!\n下回继续加油，拜拜！".format(\
                          self.questionNum,sum(self.isErrorInQues),self.errorTimes))
        QApplication.instance().quit()



    def getText(self):

        text=""

        for i in range(self.questionNum):

            subText=self.quesList[i]
            n=len(subText)
            subText=" "*(12-n)+subText+" "*10
            text=text+subText
            if self.testType != 4:
                if i%2==1 and i!=self.questionNum-1:
                    text=text+"\n\n"
                    if self.testType == 2 or self.testType == 3:
                        text=text+"\n\n\n"
            else:
                text=text+"\n\n\n\n\n"            

        return text

    def saveFunc(self):

        if not self.isInTest:
            QMessageBox.about(self,"错误操作","开没有开始测试，没有题目!")
            return

        fileName=QFileDialog.getSaveFileName(self,"保存文件",".","文本文件 (*.txt)")[0]
        if fileName=="":
            return
        text=self.getText()
        with open(fileName,"w") as file:
            file.write(text)


    def printFunc(self):

        if not self.isInTest:
            QMessageBox.about(self,"错误操作","开没有开始测试，没有题目!")
            return

        printer=QPrinter()
        printDialog=QPrintDialog(printer,self)
        if printDialog.exec_()==QDailog.Accepted:
            self.handlePrintRequest(printer)


    def printPreviewFunc(self):

        
        if not self.isInTest:
            QMessageBox.about(self,"错误操作","开没有开始测试，没有题目!")
            return

        dialog=QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePrintRequest)
        dialog.exec_()




    def printToPdfFunc(self):

        if not self.isInTest:
            QMessageBox.about(self,"错误操作","开没有开始测试，没有题目!")
            return

        
        printer=QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        fileName=QFileDialog.getSaveFileName(self,"保存pdf文件",".","Pdf文件 (*.pdf)")[0]
        if fileName=="":
            return
        printer.setOutputFileName(fileName)
        self.handlePrintRequest(printer)


    def handlePrintRequest(self,printer):
        
        text=self.getText()
        document=QTextDocument()
        cursor=QTextCursor(document)
        form=QTextCharFormat()
        form.setFont(QFont("SanFrancisco",24))
        cursor.setCharFormat(form)
        if self.testType==0:
            text=str(self.maxNum)+"以内加减法作业"+str(self.questionNum)+"道:\n\n"+text
        elif self.testType==1:
            text="乘法表练习{}道:\n\n".format(self.questionNum)+text
        elif self.testType==2:
            text = text
            text="多位数乘法练习{}道:\n\n".format(self.questionNum)+text
        elif self.testType==3:
            text = text
            text="多位数除法练习{}道:\n\n".format(self.questionNum)+text
        elif self.testType==4:
            text = text
            text="四则混合运算练习{}道:\n\n".format(self.questionNum)+text            
        cursor.insertText(text)
        document.print(printer)

    def configFunc(self):

        if self.isInTest:
            QMessageBox.about(self,"警告","测试已经开始，请在测试前设定!")
        else:
            configWindow=ConfigWindow(self)
            print(configWindow)
            configWindow.exec_()
            

        

        
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    w=Window()
    sys.exit(app.exec_())
    input('Press Enter to quit test:')
