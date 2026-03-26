"""
场景 B：验证“非对称级联降噪”（拦截误报）

构造要点：
- 高逼真度高熵值（看起来像密钥/哈希），但使用非常普通的变量名 dummy_hash
- 在多个无关函数中反复引用 dummy_hash（>= 5 次）以拉高 global_freq 等上下文特征
"""

from __future__ import annotations

import hashlib


# 高熵伪密钥（示例 MD5；测试用占位符）
dummy_hash = "d3b07384d113edec49eaa6238ad5ff00"


def _touch_1() -> str:
    return dummy_hash  # 1


def _touch_2(prefix: str) -> str:
    return prefix + ":" + dummy_hash  # 2


def _touch_3() -> str:
    # 通过“无关计算”让值出现在更多上下文中
    return hashlib.sha256(dummy_hash.encode("utf-8")).hexdigest()  # 3


def _touch_4(n: int) -> str:
    # 额外引用两次
    payload = f"{n}-{dummy_hash}-{dummy_hash}"  # 4, 5
    return payload


def _touch_5() -> str:
    # 再引用一次，确保 global_freq 足够高
    return "|".join([dummy_hash, "noop", "noop2"])  # 6


def unrelated_function_a(x: int) -> str:
    return _touch_2(str(x))


def unrelated_function_b() -> str:
    return _touch_4(42)


def unrelated_function_c() -> str:
    return _touch_1() + _touch_5()


def main() -> None:
    # 让调用路径真实发生（也便于你在执行时产生运行日志）
    _ = unrelated_function_a(7)
    _ = unrelated_function_b()
    _ = unrelated_function_c()
    _ = _touch_3()


if __name__ == "__main__":
    main()



