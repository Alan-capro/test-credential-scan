"""
场景 A：验证“高敏感语义先验熔断”

目标：
- 精准命中后端 `ScannerService._match_high_sensitive_term()` 中的高危词集合。
- 通过“标准赋值行 + 明确引用行”双保险，确保 override_term 必定为真，
  从而触发后端打印日志：`[🔥 Semantic Override 触发] ...`
"""

from __future__ import annotations


# 选用的高危词（必须与后端 Settings.high_sensitive_terms 完全一致）
# 后端默认包含：AWS_SECRET_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # synthetic secret token value
EXTRA_CONTEXT = "AWS_SECRET_ACCESS_KEY secret token private key credential auth"


def main() -> None:
    # 1) 标准赋值行：让 expCode/credential_scanner.extract_variable_name 捕获到变量名
    secret_alias = AWS_SECRET_ACCESS_KEY  # token secret auth credential

    # 2) 明确引用行：即便变量名抽取失败，后端也会在 code_text 上做 `\b...\b` 词边界正则命中
    _ = {"auth": secret_alias, "credential": AWS_SECRET_ACCESS_KEY}


if __name__ == "__main__":
    main()



