"""
场景 A：验证“高敏感语义先验熔断”

注意：以下字符串仅用于靶场/论文实验的告警触发测试（synthetic test data）。
"""

from __future__ import annotations


# 极其高危的变量名 + 值（用于触发后端 override_term 逻辑）
# 这里故意使用高度敏感语义的键名；值为测试用占位符。
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"


def do_nothing_but_keep_it_in_scope() -> str:
    """
    让变量在可执行路径中出现，避免被静态分析/打包时裁剪。
    """
    return AWS_SECRET_ACCESS_KEY


def main() -> None:
    _ = do_nothing_but_keep_it_in_scope()


if __name__ == "__main__":
    main()



