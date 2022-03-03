import requests, json, time, logging
from datetime import datetime
import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


developer_token = 'ycgcXthqbaaBCSapzWsV0g'

def get_token():
    url = 'https://www.googleapis.com/oauth2/v3/token'
    mess = ''
    token = ''
    data = {
        'grant_type': 'refresh_token',
        'client_id': '724613478382-f22190u3suije4p22rputi73nilhdv7r.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//0cDFPBykDkqhqCgYIARAAGAwSNwF-L9IrzGFJJ2sf1jvjEN-YNRMSdNuMKuf79dwNIAdaH6M1YTogHapZsO1qiDowae9tY9fOX8I',
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        if resp.status_code == 200:
            dct_answer = json.loads(resp.text)
            token = dct_answer.get('access_token')
            expires_in = dct_answer.get('expires_in')
            # print(expires_in)
            if token == None:
                fault = dct_answer.get('fault')
                if fault: mess = f'ERROR: {fault.get("message")} {fault.get("description")}'
        else: mess = f'ERROR get_token: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_token: try: {str(e)}'
    
    return mess[:200], token
    
def get_test(token):
    # url = 'https://googleads.googleapis.com/v10/customers:listAccessibleCustomers'
    # url = 'https://googleads.googleapis.com/v10/basic_operations:get_campaigns'
    url = 'https://googleads.googleapis.com/v10'
    params = {
        'Authorization': f'Bearer {token}',
        'developer-token': developer_token,
    }
    # try:
    resp = requests.post(url, params=params, timeout=30)
    print(resp.status_code)
    print(resp.text)




def run_google_ads():
    # Получаем токен
    e, token = get_token()
    if e:
        print(e)
        # mess = f'run_lk_mts ERROR: {e}'
        # send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
        # logger.error(mess)
        return
    time.sleep(0.2)
    print('token OK')
    
    get_test(token)
    
    
    
    
if __name__ == '__main__':
    # # run_google_ads()
    # googleads_client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    # ga_service = googleads_client.get_service("GoogleAdsService")

    # query = """
        # SELECT
          # campaign.id,
          # campaign.name
        # FROM campaign
        # ORDER BY campaign.id"""
    
    # # customer_id = '7451203980'
    # customer_id = '7636307846'
    # # Issues a search request using streaming.
    # try:
        # stream = ga_service.search_stream(customer_id=customer_id, query=query)
    # except GoogleAdsException as ex:
        # print(
            # f'Request with ID "{ex.request_id}" failed with status '
            # f'"{ex.error.code().name}" and includes the following errors:'
        # )
        # for error in ex.failure.errors:
            # print(f'\tError with message "{error.message}".')
            # if error.location:
                # for field_path_element in error.location.field_path_elements:
                    # print(f"\t\tOn field: {field_path_element.field_name}")
        # sys.exit(1)
        
    # for batch in stream:
        # for row in batch.results:
            # print(
                # f"Campaign with ID {row.campaign.id} and name "
                # f'"{row.campaign.name}" was found.'
            # )
    #============================== работает ====================
    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    customer_service = client.get_service("CustomerService")

    accessible_customers = customer_service.list_accessible_customers()
    result_total = len(accessible_customers.resource_names)
    print(f"Total results: {result_total}")

    resource_names = accessible_customers.resource_names
    for resource_name in resource_names:
        print(f'Customer resource name: "{resource_name}"')
    #==============================  ====================
    # client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    # ga_service = client.get_service("GoogleAdsService")
    # query = """
        # SELECT
            # customer.id,
            # customer.descriptive_name,
            # customer.currency_code,
            # customer.time_zone,
            # customer.tracking_url_template,
            # customer.auto_tagging_enabled
        # FROM customer
        # LIMIT 1"""
    
    # # customer_id = '7944544741'
    # customer_id = '6796810439'
    # # customer_id = '7636307846'
    # request = client.get_type("SearchGoogleAdsRequest")
    # request.customer_id = customer_id
    # request.query = query
    # response = ga_service.search(request=request)
    # # customer = list(response)[0].customer
    # print(response)

    # print(f"Customer ID: {customer.id}")
    # print(f"\tDescriptive name: {customer.descriptive_name}")
    # print(f"\tCurrency code: {customer.currency_code}")
    # print(f"\tTime zone: {customer.time_zone}")
    # print(f"\tTracking URL template: {customer.tracking_url_template}")
    # print(f"\tAuto tagging enabled: {customer.auto_tagging_enabled}")
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # def main(client, manager_customer_id):
    # # manager_customer_id = '7944544741'
    # # manager_customer_id = '7636307846'
    # manager_customer_id = '7944544741'
    # # client = GoogleAdsClient.load_from_storage(version="v10")
    # client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    # customer_service = client.get_service("CustomerService")
    # customer = client.get_type("Customer")
    # now = datetime.today().strftime("%Y%m%d %H:%M:%S")
    # customer.descriptive_name = f"Account created with CustomerService on {now}"
    # # For a list of valid currency codes and time zones see this documentation:
    # # https://developers.google.com/google-ads/api/reference/data/codes-formats
    # customer.currency_code = "RUB"
    # customer.time_zone = "Europe/Moscow"
    # # The below values are optional. For more information about URL
    # # options see: https://support.google.com/google-ads/answer/6305348
    # # customer.tracking_url_template = "{lpurl}?device={device}"
    # # customer.final_url_suffix = (
        # # "keyword={keyword}&matchtype={matchtype}" "&adgroupid={adgroupid}"
    # # )

    # try:
        # response = customer_service.create_customer_client(
            # customer_id=manager_customer_id, customer_client=customer
        # )
    # except GoogleAdsException as ex:
        # print(
            # f'Request with ID "{ex.request_id}" failed with status '
            # f'"{ex.error.code().name}" and includes the following errors:'
        # )
        # for error in ex.failure.errors:
            # print(f'\tError with message "{error.message}".')
            # if error.location:
                # for field_path_element in error.location.field_path_elements:
                    # print(f"\t\tOn field: {field_path_element.field_name}")
        # sys.exit(1)
    
    # print(
        # f'Customer created with resource name "{response.resource_name}" '
        # f'under manager account with ID "{manager_customer_id}".'
    # )