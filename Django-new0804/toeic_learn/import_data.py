import json
from toeic.models import ListeningMaterial, Question # 假設您的模型在 toeic/models.py 中
from datetime import datetime
from django.utils import timezone
import uuid

# 要匯入的資料列表
data_to_import = [
    {"listening_material": {"audio_url": "", "transcript": "Question. What is the main goal of a market research survey? A: It's to analyze customer behavior. B: It helps companies understand their competitors. C: It measures public opinion on social issues.", "accent": "", "topic": "企業發展", "listening_level": "intermediate", "created_at": "2025-07-23T17:00:12.286451", "updated_at": "2025-07-23T17:00:12.286451", "is_approved": 0, "rejection_reason": "", "material_id": "3074d25d-4de3-4f67-8ad3-50c66d3f3922"}, "questions": [{"question_text": "What is the main goal of a market research survey?", "question_type": "listen", "question_category": "tense", "passage_id": None, "question_image_url": None, "part": "2", "option_a_text": "It's to analyze customer behavior.", "option_b_text": "It helps companies understand their competitors.", "option_c_text": "It measures public opinion on social issues.", "option_d_text": None, "is_correct": "A", "difficulty_level": "3", "explanation": "", "created_at": "2025-07-23T17:00:12.286451", "updated_at": "2025-07-23T17:00:12.286451", "question_id": "372804ef-29b8-4d16-accb-67f3a93b64a7", "material_id": "3074d25d-4de3-4f67-8ad3-50c66d3f3922"}]},
    {"listening_material": {"audio_url": "", "transcript": "Question. What is the main purpose of the meeting today? The marketing team has been working on a new campaign and they need to get approval from the board members. A: We'll review the proposal. B: It's time for a change. C: I think we're almost there.", "accent": "", "topic": "辦公室", "listening_level": "beginner", "created_at": "2025-07-23T17:03:15.194532", "updated_at": "2025-07-23T17:03:15.194532", "is_approved": 0, "rejection_reason": "", "material_id": "85e763f3-cc95-433d-ac7d-853f67e2739c"}, "questions": [{"question_text": "What is the main purpose of the meeting today?", "question_type": "listen", "question_category": "topic", "passage_id": None, "question_image_url": None, "part": "2", "option_a_text": "We'll review the proposal.", "option_b_text": "It's time for a change.", "option_c_text": "I think we're almost there.", "option_d_text": None, "is_correct": "A", "difficulty_level": "1", "explanation": "", "created_at": "2025-07-23T17:03:15.194532", "updated_at": "2025-07-23T17:03:15.194532", "question_id": "5443b87d-7e04-46f2-bc84-3a3eb6d52e78", "material_id": "85e763f3-cc95-433d-ac7d-853f67e2739c"}]},
    {"listening_material": {"audio_url": "", "transcript": "Question. What is the main purpose of the new laboratory equipment? A: It's for conducting experiments. B: It's for storing samples. C: It's for testing theories.", "accent": "", "topic": "技術層面", "listening_level": "intermediate", "created_at": "2025-07-23T17:04:34.708431", "updated_at": "2025-07-23T17:04:34.708431", "is_approved": 0, "rejection_reason": "", "material_id": "dba4bc53-138b-4f2a-b4cf-586db18696d9"}, "questions": [{"question_text": "What is the main purpose of the new laboratory equipment?", "question_type": "listen", "question_category": "vocab", "passage_id": None, "question_image_url": None, "part": "2", "option_a_text": "It's for conducting experiments.", "option_b_text": "It's for storing samples.", "option_c_text": "It's for testing theories.", "option_d_text": None, "is_correct": "A", "difficulty_level": "3", "explanation": "", "created_at": "2025-07-23T17:04:34.708431", "updated_at": "2025-07-23T17:04:34.708431", "question_id": "353ecb92-a3bd-494e-a928-98fc03402b03", "material_id": "dba4bc53-138b-4f2a-b4cf-586db18696d9"}]},
    {"listening_material": {"audio_url": "", "transcript": "Question. What is the main reason for installing smart home systems? The increasing demand for energy efficiency has led many homeowners to consider installing smart home systems. These systems can help reduce energy consumption and lower electricity bills. In addition, they provide a sense of security and convenience.", "accent": "", "topic": "房屋／公司地產", "listening_level": "intermediate", "created_at": "2025-07-23T17:07:23.699952", "updated_at": "2025-07-23T17:07:23.700948", "is_approved": 0, "rejection_reason": "", "material_id": "be9ba890-e331-4bf9-bee1-c1577aea3747"}, "questions": [{"question_text": "What is the main reason for installing smart home systems?", "question_type": "listen", "question_category": "tense", "passage_id": None, "question_image_url": None, "part": "2", "option_a_text": "The increasing demand for energy efficiency.", "option_b_text": "The desire to stay connected online.", "option_c_text": "The need for a better home security system.", "option_d_text": None, "is_correct": "A", "difficulty_level": "3", "explanation": "", "created_at": "2025-07-23T17:07:23.700948", "updated_at": "2025-07-23T17:07:23.700948", "question_id": "cf69eaf4-c914-4b39-be98-f76759cbb549", "material_id": "be9ba890-e331-4bf9-bee1-c1577aea3747"}]}
]

