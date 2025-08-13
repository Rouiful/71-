from django.core.management.base import BaseCommand
from toeic.models import DailyVocabulary
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Imports initial vocabulary data into the database.'

    def handle(self, *args, **options):
        # 難度 2-4 的不重複日常用語單字列表
        all_words = [
            # DailyLife 日常生活 (難度 2-4)
            {
                "word": "subtle",
                "pronunciation": "/ˈsʌtəl/",
                "part_of_speech": "adj.",
                "translation": "細微的，微妙的",
                "example_sentence": "He gave a subtle hint that he wanted to leave.",
                "example_translation": "他給了一個想離開的微妙暗示。",
                "difficulty_level": 3,
                "related_category": "DailyLife"
            },
            {
                "word": "tedious",
                "pronunciation": "/ˈtiːdiəs/",
                "part_of_speech": "adj.",
                "translation": "單調乏味的，冗長的",
                "example_sentence": "The process of filling out the forms was tedious.",
                "example_translation": "填寫這些表格的過程很單調乏味。",
                "difficulty_level": 3,
                "related_category": "DailyLife"
            },
            {
                "word": "conspicuous",
                "pronunciation": "/kənˈspɪkjuəs/",
                "part_of_speech": "adj.",
                "translation": "顯眼的，引人注目的",
                "example_sentence": "He made a conspicuous effort to be polite.",
                "example_translation": "他做出了顯著的努力來保持禮貌。",
                "difficulty_level": 4,
                "related_category": "DailyLife"
            },
            {
                "word": "profound",
                "pronunciation": "/prəˈfaʊnd/",
                "part_of_speech": "adj.",
                "translation": "深奧的，深刻的",
                "example_sentence": "His speech had a profound impact on everyone.",
                "example_translation": "他的演講對每個人都產生了深刻的影響。",
                "difficulty_level": 4,
                "related_category": "DailyLife"
            },
            {
                "word": "alleviate",
                "pronunciation": "/əˈliːviˌeɪt/",
                "part_of_speech": "v.",
                "translation": "減輕，緩解",
                "example_sentence": "The medicine helped to alleviate her pain.",
                "example_translation": "這款藥物幫助緩解了她的疼痛。",
                "difficulty_level": 4,
                "related_category": "DailyLife"
            },
            {
                "word": "leisure",
                "pronunciation": "/ˈliːʒər/",
                "part_of_speech": "n.",
                "translation": "閒暇，空閒時間",
                "example_sentence": "I like to read in my leisure time.",
                "example_translation": "我喜歡在閒暇時閱讀。",
                "difficulty_level": 2,
                "related_category": "DailyLife"
            },
            {
                "word": "commute",
                "pronunciation": "/kəˈmjuːt/",
                "part_of_speech": "v.",
                "translation": "通勤",
                "example_sentence": "He has a long commute to work every day.",
                "example_translation": "他每天通勤上班的路程很長。",
                "difficulty_level": 2,
                "related_category": "DailyLife"
            },
            {
                "word": "routine",
                "pronunciation": "/ruːˈtiːn/",
                "part_of_speech": "n.",
                "translation": "例行公事",
                "example_sentence": "My morning routine includes jogging and reading.",
                "example_translation": "我早上的例行公事包括慢跑和閱讀。",
                "difficulty_level": 2,
                "related_category": "DailyLife"
            },
            {
                "word": "spontaneous",
                "pronunciation": "/spɑːnˈteɪniəs/",
                "part_of_speech": "adj.",
                "translation": "自發的，非計畫好的",
                "example_sentence": "We made a spontaneous decision to go to the beach.",
                "example_translation": "我們做了一個自發的決定，要去海邊。",
                "difficulty_level": 3,
                "related_category": "DailyLife"
            },
            {
                "word": "chore",
                "pronunciation": "/tʃɔːr/",
                "part_of_speech": "n.",
                "translation": "家務雜事",
                "example_sentence": "Doing laundry is a daily chore for me.",
                "example_translation": "洗衣服對我來說是每天的家務雜事。",
                "difficulty_level": 2,
                "related_category": "DailyLife"
            },
        ]
        
        self.stdout.write(self.style.NOTICE('開始匯入單字資料...'))
        
        for word_data in all_words:
            try:
                DailyVocabulary.objects.create(**word_data)
                self.stdout.write(self.style.SUCCESS(f"成功新增單字: {word_data['word']}"))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f"單字 {word_data['word']} 已存在，跳過。"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"新增單字 {word_data['word']} 時出錯: {e}"))

        self.stdout.write(self.style.SUCCESS('所有單字處理完畢！'))
