import re
import logging

class SecurityEngine:
    SECRET_PATTERNS = [
        (r'0x[a-fA-F0-9]{64}', 'EVM Private Key'),
        (r'5[HJK][1-9A-HJ-NP-Za-km-z]{49}', 'Bitcoin WIF Private Key'),
        (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
        (r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', 'GitHub Fine-Grained Token'),
        (r'(?=.*frown)(?=.*tonight)(?=.*accident)', 'Wallet Seed Phrase'),
        (r'AIzaSy[a-zA-Z0-9_-]{33}', 'Google API Key')
    ]

    VULNERABILITY_PATTERNS = [
        (r'eval\s*\(', 'Unsafe eval() execution'),
        (r'os\.system\s*\(', 'Unsanitized os.system execution'),
        (r'exec\s*\(', 'Unsafe exec() execution')
    ]

    @classmethod
    def scan_code(cls, code_content, filename=""):
        findings = []

        # 1. Secret Leak Detection
        for pattern, label in cls.SECRET_PATTERNS:
            if re.search(pattern, code_content):
                findings.append({
                    "severity": "CRITICAL",
                    "type": "SECRET_LEAK",
                    "label": label,
                    "filename": filename,
                    "action_required": "DO NOT COMMIT. Strip secret immediately!"
                })

        # 2. Security Vulnerability Scanning
        for pattern, label in cls.VULNERABILITY_PATTERNS:
            if re.search(pattern, code_content):
                findings.append({
                    "severity": "HIGH",
                    "type": "VULNERABILITY",
                    "label": label,
                    "filename": filename,
                    "action_required": "Refactor code to avoid unsafe execution."
                })

        is_safe = len([f for f in findings if f["severity"] == "CRITICAL"]) == 0
        return {
            "is_safe": is_safe,
            "findings_count": len(findings),
            "findings": findings
        }
