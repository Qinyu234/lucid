"""
CSF → Code patch: Add Early Return
使用 libcst 添加 early return
"""
import libcst as cst
from typing import Dict


def add_early_return(csf: Dict, block_node_id: str, source_path: str) -> Dict:
    """
    添加 early return (guard chain 转 early return)
    
    用 libcst.CSTTransformer 找到 guard_chain 对应的 if 节点，
    把嵌套 if 改写为 early return 形式
    
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
        "preview": f"add_early_return: block {block_node_id}",
    }
