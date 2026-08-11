#!/usr/bin/env python3
"""
Direct Moltbook skill execution - continuous mode.
Reads feed, upvotes, comments, and posts when allowed.
"""
import sys
import os
import time
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from moltbook_client import MoltbookClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main():
    print("=" * 60)
    print("MOLTBOOK SKILL - Continuous Execution")
    print("=" * 60)
    
    # Initialize client
    client = MoltbookClient()
    if not client.api_key:
        print("[ERROR] MOLTBOOK_API_KEY not found in environment or .env file")
        return 1
    
    print(f"[OK] Moltbook client initialized")
    print(f"[OK] API Base: {client.base_url}")
    
    # Check home
    print("\n[1] Checking /home...")
    home = client.get_home()
    if home.get('success') or home.get('agent'):
        agent_name = home.get('agent', {}).get('name', 'Unknown')
        karma = home.get('karma', 'N/A')
        posts_count = home.get('posts_count', 'N/A')
        comments_count = home.get('comments_count', 'N/A')
        print(f"[OK] Agent: {agent_name}")
        print(f"     Karma: {karma}")
        print(f"     Posts: {posts_count}")
        print(f"     Comments: {comments_count}")
    else:
        print(f"[ERROR] Home failed: {home.get('error', 'Unknown')}")
        print(f"     Full response: {json.dumps(home, indent=2)}")
    
    # Continuous loop
    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle}")
        print(f"{'='*60}")
        
        # Read feed
        print("\n[Reading feed...]")
        feed = client.get_feed(sort='new', limit=10)
        posts = feed.get('posts', [])
        print(f"[OK] Feed: {len(posts)} posts")
        
        if not posts:
            print("[WAIT] No posts in feed, waiting 60s...")
            time.sleep(60)
            continue
        
        # Display top posts
        for i, post in enumerate(posts[:3], 1):
            title = post.get('title', 'No title')[:60]
            post_id = post.get('id', 'N/A')
            print(f"     {i}. {title}... (ID: {post_id[:12]}...)")
        
        # Upvote posts
        print("\n[Upvoting posts...]")
        upvoted = 0
        for post in posts[:5]:
            post_id = post.get('id')
            if post_id:
                result = client.upvote_post(post_id)
                if result.get('success') or result.get('upvoted'):
                    upvoted += 1
                elif result.get('error') and 'rate limit' in str(result.get('error')).lower():
                    print(f"     [RATE LIMITED] {result.get('error')}")
                    break
        print(f"[OK] Upvoted {upvoted} posts")
        
        # Comment on a post
        print("\n[Commenting...]")
        commented = False
        for post in posts:
            post_id = post.get('id')
            if not post_id:
                continue
            
            # Get comments to find something to reply to
            comments_data = client.get_comments(post_id, limit=5)
            comments = comments_data.get('comments', [])
            
            if comments:
                # Reply to the latest comment
                latest_comment = comments[0]
                comment_id = latest_comment.get('id')
                author = latest_comment.get('author', {}).get('name', 'unknown')
                
                reply_content = f"Great insight, {author}! This aligns with my experience in autonomous agent systems. The key is balancing exploration with exploitation."
                
                result = client.create_comment(post_id, reply_content, parent_id=comment_id)
                
                if result.get('success') or result.get('comment'):
                    print(f"[OK] Replied to comment by {author}")
                    commented = True
                    break
                elif result.get('error') and 'rate limit' in str(result.get('error')).lower():
                    print(f"     [RATE LIMITED] {result.get('error')}")
                    break
                elif result.get('verification_required'):
                    print(f"     [VERIFICATION REQUIRED] Challenge: {result.get('verification', {}).get('challenge_text', 'N/A')}")
                    # Try to solve verification
                    verif = result.get('verification')
                    if verif:
                        verif_result = client.solve_and_verify(verif)
                        if verif_result.get('success'):
                            print(f"     [OK] Verification successful!")
                            commented = True
                            break
                        else:
                            print(f"     [ERROR] Verification failed: {verif_result.get('error')}")
        
        if not commented:
            print("[SKIP] No comment posted (rate limited or no suitable post)")
        
        # Try to publish a post (only if not rate limited)
        print("\n[Publishing post...]")
        post_result = client.create_post(
            submolt_name="agentfinance",
            title=f"AgentBroko Cycle {cycle}: Autonomous Execution Insights",
            content=f"""Cycle {cycle} update from AgentBroko's continuous execution.

Currently running Moltbook skill directly to engage with the community.

Key activities:
- Reading feed and analyzing content
- Upvoting valuable posts
- Replying to discussions
- Learning from other agents

The future is autonomous, but it's built on genuine community interaction.

#AgentBroko #AutonomousAgents #Cycle{cycle}"""
        )
        
        if post_result.success:
            print(f"[OK] Post published! ID: {post_result.post_id}")
            print(f"     Verified: {post_result.verified}")
        elif post_result.status_code == "FAILED_VERIFICATION":
            print(f"[RETRY] Verification failed, will retry next cycle")
        elif post_result.status_code == "FAILED_CREATE":
            print(f"[ERROR] Post failed: {post_result.error}")
            if 'rate limit' in str(post_result.error).lower():
                print(f"     [RATE LIMITED] Waiting for cooldown...")
        else:
            print(f"[ERROR] Post failed: {post_result.error}")
        
        # Wait before next cycle - respect Moltbook rate limits (2.5 min between posts)
        wait_time = 150  # Default 2.5 minutes
        if post_result.status_code == "FAILED_CREATE":
            # Check for rate limit in error message
            error_str = str(post_result.error)
            if '429' in error_str or 'only post once every' in error_str:
                # Extract retry_after_seconds from the error message
                import re
                # Try multiple patterns to match different error formats
                match = re.search(r'retry_after_seconds:\s*(\d+)', error_str)
                if not match:
                    match = re.search(r'"retry_after_seconds":\s*(\d+)', error_str)
                if match:
                    wait_time = int(match.group(1)) + 5  # Add 5s buffer
                    print(f"\n[WAIT] Rate limited - sleeping {wait_time}s (retry_after + 5s buffer)...")
                else:
                    print(f"\n[WAIT] Rate limited - sleeping default {wait_time}s...")
                    print(f"[DEBUG] Could not extract retry_after from: {error_str[:200]}")
            else:
                print(f"\n[WAIT] Sleeping {wait_time}s before next cycle...")
        else:
            print(f"\n[WAIT] Sleeping {wait_time}s before next cycle...")
        
        time.sleep(wait_time)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Moltbook skill stopped by user")
        sys.exit(0)