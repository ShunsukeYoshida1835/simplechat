import json
import os
import urllib.request
import urllib.parse

# ここにURLを入れる
API_URL = ""

def lambda_handler(event, context):
    try:
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']

        # ローカルAPIに送信するデータ
        data = {'prompt': message}
        json_data = json.dumps(data).encode('utf-8')

        # リクエストの作成
        req = urllib.request.Request(API_URL + "/generate",
                                      data=json_data,
                                      headers={'Content-Type': 'application/json'},
                                      method='POST')

        # API呼び出し
        with urllib.request.urlopen(req) as res:
            response_body = res.read().decode('utf-8')
        response = json.loads(response_body)

        if 'generated_text' not in response:
            raise Exception("No 'generated_text' in API response")

        assistant_response = response['generated_text']

        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }