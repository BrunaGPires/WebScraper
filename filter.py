from config import KEY_WORDS

class Filter:
    def __init__(self):
        self.key_words = KEY_WORDS

    def filter_news(self, all_news):
        filtered_posts = []

        for post in all_news:
            text = ' '.join(post['post_paragraph']).lower()
            title = post['title'].lower()

            for word in self.key_words:
                word_lower = word.lower()
                if word_lower in title or word_lower in text:
                    filtered_posts.append(post)
                    break
        return filtered_posts