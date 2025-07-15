from google import genai
from google.genai.types import GenerateContentResponse

import os
import ssl
import re
import json

# 暫時停用 SSL 憑證驗證（僅用於開發測試）
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context


client = genai.Client()


def ask_gemini(prompt: str) -> str:
    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


def extract_json_from_response(response_str):
    # 嘗試自動補齊未結束的字串
    # 找到所有 "，如果是奇數，補一個 "
    quote_count = response_str.count('"')
    if quote_count % 2 == 1:
        response_str += '"'

    # 再次補齊未關閉的 object/array
    open_brace = response_str.count('{')
    close_brace = response_str.count('}')
    if open_brace > close_brace:
        response_str += '}' * (open_brace - close_brace)
    open_bracket = response_str.count('[')
    close_bracket = response_str.count(']')
    if open_bracket > close_bracket:
        response_str += ']' * (open_bracket - close_bracket)

    # 若內容明顯被截斷，給出警告
    if response_str and (response_str[-1] not in ['}', ']']):
        print('[警告] LLM 回傳內容可能被截斷，資料不完整，已嘗試自動補齊。')
    # 嘗試抓取 ```json ... ``` 區塊
    match = re.search(r"```json\s*([\s\S]*?)```", response_str)
    if match:
        response_str = match.group(1).strip()
    # 嘗試抓取 ``` ... ``` 區塊
    match = re.search(r"```([\s\S]*?)```", response_str)
    if match:
        response_str = match.group(1).strip()
    # 去除開頭 'json' 或其他雜訊，保證以 { 開頭
    json_start = response_str.find('{')
    if json_start != -1:
        response_str = response_str[json_start:]
    else:
        response_str = ''
    # 將 \n 換成空白，去除多餘空白
    response_str = response_str.replace('\n', ' ')
    response_str = re.sub(r'\s+', ' ', response_str)
    response_str = response_str.strip()
    # 處理 \" 被 escape 的情況
    if response_str.startswith('{') and '\"' in response_str:
        response_str = response_str.replace('\\"', '"')

    # 自動修復常見 JSON 問題
    # 1. 移除註解（//... 或 /* ... */）
    response_str = re.sub(r'//.*?([\n\r]|$)', '', response_str)
    response_str = re.sub(r'/\*.*?\*/', '', response_str, flags=re.DOTALL)
    # 2. 移除 ... 省略號
    response_str = response_str.replace('...', '')
    # 3. 移除陣列/物件結尾的逗號
    response_str = re.sub(r',\s*([}\]])', r'\1', response_str)
    # 4. 補齊未關閉的 array/object（簡單判斷）
    open_brace = response_str.count('{')
    close_brace = response_str.count('}')
    if open_brace > close_brace:
        response_str += '}' * (open_brace - close_brace)
    open_bracket = response_str.count('[')
    close_bracket = response_str.count(']')
    if open_bracket > close_bracket:
        response_str += ']' * (open_bracket - close_bracket)

    return response_str


def generate_srs(srs_map: dict, proj_name: str, proj_requirements: str) -> dict:
    prompt: str = f"""
    欄位定義：{srs_map}
    專案名稱：{proj_name}
    專案需求：{proj_requirements}
    你是一位專案經理，負責收集和整理專案需求。請根據以上信息生成一份完整的軟體需求規格書（SRS）。
    請嚴格只輸出純 JSON（不能有 markdown、註解、...、多餘文字、說明、程式碼區塊、標題、換行、註腳、或任何非 JSON 格式內容）。
    不得省略任何內容。
    """
    response_str: str = ask_gemini(prompt)
    json_str = extract_json_from_response(response_str)
    try:
        return json.loads(json_str)
    except Exception as e:
        print("[SRS JSON parse error] 原始內容如下:\n", json_str)
        raise e
