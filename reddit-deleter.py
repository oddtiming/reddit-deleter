import argparse
import datetime
import praw

import os

class RedditCommentDeleter:
    def __init__(self, reddit, days=7):
        self.reddit = reddit
        self.current_index = 0
        self.user = self.reddit.user.me()
        self.days = days
        self.fetch_comments()
        print(f'\n\nWelcome, {self.user.name}! Fetched {len(self.comments)} comments in the last {self.days} days. Use the commands below to manage your comments.')


    def get_time_elapsed(self, comment):
        # Get the current time and the time the comment was created
        now = datetime.datetime.now()
        created_time = datetime.datetime.fromtimestamp(comment.created_utc)

        # Calculate the time difference
        time_diff = now - created_time
        # Convert the time difference to a human-readable format
        if time_diff.days > 0:
            time_elapsed = f"{time_diff.days} days ago"
        elif time_diff.seconds > 3600:
            time_elapsed = f"{time_diff.seconds // 3600} hours ago"
        else:
            time_elapsed = f"{time_diff.seconds // 60} minutes ago"
        return time_elapsed


    def fetch_comments(self):
        now = datetime.datetime.now()
        days_ago = now - datetime.timedelta(days=self.days)
        self.comments = []
        self.checked = []
        for comment in self.reddit.redditor(self.reddit.user.me().name).comments.new(limit=None):
            created_time = datetime.datetime.fromtimestamp(comment.created_utc)
            if created_time > days_ago:
                self.comments.append(comment)
                self.checked.append(True)  # Mark for deletion by default

    def display_comments_with_checkmarks(self):
        print('\n')
        for index, (comment, checked) in enumerate(zip(self.comments, self.checked)):
            time_elapsed = self.get_time_elapsed(comment)
            checkmark = '[x]' if checked else '[ ]'
            print(f'{index + 1}. {checkmark} ({time_elapsed}) ' + f'{comment.body[:50]}...' if len(comment.body) > 50 else comment.body)

    def toggle_checkmark(self, index):
        if 0 <= index < len(self.checked):
            self.checked[index] = not self.checked[index]

    def delete_marked_comments(self):
        print('Are you sure you want to delete the marked comments? (y/n)')
        confirmation = input("> ").strip().lower()
        if confirmation == 'y':
            for comment, checked in zip(self.comments, self.checked):
                if checked:
                    comment.delete()  # Or edit and then delete, if desired
                    print(f'Deleted: {comment.body[:50]}...')
            print("Marked comments deleted.")
            self.fetch_comments()
        else:
            print("Deletion canceled.")

    def run(self):
        while True:
            self.display_comments_with_checkmarks()
            print("\nEnter the index of the comment to toggle its checkmark, 'd' to delete, 'q' to quit.")
            command = input("> ").strip().lower()

            if command.isdigit():
                self.toggle_checkmark(int(command) - 1)
            elif command == 'd':
                self.delete_marked_comments()
            elif command == 'q':
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete Reddit comments.')
    parser.add_argument('--days', type=int, default=7, help='Number of days to go back for comments.')
    args = parser.parse_args()

    # Use environment variables for credentials
    reddit = praw.Reddit(
        client_id=os.environ['REDDIT_CLIENT_ID'],
        client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        user_agent=os.environ['REDDIT_USER_AGENT'],
        username=os.environ['REDDIT_USERNAME'],
        password=os.environ['REDDIT_PASSWORD'],
    )
    reddit.validate_on_submit = True

    deleter = RedditCommentDeleter(reddit, args.days)
    deleter.run()
