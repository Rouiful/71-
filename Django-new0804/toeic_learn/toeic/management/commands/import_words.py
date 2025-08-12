from django.core.management.base import BaseCommand
from toeic.models import DailyVocabulary
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Imports initial vocabulary data into the database.'

    def handle(self, *args, **options):
        # 等級 1-3 的單字列表
        easy_words = [
{
    "word": "consultant",
    "pronunciation": "/kənˈsʌltənt/",
    "part_of_speech": "n.",
    "translation": "顧問",
    "example_sentence": "The company hired a marketing consultant to improve sales.",
    "example_translation": "公司聘請了一位行銷顧問來提升銷售額。",
    "difficulty_level": 3,
    "related_category": "專業，服務"
},
{
    "word": "deduct",
    "pronunciation": "/dɪˈdʌkt/",
    "part_of_speech": "v.",
    "translation": "扣除，減除",
    "example_sentence": "Taxes will be deducted from your salary every month.",
    "example_translation": "稅金將會每個月從你的薪水中扣除。",
    "difficulty_level": 2,
    "related_category": "財務，會計"
},
{
    "word": "deposit",
    "pronunciation": "/dɪˈpɑːzɪt/",
    "part_of_speech": "n., v.",
    "translation": "訂金，存款；存放",
    "example_sentence": "We need to pay a deposit to reserve the conference room.",
    "example_translation": "我們需要支付訂金來預訂會議室。",
    "difficulty_level": 2,
    "related_category": "財務，銀行"
},
{
    "word": "evaluate",
    "pronunciation": "/ɪˈvæljueɪt/",
    "part_of_speech": "v.",
    "translation": "評估，評價",
    "example_sentence": "The manager will evaluate our performance at the end of the year.",
    "example_translation": "經理將在年底評估我們的工作表現。",
    "difficulty_level": 3,
    "related_category": "管理，考績"
},
{
    "word": "fund",
    "pronunciation": "/fʌnd/",
    "part_of_speech": "n., v.",
    "translation": "資金，基金；提供資金",
    "example_sentence": "The new project will be funded by the government.",
    "example_translation": "這個新專案將由政府提供資金。",
    "difficulty_level": 2,
    "related_category": "財務，專案"
},
{
    "word": "incur",
    "pronunciation": "/ɪnˈkɜːr/",
    "part_of_speech": "v.",
    "translation": "招致，蒙受",
    "example_sentence": "The company incurred heavy losses due to the economic downturn.",
    "example_translation": "由於經濟衰退，公司蒙受了巨大損失。",
    "difficulty_level": 3,
    "related_category": "財務，風險"
},
{
    "word": "merchandise",
    "pronunciation": "/ˈmɜːrtʃənˌdaɪz/",
    "part_of_speech": "n.",
    "translation": "商品，貨物",
    "example_sentence": "The store will have a sale on all merchandise next week.",
    "example_translation": "這家商店下週將會舉辦所有商品的特賣會。",
    "difficulty_level": 2,
    "related_category": "零售，銷售"
},
{
    "word": "revenue",
    "pronunciation": "/ˈrɛvənuː/",
    "part_of_speech": "n.",
    "translation": "收入，收益",
    "example_sentence": "The company's annual revenue has exceeded our expectations.",
    "example_translation": "公司的年度收益超出了我們的預期。",
    "difficulty_level": 3,
    "related_category": "財務，商業"
},
{
    "word": "tariff",
    "pronunciation": "/ˈtærɪf/",
    "part_of_speech": "n.",
    "translation": "關稅",
    "example_sentence": "The government plans to impose a new tariff on imported goods.",
    "example_translation": "政府計畫對進口商品課徵新關稅。",
    "difficulty_level": 3,
    "related_category": "國際貿易，商業"
},
{
    "word": "transaction",
    "pronunciation": "/trænˈzækʃən/",
    "part_of_speech": "n.",
    "translation": "交易，買賣",
    "example_sentence": "All credit card transactions are processed securely.",
    "example_translation": "所有信用卡交易都經過安全處理。",
    "difficulty_level": 2,
    "related_category": "財務，銀行"
}
        ]

        # 等級 4-5 的單字列表
        hard_words = [
            {
    "word": "arbitrate",
    "pronunciation": "/ˈɑːrbəˌtreɪt/",
    "part_of_speech": "v.",
    "translation": "仲裁，公斷",
    "example_sentence": "An independent body was called in to arbitrate the labor dispute.",
    "example_translation": "一個獨立機構被請來仲裁這場勞資糾紛。",
    "difficulty_level": 5,
    "related_category": "法律，爭議"
},
{
    "word": "conglomerate",
    "pronunciation": "/kənˈɡlɑːmərət/",
    "part_of_speech": "n.",
    "translation": "企業集團",
    "example_sentence": "The tech company is a large conglomerate with various subsidiaries.",
    "example_translation": "這家科技公司是一個擁有許多子公司的龐大企業集團。",
    "difficulty_level": 5,
    "related_category": "企業，策略"
},
{
    "word": "disburse",
    "pronunciation": "/dɪsˈbɜːrs/",
    "part_of_speech": "v.",
    "translation": "支付，支出",
    "example_sentence": "The funds will be disbursed to the contractors after the project is completed.",
    "example_translation": "專案完成後，資金將會支付給承包商。",
    "difficulty_level": 5,
    "related_category": "財務，會計"
},
{
    "word": "embezzle",
    "pronunciation": "/ɪmˈbɛzəl/",
    "part_of_speech": "v.",
    "translation": "貪污，挪用",
    "example_sentence": "The accountant was fired for embezzling company funds.",
    "example_translation": "這名會計師因挪用公司資金而被解雇。",
    "difficulty_level": 5,
    "related_category": "法律，財務"
},
{
    "word": "fiscal",
    "pronunciation": "/ˈfɪskəl/",
    "part_of_speech": "adj.",
    "translation": "財政的，會計的",
    "example_sentence": "The company's fiscal year ends on December 31st.",
    "example_translation": "公司的財政年度在 12 月 31 日結束。",
    "difficulty_level": 4,
    "related_category": "財務，會計"
},
{
    "word": "indemnity",
    "pronunciation": "/ɪnˈdɛmnəti/",
    "part_of_speech": "n.",
    "translation": "賠償，保證",
    "example_sentence": "The contract includes an indemnity clause to protect both parties.",
    "example_translation": "這份合約包含一項賠償條款來保護雙方。",
    "difficulty_level": 5,
    "related_category": "法律，保險"
},
{
    "word": "lien",
    "pronunciation": "/liːn/",
    "part_of_speech": "n.",
    "translation": "留置權",
    "example_sentence": "The bank placed a lien on the property until the loan was paid off.",
    "example_translation": "在貸款還清之前，銀行對該房產擁有留置權。",
    "difficulty_level": 5,
    "related_category": "法律，財務"
},
{
    "word": "prospectus",
    "pronunciation": "/prəˈspɛktəs/",
    "part_of_speech": "n.",
    "translation": "招股說明書",
    "example_sentence": "Investors should read the prospectus carefully before buying shares.",
    "example_translation": "投資者在購買股票前應仔細閱讀招股說明書。",
    "difficulty_level": 5,
    "related_category": "投資，財務"
},
{
    "word": "reconciliation",
    "pronunciation": "/ˌrɛkənˌsɪliˈeɪʃən/",
    "part_of_speech": "n.",
    "translation": "核對，調和",
    "example_sentence": "Monthly bank reconciliation is a critical part of the accounting process.",
    "example_translation": "每月的銀行核對是會計流程中至關重要的一部分。",
    "difficulty_level": 5,
    "related_category": "會計，財務"
},
{
    "word": "stipulate",
    "pronunciation": "/ˈstɪpjəˌleɪt/",
    "part_of_speech": "v.",
    "translation": "規定，約定",
    "example_sentence": "The contract stipulates that the project must be completed by the end of the year.",
    "example_translation": "合約規定專案必須在年底前完成。",
    "difficulty_level": 4,
    "related_category": "合約，法律"
}
        ]

        all_words = easy_words + hard_words
        
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
