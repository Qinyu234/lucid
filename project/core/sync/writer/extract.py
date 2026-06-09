"""
CSF → Code patch: Extract Function
使用 libcst 提取函数
"""
import libcst as cst
from typing import Dict, List


def extract_function(csf: Dict, node_ids: List[str], new_name: str, source_path: str) -> Dict:
    """
    提取函数
    
    用 libcst 解析源文件，找到 node_ids 对应的 CST 节点，
    提取成新函数，在原位替换为调用
    
    返回:
    {
        "patch": str,        # unified diff 字符串
        "new_csf": dict,     # 更新后的 csf
        "preview": str,      # 操作预览描述
    }
    """
    with open(source_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    tree = cst.parse_module(source_code)
    
    # v0.1 简化实现：返回占位符
    return {
        "patch": "",
        "new_csf": csf.copy(),
        "preview": f"extract_function: {len(node_ids)} nodes → {new_name}()",
    }
