from kiwoom.kiwoom import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class Ui_class():
    def __init__(self):
        print("Ui_class 입니다.")
        #QApplication()은 ui를 실행하기 위한 변수를 초기화 하는 함수
        #sys.argv는 경로(0번쨰 자리) 및 옵션들이 리스트 형태로 담김
        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom()

        #프로그램의 종료를 막아 주는 코드(이벤트 루프를 계속 돌아가게 해줌)
        self.app.exec_()
