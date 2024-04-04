from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        print("Kiwoom2 클래스 입니다.")

    #이벤트 loop 모음
        #데이터를 지우고 시작
        self.login_event_loop = None
        #계정 갯수 초기화
        self.account_num = None
        #계정의 예수금상세 확인 루프 비우기
        self.detail_account_info_event_loop=None
        #계정의 예수그
        self.detail_account_info_event_loop2 =None

    #응용프로그램 제어
        #OXC값을 대입하여 프로그램을 찾음
        self.get_ocx_instnace()
        #키움에서 로그인 정보를 보여 해주는 코드
        self.event_slots()
        #로그인을 하는 코드
        self.signal_login_commConnect()
        #계정 번호 받기
        self.get_account_info()
        #예수금 받아오기
        self.detail_account_info()

    #변수모음
        #
        self.account_stock_dict = {}


    #키움 레지스트리 위치를 알려주기 위한 코드
    def get_ocx_instnace(self):
        self.setControl("KHOPENAPI.KHopenAPICtrl.1")

    #이벤트 슬롯 모음
    def event_slots(self):
        #로그인을 담당하는 이벤트
        self.OnEventConnect.connect(self.login_slot)
        #TR데이터를 불러오는 이벤트
        self.OnReceiveTrData.connect(self.trdata_slot)

    # event_slot에서 로그인을 하고 받은 결과값을 프린트
    # 로그인이 완료 후 exit()을 통해서 로그인 이벤트 루프를 끊어줌
    def login_slot(self,errCode):
        print(errors(errCode))
        self.login_event_loop.exit()

    #dynmicCall()은 다른 응용프로그램에 정보를 전달해줌
    #키움에 "CommConnect()"를 통해서 자동로그인 혹은 로그인창 출력
    #QEventLoop를 사용해서 로그인 변수 생성
    #.exec_를 이용해서 로그인이 완료될때 까지 다음 코드 실행 되지 않게 해줌
    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    #dynamicCall을 이용하여 키움 "GetLogininfo(String)"을 사용해서 로그인 정보를 가지고옴
    #"ACCNO"는 계좌 목록을 불러오겠다는 뜻임
    #"ACCNO"를 사용할시 ';'구분자로 복록을 반환하기에 이를 스플릿 해준다.
    #보유 계좌번호들을 출력
    def get_account_info(self):
        account_list = self.dynamicCall("GetLogininfo(String)","ACCNO")
        self.account_num = account_list.split(";")[0]
        print("나의 보유 계좌번호 %s" %self.account_num)

    #예수금상세현황의 데이터를 불러오기 위해 데이터를 보내는 부분
    def detail_account_info(self):
        print("예수금 받아오기")
        #1 Open API 조회 합수 입력값 입력
        self.dynamicCall("SetInputValue(String, String)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(String, String)","비밀번호","")
        self.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        #2 Open API 조회 함수를 호출해 서버로 전송(RQName(조회요청이름),TR번호,0,화면번호)
        self.dynamicCall("CommRqData(String, String, int, String)","예수금상세현황요청","opw00001", "0", "2000")
        #이벤트 루프 생성
        self.detail_account_info_event_loop=QEventLoop()
        self.detail_account_info_event_loop.exec_()

    #예수금상세현황의 데이터를 불러오기 위해 데이터를 보내는 부분
    def detail_account_info(self):
        print("예수금 받아오기")
        #1 Open API 조회 합수 입력값 입력
        self.dynamicCall("SetInputValue(String, String)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(String, String)","비밀번호","")
        self.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        #2 Open API 조회 함수를 호출해 서버로 전송(RQName(조회요청이름),TR번호,0,화면번호)
        self.dynamicCall("CommRqData(String, String, int, String)","예수금상세현황요청","opw00001", "0", "2000")
        #이벤트 루프 생성
        self.detail_account_info_event_loop2=QEventLoop()
        self.detail_account_info_event_loop2.exec_()

    #데이터 슬롯
    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        '''
        tr요청을 받는 구역
        :param sScrNo: 스크린번호
        :param sRQName: 내가 요청했을때 지은 이름
        :param sTrCode: 요청id, tr 코드
        :param sRecordName: 사용 x
        :param sPrevNext: 다음페이지가 있는지
        :return:
        '''

        #예수금 상세 현황 요청
        if sRQName == "예수금상세현황요청":
            depos = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금 %s" %format(int(depos),','))
            depos_now = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            print("출금 가능 금액 %s" %format(int(depos_now),','))
            #요청을 종료하는 코드
            self.detail_account_info_event_loop.exit()

        #계좌 평가 잔고내역
        if sRQName == "계좌평가잔고내역요청":
            depos = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금 %s" %format(int(depos),','))
            depos_now = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            print("출금 가능 금액 %s" %format(int(depos_now),','))

            #보유종목 가져오기
            rows = self.dynamicCall("GetRepeatCnt(QString,Qstring)",sTrCode, sRQName)
            cnt = 0
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, Qstring, int, Qstring)", sTrCode, sRQName, cnt, "종목번호")
                stock_name = self.dynamicCall("GetCommData(QString, Qstring, int, Qstring)", sTrCode, sRQName, cnt, "종목명")
                stock_quan = self.dynamicCall("GetCommData(QString, Qstring, int, Qstring)", sTrCode, sRQName, cnt, "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, Qstring, int, Qstring)", sTrCode, sRQName, cnt, "매입가")

                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict.update({code:{}})

                stock_name = stock_name.strip()
                stock_quan = int(stock_quan)
                buy_price = int(buy_price)

                self.account_stock_dict[code].update({"종목명":stock_name})
                self.account_stock_dict[code].update({"보유수량":stock_quan})
                self.account_stock_dict[code].update({"매입가":buy_price})

                cnt += 1

            print("계좌에 가지고 있는 종목 %s", self.account_stock_dict)
            print("계좌에 가지고 있는 종목수 %s", cnt)


            #요청을 종료하는 코드
            self.detail_account_info_event_loop.exit()