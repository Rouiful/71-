from django.core.management.base import BaseCommand
from toeic.models import Exam, ExamQuestion, ListeningMaterial, Question
import math
import uuid

class Command(BaseCommand):
    help = 'Generate Exam and ExamQuestions for Part 2 (4 questions per exam)'

    def handle(self, *args, **options):
        self.stdout.write("開始建立 Part 2 Exam（每份 4 題）...")

        # 取得所有 part 2 題目，依照 material 分群，照時間排序（穩定）
        part2_questions = Question.objects.filter(part=2).order_by('created_at')
        total_questions = part2_questions.count()

        if total_questions < 4:
            self.stdout.write("Part 2 題目數量不足 4 題，無法建立考卷。")
            return

        group_count = math.ceil(total_questions / 4)
        self.stdout.write(f"總共找到 {total_questions} 題 Part 2 題目，預計建立 {group_count} 份考卷")

        for i in range(group_count):
            exam_questions = part2_questions[i * 4:(i + 1) * 4]

            if not exam_questions:
                continue

            exam_title = f"Part 2 Listening Test {i + 1}"
            exam = Exam.objects.create(
                title=exam_title,
                description="自動產生的 Part 2 測驗",
                exam_type='listen',
                part=2,
                duration_minutes=20,
                total_questions=exam_questions.count(),
                passing_score=60,
                is_active=True,
            )

            for order, question in enumerate(exam_questions, start=1):
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    question_order=order,
                    scores=1.0,
                )

            self.stdout.write(f"✅ 已建立：{exam_title}（共 {exam_questions.count()} 題）")

        self.stdout.write("🎉 所有 Part 2 測驗建立完成！")
