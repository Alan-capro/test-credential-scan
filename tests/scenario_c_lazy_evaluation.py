"""
场景 C：验证“延迟计算（Lazy Evaluation）”

构造要点：
- 同一文件内混合 1 个“真实极高危密钥”（高敏感语义变量名 + 明显口令值）
- 以及 10 个普通伪密钥/UUID（用于被 Stage2 证伪并跳过 I/O 溯源）
"""

from __future__ import annotations

from dataclasses import dataclass


# 1 个真实的极高危密钥（测试用占位符）
DB_PASSWORD = "RealSecretPassword123!@#"


# 10 个普通的伪密钥/UUID（测试用占位符）
test_id_1 = "123e4567-e89b-12d3-a456-426614174000"
test_id_2 = "123e4567-e89b-12d3-a456-426614174001"
test_id_3 = "123e4567-e89b-12d3-a456-426614174002"
test_id_4 = "123e4567-e89b-12d3-a456-426614174003"
test_id_5 = "123e4567-e89b-12d3-a456-426614174004"
test_id_6 = "123e4567-e89b-12d3-a456-426614174005"
test_id_7 = "123e4567-e89b-12d3-a456-426614174006"
test_id_8 = "123e4567-e89b-12d3-a456-426614174007"
test_id_9 = "123e4567-e89b-12d3-a456-426614174008"
test_id_10 = "123e4567-e89b-12d3-a456-426614174009"


@dataclass(frozen=True)
class RequestContext:
    request_id: str
    user_id: str


def build_context() -> RequestContext:
    # 将 UUID 混入无关上下文，模拟真实业务中常见的 trace/request 字段
    return RequestContext(request_id=test_id_1, user_id=test_id_2)


def connect_to_db_simulated(password: str) -> str:
    # 仅用于让“真实密钥”走到可执行路径中
    return f"db://user:{password}@localhost:5432/app"


def main() -> None:
    _ctx = build_context()

    # 触发 10 个伪样本被扫描到（但期望后端 lazy 跳过 blame I/O）
    _ = (
        test_id_3,
        test_id_4,
        test_id_5,
        test_id_6,
        test_id_7,
        test_id_8,
        test_id_9,
        test_id_10,
    )

    # 仅对 1 个被确证的真实密钥，期望触发后端更重的溯源流程（git blame -L）
    _conn = connect_to_db_simulated(DB_PASSWORD)
    _ = (_ctx, _conn)


if __name__ == "__main__":
    main()


