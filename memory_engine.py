import json
import os
import time

class MemoryEngine:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.state = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    state = json.load(f)
                    state.setdefault('subscribed_submolts', [])
                    state.setdefault('replied_comments', [])
                    state.setdefault('upvoted_posts', [])
                    state.setdefault('last_post_time', 0)
                    return state
            except Exception:
                pass
        return {
            'created_at': time.time(),
            'last_run': None,
            'last_post_time': 0,
            'subscribed_submolts': [],
            'replied_comments': [],
            'upvoted_posts': [],
            'karma_history': [],
            'posts_created': [],
            'comments_made': [],
            'followed_agents': [],
            'wallet_history': [],
            'insights': []
        }

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def is_submolt_subscribed(self, submolt_name):
        return submolt_name in self.state.get('subscribed_submolts', [])

    def mark_submolt_subscribed(self, submolt_name):
        if submolt_name not in self.state['subscribed_submolts']:
            self.state['subscribed_submolts'].append(submolt_name)
            self.save_memory()

    def is_comment_replied(self, comment_id):
        return comment_id in self.state.get('replied_comments', [])

    def mark_comment_replied(self, comment_id):
        if comment_id not in self.state['replied_comments']:
            self.state['replied_comments'].append(comment_id)
            self.save_memory()

    def is_post_upvoted(self, post_id):
        return post_id in self.state.get('upvoted_posts', [])

    def mark_post_upvoted(self, post_id):
        if post_id not in self.state['upvoted_posts']:
            self.state['upvoted_posts'].append(post_id)
            self.save_memory()

    def record_run(self, karma, balances):
        self.state['last_run'] = time.time()
        self.state['karma_history'].append({'timestamp': time.time(), 'karma': karma})
        self.state['wallet_history'].append({'timestamp': time.time(), 'balances': balances})
        self.save_memory()

    def add_post_record(self, post_id, title, submolt):
        self.state['posts_created'].append({
            'post_id': post_id,
            'title': title,
            'submolt': submolt,
            'timestamp': time.time()
        })
        self.state['last_post_time'] = time.time()
        self.save_memory()

    def add_comment_record(self, comment_id, post_id, content):
        self.state['comments_made'].append({
            'comment_id': comment_id,
            'post_id': post_id,
            'content': content,
            'timestamp': time.time()
        })
        self.save_memory()

    def add_insight(self, insight):
        self.state['insights'].append({
            'timestamp': time.time(),
            'insight': insight
        })
        self.save_memory()
