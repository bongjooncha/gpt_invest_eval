import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dotenv,os

dotenv.load_dotenv()


#요청승인
scope = ['https://spreadsheets.google.com/feeds']

#이전에 생성한 json 파일 위치와 이름(여기서는 실행 파일과 같은 곳에 위치해 있기 때문에 위치를 작성하지 않음)
json_file_name = 'key.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
client = gspread.authorize(creds)
spreadsheet_url = os.environ['google_spreadsheat']
# 문서 불러오기
doc = client.open_by_url(spreadsheet_url)

x='1'

def sheat(x):
    # a 시트 불러오기
    worksheet = doc.worksheet(x)

    cell = worksheet.acell('d2').value
    print(cell)

sheat(x)