# 輔助函數：將字串時間轉換為 Django 時區感知型時間
def parse_datetime_string(dt_str):
    if dt_str:
        # 處理毫秒部分
        dt_obj = datetime.strptime(dt_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        return timezone.make_aware(dt_obj)
    return None

print("開始匯入資料...")

for entry_data in data_to_import:
    # 處理 ListeningMaterial
    lm_data = entry_data["listening_material"]
    lm_id = uuid.UUID(lm_data["material_id"]) # 將字串轉換為 UUID 物件
    
    # 檢查 ListeningMaterial 是否已存在，如果存在則更新，否則創建
    try:
        listening_material_instance = ListeningMaterial.objects.get(material_id=lm_id)
        print(f"更新 ListeningMaterial: {lm_id}")
    except ListeningMaterial.DoesNotExist:
        listening_material_instance = ListeningMaterial(material_id=lm_id)
        print(f"創建新的 ListeningMaterial: {lm_id}")

    listening_material_instance.audio_url = lm_data["audio_url"]
    listening_material_instance.transcript = lm_data["transcript"]
    listening_material_instance.accent = lm_data["accent"]
    listening_material_instance.topic = lm_data["topic"]
    listening_material_instance.listening_level = lm_data["listening_level"]
    # created_at 和 updated_at 由 Django 自動處理，或如果您需要覆蓋，請手動設置
    # For auto_now_add/auto_now fields, generally you don't set them directly unless necessary for existing data.
    # If the model has auto_now_add=True, created_at will be set on creation and cannot be changed later.
    # If auto_now=True, updated_at will be set on every save.
    # Here, we'll let Django handle them unless specifically needed for historical data preservation.
    
    # 將 0/1 轉換為 True/False
    listening_material_instance.is_approved = bool(lm_data["is_approved"])
    listening_material_instance.rejection_reason = lm_data["rejection_reason"]
    
    listening_material_instance.save()

    # 處理 Questions
    for q_data in entry_data["questions"]:
        q_id = uuid.UUID(q_data["question_id"]) # 將字串轉換為 UUID 物件
        
        try:
            question_instance = Question.objects.get(question_id=q_id)
            print(f"更新 Question: {q_id}")
        except Question.DoesNotExist:
            question_instance = Question(question_id=q_id)
            print(f"創建新的 Question: {q_id}")

        question_instance.question_text = q_data["question_text"]
        question_instance.question_type = q_data["question_type"]
        question_instance.question_category = q_data["question_category"]
        
        # 由於您提供的是 ListeningMaterial，所以 passage_id 為 None，直接設置 material
        question_instance.material = listening_material_instance 
        question_instance.passage = None # 確保 passage 是 None

        question_instance.question_image_url = q_data["question_image_url"]
        question_instance.part = q_data["part"]
        question_instance.option_a_text = q_data["option_a_text"]
        question_instance.option_b_text = q_data["option_b_text"]
        question_instance.option_c_text = q_data["option_c_text"]
        question_instance.option_d_text = q_data["option_d_text"]
        question_instance.is_correct = q_data["is_correct"]
        question_instance.difficulty_level = q_data["difficulty_level"]
        question_instance.explanation = q_data["explanation"]

        question_instance.save()

print("資料匯入完成！")