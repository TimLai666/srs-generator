
import os
from typing import Dict, Any


def render_srs_from_llm_response(llm_response: Dict[str, Any], template_path: str = None) -> str:
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

    # 依照模板中的 {key} 進行替換
    result = template
    for k, v in llm_response.items():
        result = result.replace(f'{{{k}}}', str(v) if v is not None else '')
    return result
