import os
from typing import Dict, Any
import re


def render_srs_from_llm_response(proj_name: str, llm_response: Dict[str, Any], template_path: str = None) -> str:
    """
    將 LLM 回應(dict)渲染到 SRS markdown 模板。
    :param llm_response: LLM 回傳的 dict 內容
    :param template_path: SRS 模板檔案路徑，預設為專案根目錄下 srs_tmpl.md
    :return: 渲染後的 SRS markdown 字串
    """
    if template_path is None:
        template_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'srs_tmpl.md')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    template = template.replace('{project_name}', proj_name)

    # 處理 {{optional_features}} 佔位符
    optional_features_md = ''
    optional_features = llm_response.get('optional_features')
    if optional_features and isinstance(optional_features, list):
        for idx, feat in enumerate(optional_features):
            name = feat.get('name', f'選擇性功能{idx+1}')
            desc = feat.get('description', '')
            priority = feat.get('priority', '')
            notes = feat.get('notes', '')
            optional_features_md += f"""
* **選擇性功能 {name} 名稱：** {name}
    * **描述：** {desc}
    * **優先級：** {priority}
    * **備註：** {notes}
"""
    template = template.replace('{{optional_features}}', optional_features_md)
    template = template.replace('{optional_features}', optional_features_md)

    # 處理 {{core_features}} 佔位符
    core_features_md = ''
    core_features = llm_response.get('core_features')
    if core_features and isinstance(core_features, list):
        for idx, feat in enumerate(core_features):
            name = feat.get('name', f'核心功能{idx+1}')
            desc = feat.get('description', '')
            priority = feat.get('priority', '')
            user_stories = feat.get('user_stories', '')
            core_features_md += f"""
* **功能 {idx+1} 名稱：** {name}
    * **描述：** {desc}
    * **優先級：** {priority}
    * **相關使用者故事/用例：** {user_stories}
"""
    template = template.replace('{{core_features}}', core_features_md)
    template = template.replace('{core_features}', core_features_md)

    # 依照模板中的 {key} 進行替換（排除 optional_features）
    result = template
    for k, v in llm_response.items():
        if k == 'optional_features' or k == 'core_features':
            continue
        result = result.replace(f'{{{k}}}', str(v) if v is not None else '')
    return result


def extract_json_from_response(response_str):
    # 去除 ```json、``` 及前後空白
    response_str = response_str.replace(
        '```json', '').replace('```', '').strip()
    return response_str
