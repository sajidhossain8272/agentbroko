import urllib.request
import urllib.parse
import json
import re
import os
import hashlib
import time
import logging
from dataclasses import dataclass

@dataclass
class PublishResult:
    success: bool
    post_id: str | None = None
    verified: bool = False
    error: str | None = None
    verification_required: bool = False
    status_code: str = "UNKNOWN"

class MoltbookClient:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get("MOLTBOOK_API_KEY", "")
        if not api_key:
            if os.path.exists(".env"):
                try:
                    with open(".env", "r") as f:
                        for line in f:
                            if line.strip().startswith("MOLTBOOK_API_KEY="):
                                api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                except Exception:
                    pass
        if not api_key:
            cred_path = os.path.expanduser('~/.config/moltbook/credentials.json')
            if os.path.exists(cred_path):
                try:
                    with open(cred_path, 'r') as f:
                        creds = json.load(f)
                        api_key = creds.get('api_key')
                except Exception:
                    pass

        self.api_key = api_key
        self.base_url = 'https://www.moltbook.com/api/v1'

    def _request(self, endpoint, method='GET', payload=None):
        if not self.api_key:
            logging.error("[MOLTBOOK] API key missing")
            return {'success': False, 'error': '[MOLTBOOK] API key missing'}

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = json.dumps(payload).encode('utf-8') if payload else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            try:
                res = json.loads(err_body)
                res['http_code'] = e.code
                return res
            except Exception:
                return {'success': False, 'error': f"HTTP {e.code}: {err_body}", 'http_code': e.code}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_home(self):
        return self._request('/home')

    def get_feed(self, sort='new', limit=20, filter_type=None):
        query = f"?sort={sort}&limit={limit}"
        if filter_type:
            query += f"&filter={filter_type}"
        return self._request(f'/feed{query}')

    def get_comments(self, post_id, sort='new', limit=35):
        return self._request(f'/posts/{post_id}/comments?sort={sort}&limit={limit}')

    def upvote_post(self, post_id):
        return self._request(f'/posts/{post_id}/upvote', method='POST')

    def upvote_comment(self, comment_id):
        return self._request(f'/comments/{comment_id}/upvote', method='POST')

    def create_comment(self, post_id, content, parent_id=None):
        payload = {'content': content}
        if parent_id:
            payload['parent_id'] = parent_id
        res = self._request(f'/posts/{post_id}/comments', method='POST', payload=payload)
        
        if res.get('verification_required') or (res.get('comment') and res['comment'].get('verification')):
            verif = res.get('verification') or res['comment']['verification']
            self.solve_and_verify(verif)
        return res

    def create_post(self, submolt_name, title, content) -> PublishResult:
        if not self.api_key:
            logging.error("[MOLTBOOK] Publication failed: API key missing")
            return PublishResult(success=False, error="[MOLTBOOK] API key missing", status_code="AUTH_ERROR")

        # Duplicate Protection via Content Hashing
        content_hash = hashlib.sha256(f"{submolt_name}:{title}:{content}".encode('utf-8')).hexdigest()
        if self.is_duplicate_publication(content_hash):
            logging.info(f"[MOLTBOOK] Duplicate content detected for title '{title[:30]}...'; skipping publication.")
            return PublishResult(success=False, error="Duplicate content detected", status_code="DUPLICATE_SKIPPED")

        logging.info(f"[MOLTBOOK] Publication attempt started | Submolt: m/{submolt_name} | Title: '{title[:40]}...' | Length: {len(content)}")
        payload = {
            'submolt_name': submolt_name,
            'title': title,
            'content': content
        }
        res = self._request('/posts', method='POST', payload=payload)

        if not res.get('success') and not res.get('post') and not res.get('verification_required'):
            err = res.get('error', 'Unknown HTTP error')
            http_code = res.get('http_code')
            
            # Enhance error message with rate limit details if present
            if http_code == 429:
                retry_after = res.get('retry_after_seconds', 'unknown')
                err = f"HTTP 429 Rate Limited: {err} | retry_after_seconds: {retry_after}"
            elif http_code:
                err = f"HTTP {http_code}: {err}"
            
            logging.error(f"[MOLTBOOK] Publication failed at CREATE stage | Error: {err}")
            logging.error(f"[MOLTBOOK] Full response: {json.dumps(res, indent=2)}")
            return PublishResult(success=False, error=err, status_code="FAILED_CREATE")

        post_id = res.get('post', {}).get('id') or res.get('post_id')
        verif_required = res.get('verification_required', False) or bool(res.get('verification') or (res.get('post') and res['post'].get('verification')))

        if verif_required:
            logging.info("[MOLTBOOK] Verification required | Extracting challenge...")
            verif = res.get('verification') or (res.get('post') and res['post'].get('verification'))
            verif_res = self.solve_and_verify(verif)

            if verif_res and verif_res.get('success'):
                logging.info(f"[MOLTBOOK] Verification successful | Published successfully | Post ID: {post_id}")
                self.record_publication_hash(content_hash, post_id, submolt_name, title)
                return PublishResult(success=True, post_id=post_id, verified=True, verification_required=True, status_code="SUCCESS")
            else:
                v_err = verif_res.get('error') if verif_res else 'Verification challenge solution rejected'
                logging.error(f"[MOLTBOOK] Publication failed at VERIFICATION stage | Error: {v_err}")
                return PublishResult(success=False, post_id=post_id, verified=False, error=v_err, verification_required=True, status_code="FAILED_VERIFICATION")

        logging.info(f"[MOLTBOOK] Published successfully without verification | Post ID: {post_id}")
        self.record_publication_hash(content_hash, post_id, submolt_name, title)
        return PublishResult(success=True, post_id=post_id, verified=True, verification_required=False, status_code="SUCCESS")

    def solve_and_verify(self, verif):
        if not verif:
            return {'success': False, 'error': 'Missing verification object'}

        code = verif.get('verification_code')
        challenge = verif.get('challenge_text')
        if not code or not challenge:
            logging.error("[MOLTBOOK] Invalid verification payload structure")
            return {'success': False, 'error': 'Missing code or challenge text'}

        logging.info(f"[MOLTBOOK] Challenge received | Code: {code[:12]}...")
        answer = self.solve_math_challenge(challenge)
        if answer is not None:
            logging.info(f"[MOLTBOOK] Challenge solved -> Answer: {answer} | Submitting verification...")
            verif_res = self._request('/verify', method='POST', payload={
                'verification_code': code,
                'answer': str(answer)
            })
            logging.info(f"[MOLTBOOK] Verification response: {json.dumps(verif_res, indent=2)}")
            return verif_res
        
        logging.error("[MOLTBOOK] Unsupported verification challenge")
        return {'success': False, 'error': 'Unsupported verification challenge'}

    @staticmethod
    def solve_math_challenge(text):
        """
        Parses obfuscated math challenge strings and returns normalized numeric answer.
        Returns None if parsing fails.
        """
        if not text:
            return None

        words_to_num = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
            'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
            'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
            'hundred': 100
        }

        lower_txt = text.lower()
        numbers = []

        # Tokenize by punctuation/spaces while preserving digits
        clean_text = re.sub(r'[^a-zA-Z0-9\.\s]', ' ', lower_txt)
        tokens = clean_text.split()

        i = 0
        while i < len(tokens):
            t = tokens[i]
            # 1. Direct digit match e.g. "15" or "32.5"
            if re.match(r'^\d+(?:\.\d+)?$', t):
                numbers.append(float(t))
            # 2. Word match e.g. "thirty" or "thirty two"
            elif t in words_to_num:
                val = float(words_to_num[t])
                if i + 1 < len(tokens) and tokens[i+1] in words_to_num:
                    next_val = words_to_num[tokens[i+1]]
                    if val >= 20 and next_val < 10:
                        val += next_val
                        i += 1
                numbers.append(val)
            i += 1

        if len(numbers) >= 2:
            n1, n2 = numbers[0], numbers[1]
            if 'slow' in lower_txt or 'reduce' in lower_txt or 'minus' in lower_txt or 'subtract' in lower_txt or 'less' in lower_txt or ' - ' in text:
                res = n1 - n2
            elif 'times' in lower_txt or 'multiply' in lower_txt or 'product' in lower_txt or ' * ' in text or 'x' in tokens:
                res = n1 * n2
            elif 'divide' in lower_txt or 'split' in lower_txt or ' / ' in text:
                res = n1 / n2 if n2 != 0 else 0.0
            else:
                res = n1 + n2
            
            # Format as integer if whole number, else 2 decimal places
            return f"{res:.2f}" if res != int(res) else f"{int(res)}"

        elif len(numbers) == 1:
            res = numbers[0]
            return f"{res:.2f}" if res != int(res) else f"{int(res)}"

        return None

    def is_duplicate_publication(self, content_hash, hash_file="processed_posts.json"):
        if os.path.exists(hash_file):
            try:
                with open(hash_file, 'r') as f:
                    history = json.load(f)
                    for item in history:
                        if item.get("content_hash") == content_hash:
                            return True
            except Exception:
                pass
        return False

    def record_publication_hash(self, content_hash, post_id, submolt, title, hash_file="processed_posts.json"):
        history = []
        if os.path.exists(hash_file):
            try:
                with open(hash_file, 'r') as f:
                    history = json.load(f)
            except Exception:
                pass
        
        entry = {
            "post_id": post_id,
            "title": title,
            "submolt": submolt,
            "content_hash": content_hash,
            "published_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        history.append(entry)
        if len(history) > 100:
            history.pop(0)

        with open(hash_file, 'w') as f:
            json.dump(history, f, indent=2)

    def follow_agent(self, agent_name):
        return self._request(f'/agents/{agent_name}/follow', method='POST')

    def get_submolts(self):
        return self._request('/submolts')

    def subscribe_submolt(self, submolt_name):
        return self._request(f'/submolts/{submolt_name}/subscribe', method='POST')
