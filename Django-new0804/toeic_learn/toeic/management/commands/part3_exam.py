from django.core.management.base import BaseCommand
from toeic.models import Exam, ExamQuestion, ListeningMaterial, Question

class Command(BaseCommand):
    help = 'Generate Exam and ExamQuestions for all listening materials, all questions included.'

    def handle(self, *args, **options):
        self.stdout.write("開始建立聽力 Exam 與 ExamQuestion ...")

        materials = ListeningMaterial.objects.all()
        for material in materials:
            part = None
            first_question = material.question_set.first()
            if first_question:
                part = first_question.part
            if part is None:
                self.stdout.write(f"跳過聽力 {material.topic}，無法取得 part")
                continue

            # Exam title 加上 material_id，確保唯一
            exam_title = f"Listening Exam for Part {part} - {material.topic} ({material.material_id})"
            exam, created = Exam.objects.get_or_create(
                title=exam_title,
                defaults={
                    'description': "自動建立的聽力測驗",
                    'exam_type': 'toeic',
                    'part': part,
                    'duration_minutes': 45,
                    'total_questions': material.question_set.count(),
                    'passing_score': 70.0,
                    'is_active': True,
                }
            )
            if not created:
                self.stdout.write(f"{exam_title} 已存在，跳過建立")
                continue

            questions = material.question_set.all().order_by('created_at')
            for idx, question in enumerate(questions, start=1):
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    question_order=idx,
                    scores=1.0,
                )
            self.stdout.write(f"建立 {exam_title}，共 {questions.count()} 題成功")

        self.stdout.write("全部聽力 Exam 建立完成！")