from google import genai
from google.genai.types import GenerateContentResponse
import os
import ssl

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


def generate_srs(srs_map: dict, proj_name: str, proj_requirements: str) -> str:
    prompt: str = f"""
    欄位定義：{srs_map}
    專案名稱：{proj_name}
    專案需求：{proj_requirements}
    你是一位專案經理，負責收集和整理專案需求。請根據以上信息生成一份完整的軟體需求規格書（SRS）。
    使用json格式輸出。
    """
    return ask_gemini(prompt).replace("```json", "").replace("```", "")
