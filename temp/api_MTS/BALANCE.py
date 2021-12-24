import requests
# import json
from bs4 import BeautifulSoup as bs  # pip install beautifulsoup4
import lxml  # pip install lxml


# access_token = "AQIC5wM2LY4SfcxPFfh9bjvKKdeCY4IH19rR7eLqmrlaEUM.*AAJTSQACMDQAAlNLABMtNTUwMjIzMTAyNTgzOTc1MDk0AAJTMQACMTE.*"
# number = '79109630404'

# headers = {
    # "Accept-Encoding": "gzip,deflate",
    # "Content-Type": "text/xml;charset=UTF-8",
    # "SOAPAction": "",
    # "Authorization": f"Bearer {access_token}",
    # "Content-Length": "1059",
    # "Host": "login.mts.ru:443",
    # "Connection": "Keep-Alive",
    # "User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)",
# }
# data = f'''
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:CustomerManagement="http://www.mts.ru/schema/api/CustomerManagement" xmlns:pag="http://mts.ru/siebel/pagination" xmlns:sec="http://schemas.xmlsoap.org/ws/2002/07/secext" xmlns:sieb="http://mts.ru/siebel" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   # <soapenv:Header>
      # <msisdn>{number}</msisdn>
   # </soapenv:Header>
   # <soapenv:Body>
      # <sieb:GetAccounts>
         # <request>
            # <channel id="NCIH" />
            # <items>
               # <item id="1" xsi:type="CustomerManagement:AccountRequestItem">
                  # <accounts>
                     # <account>
                        # <balances>
                           # <balance>
                              # <remainedAmount unitOfMeasure="RUB" />
                           # </balance>
                        # </balances>
                     # </account>
                  # </accounts>
               # </item>
            # </items>
         # </request>
      # </sieb:GetAccounts>
   # </soapenv:Body>
# </soapenv:Envelope>
# '''

# url = "https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/ICustomerManagementService/v1"

# responce = requests.post(url, headers=headers, data=data)
# print(responce.status_code)

# if responce.status_code != 200:
    # print(responce.text)
    # exit()

# with open("oauth_balance.txt", "w", encoding="utf-8") as file:
    # file.write(responce.text)

# bs_content = bs(responce.text, "lxml")

#################################################
with open("oauth_balance.txt", "r", encoding="utf-8") as file:
    content = file.readlines()

content = "".join(content)
bs = bs(content, "lxml")

print(bs.balance)

# ответ
# c:\Dev\parsing_MTS>python BALANCE.py
# 200
# 
# <?xml version='1.0' encoding='utf-8'?>
# <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
    # <S:Header>
        # <ns2:Pagination xmlns:ns2="http://mts.ru/siebel/pagination"/>
        # <ns1:Login xmlns:ns1="http://mts.ru/siebel">79109630404</ns1:Login>
        # <ns1:Source xmlns:ns1="http://mts.ru/siebel"/>
        # <ns1:SourceCode xmlns:ns1="http://mts.ru/siebel"/>
    # </S:Header>
    # <S:Body>
        # <ns1:GetAccountsResponse xmlns:ns1="http://mts.ru/siebel">
            # <result terminationCode="200" terminationMessage="Выполнено без ошибок">
            # <state>
                # success
            # </state>
            # <channel id="NCIH_National_PAPI"/>
            # <items>
                # <item xmlns:ns6="http://www.mts.ru/schema/api/CustomerManagement" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="4370236" xsi:type="ns6:AccountRequestItem">
                    # <accounts>
                        # <account id="276305269415">
                            # <balances>
                                # <balance>
                                    # <remainedAmount amount="1767.3" unitOfMeasure="Российский рубль"/>
                                # </balance>
                            # </balances>
                        # </account>
                    # </accounts>
                # </item>
            # </items></result></ns1:GetAccountsResponse>
    # </S:Body>
# </S:Envelope>

# хорошая статья про BeautifulSoup: https://habr.com/ru/company/ods/blog/346632/

# obj = soup.find(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links[:3]
