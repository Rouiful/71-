from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from toeic.models import ReadingPassage, Question,QUESTION_CATEGORY_CHOICES
import json
from .models import ReadingPassage, Question,UserAnswer,ExamResult
from django.utils import timezone
from datetime import timedelta
from .models import Exam, ExamQuestion, ExamSession
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from django.core.paginator import Paginator

# 獲取當前使用的使用者模型
User = get_user_model()

# 首頁、使用者頁面、登入、註冊、測試頁面等不變
def home(request):
    return render(request, 'home.html', {'user': request.user})

def user(request):
    return render(request, 'user.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, '請輸入電子郵件和密碼')
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('home')
        else:
            messages.error(request, '帳號或密碼錯誤')
            return render(request, 'login.html')

    return render(request, 'login.html')

from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功！請登入。')
            return redirect('login')
        else:
            messages.error(request, '註冊失敗，請檢查表單內容。')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def test_page(request):
    return render(request, 'test.html')



# ===== 以下為去除 n8n 呼叫的 API 及頁面 =====

from django.shortcuts import render
from toeic.models import Question
import random

def reading_test(request):
    # 隨機抽取一篇已審核的文章
    passages = ReadingPassage.objects.filter(is_approved=True)  # 假設有 is_approved 欄位標示審核狀態
    if not passages.exists():
        return render(request, 'reading_test.html', {'error': '目前沒有已審核的文章'})

    passage = random.choice(passages)

    # 取得該文章的所有題目
    questions = Question.objects.filter(passage=passage)

    # 將資料包成 dict 傳給模板
    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
    }

    # 將題目轉成 list of dict，方便 JS 使用
    questions_data = []
    for q in questions:
        questions_data.append({
            'question_id': q.question_id,
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'difficulty_level': q.difficulty_level,
        })

    import json
    # 把題目序列化成JSON字串，安全傳到模板
    questions_json = json.dumps(questions_data)

    return render(request, 'reading_test.html', {
        'passage': passage_data,
        'questions_json': questions_json,
    })


@require_http_methods(["POST"])
def generate_reading_passage_api(request):
    """
    不再呼叫 n8n，直接模擬成功回應
    """
    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        reading_level = data.get('reading_level')

        if not topic or not reading_level:
            return JsonResponse({'success': False, 'error': '請提供主題和閱讀級別'})

        # 模擬生成資料
        simulated_data = {
            'passage': {
                'title': f'{topic} 文章',
                'topic': topic,
                'word_count': 120,
                'reading_level': reading_level,
                'content': f'這是一篇關於 {topic} 的 {reading_level} 文章。'
            },
            'questions': []
        }

        return JsonResponse({'success': True, 'data': simulated_data})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '無效的 JSON 格式'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'服務器錯誤: {str(e)}'})

@csrf_exempt
@require_POST
def submit_test_answer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        answers = data.get('answers')

        if not session_id or not answers:
            return JsonResponse({'success': False, 'error': '缺少 session_id 或 answers'})

        try:
            session = ExamSession.objects.get(session_id=session_id)
        except ExamSession.DoesNotExist:
            return JsonResponse({'success': False, 'error': '找不到考試紀錄'})

        if session.status == 'completed':
            return JsonResponse({'success': False, 'error': '本次測驗已完成，請勿重複提交'})

        answer_time = timezone.now()
        question_details = []

        # 初始化統計
        total_questions = 0
        correct_total = 0
        reading_total = reading_correct = 0
        listen_total = listen_correct = 0

        # 取得考卷
        exam = session.exam
        exam_type = exam.exam_type

        # 儲存所有題目的文字稿
        transcripts = {}
        
        # 新增一個字典來儲存 Part 3 的題目ID和其對應的文字稿
        part3_transcripts = {}

        for qid, selected_option in answers.items():
            try:
                question = Question.objects.get(question_id=qid)
            except Question.DoesNotExist:
                continue

            is_correct = (selected_option.lower() == question.is_correct.lower())

            # 儲存每一題作答
            answer_text = ''
            if selected_option.lower() == 'a':
                answer_text = question.option_a_text
            elif selected_option.lower() == 'b':
                answer_text = question.option_b_text
            elif selected_option.lower() == 'c':
                answer_text = question.option_c_text
            elif selected_option.lower() == 'd':
                answer_text = question.option_d_text

            UserAnswer.objects.create(
                session=session,
                question=question,
                selected_options=selected_option,
                answer_text=answer_text, 
                is_correct=is_correct,
                answer_time=answer_time,
            )

            # 累加統計
            total_questions += 1
            if is_correct:
                correct_total += 1

            if question.question_type == 'reading':
                reading_total += 1
                if is_correct:
                    reading_correct += 1
            elif question.question_type == 'listen':
                listen_total += 1
                if is_correct:
                    listen_correct += 1

            # 詳解資訊
            options = [
                {'value': 'a', 'text': question.option_a_text},
                {'value': 'b', 'text': question.option_b_text},
                {'value': 'c', 'text': question.option_c_text},
                {'value': 'd', 'text': question.option_d_text},
            ]

            question_details.append({
                'question_id': str(qid),
                'question_text': question.question_text,
                'user_answer': selected_option,
                'correct_answer': question.is_correct,
                'is_correct': is_correct,
                'explanation': question.explanation,
                'options': options,
                'part': f'part{question.part}' if question.part else None,  # ✨ 新增這行：加入 part 資訊
            })
            
            # 儲存文字稿
            # Part 2 和 Part 3 的文字稿都來自 material
            # 你的 models.py 中 ListeningMaterial 應該是 material
            if question.material and question.material.transcript:
                # 這裡儲存所有題目的文字稿，但前端會根據 part 屬性決定是否顯示
                transcripts[str(qid)] = question.material.transcript

        # ... (分數計算和儲存 ExamResult 的部分保持不變)
        def calc_score(correct, total):
            return round((correct / total * 100), 2) if total else 0.0

        reading_score = calc_score(reading_correct, reading_total)
        listen_score = calc_score(listen_correct, listen_total)
        total_score = calc_score(correct_total, total_questions)

        is_passed = total_score >= float(exam.passing_score)

        # 儲存 ExamResult
        ExamResult.objects.create(
            session=session,
            total_questions=total_questions,
            correct_answers=correct_total,
            total_score=total_score,
            is_passed=is_passed,
            reading_score=reading_score,
            listen_score=listen_score,
            completed_at=timezone.now(),
        )

        # 更新 session 狀態
        session.status = 'completed'
        session.end_time = timezone.now()
        session.save()

        # 判斷測驗類型
        test_type = '閱讀測驗'
        if exam_type == 'listen':
            test_type = '聽力測驗'
        elif exam_type == 'mixed':
            test_type = '綜合測驗'
            
        # 由於 Part 3 的文字稿是多題共用，這裡我們再處理一次
        # 確保只有 Part 3 的第一題會將文字稿傳遞給前端，以利前端判斷
        final_transcripts = {}
        part3_material_ids = set()

        # 重新遍歷 question_details，將 Part 2 的文字稿直接加入，Part 3 則只加一次
        for question in question_details:
            qid = question['question_id']
            part = question.get('part')
            
            # 如果是 Part 2，直接加入
            if part == 'part2':
                if qid in transcripts:
                    final_transcripts[qid] = transcripts[qid]
            
            # 如果是 Part 3，且該 material_id 尚未處理過，才加入
            elif part == 'part3':
                try:
                    q = Question.objects.get(question_id=qid)
                    if q.material and q.material.material_id not in part3_material_ids:
                        final_transcripts[qid] = q.material.transcript
                        part3_material_ids.add(q.material.material_id)
                except Question.DoesNotExist:
                    continue

        response_data = {
            'success': True,
            'data': {
                'score': total_score,
                'correct_answers': correct_total,
                'total_questions': total_questions,
                'is_passed': is_passed,
                'reading_score': reading_score,
                'listen_score': listen_score,
                'question_details': question_details,
                'test_type': test_type,
                'transcripts': final_transcripts,  # ✨ 這裡回傳的 transcripts 是處理過的
            }
        }

        return JsonResponse(response_data)

    except Exception as e:
        print(f"Error in submit_test_answer: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

def get_listening_transcript(exam):
    """
    取得聽力測驗的文字稿
    """
    try:
        # 找到考卷中第一個有 ListeningMaterial 的題目，並取出文字稿
        first_listening_question = Question.objects.filter(
            examquestion__exam=exam,
            material__isnull=False
        ).first()

        if first_listening_question and first_listening_question.material:
            transcript = first_listening_question.material.transcript
            print(f"Transcript found: {transcript}")
            return transcript
        else:
            print("No transcript found for this exam")
            return None
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
        return None


def test_result(request):
    """
    顯示測驗結果頁面，內容不變
    """
    context = {
        'page_title': '測驗結果',
        'test_type': 'reading'
    }
    return render(request, 'result.html', context)

def all_test_view(request):
    """
    顯示綜合測驗頁面
    """
    return render(request, 'all_test.html')

def part2(request):
    part_number = 2

    # 取得所有有 Part 2 題目的考卷
    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part2.html', {'error': '目前沒有 Part 2 的考卷'})

    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    # 取出這份考卷的所有 Part 2 題目
    exam_questions = ExamQuestion.objects.filter(
        exam=exam,
        question__part=part_number
    ).select_related('question').order_by('question_order')

    # 以第一個有 material 的題目取出該段對話（ListeningMaterial）
    material = None
    questions_data = []

    for eq in exam_questions:
        q = eq.question
        if q.material:
            material = q.material
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'difficulty_level': q.difficulty_level,
            'transcript': q.material.transcript if q.material else None,  # 從 ListeningMaterial 模型獲取 transcript
        })

    if not material:
        return render(request, 'part2.html', {'error': '考卷中未找到對應音檔'})

    material_data = {
        'audio_url': material.audio_url,
        'transcript': material.transcript,
        'topic': material.topic,
        'accent': material.accent,
        'listening_level': material.listening_level,
    }

    questions_json = json.dumps(questions_data)

    # 建立使用者 session
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'material': material_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part2.html', context)

import json
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Exam, ExamQuestion, ExamSession, Question, ListeningMaterial

def part3(request):
    part_number = 3

    # 取得所有有 Part 3 題目的考卷
    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part3.html', {'error': '目前沒有 Part 3 的考卷'})

    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    # 取出這份考卷的所有 Part 3 題目
    exam_questions = ExamQuestion.objects.filter(
        exam=exam,
        question__part=part_number
    ).select_related('question').order_by('question_order')

    # 以第一個有 material 的題目取出該段對話（ListeningMaterial）
    material = None
    questions_data = []

    for eq in exam_questions:
        q = eq.question
        if not material and q.material:
            material = q.material
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'difficulty_level': q.difficulty_level,
        })

    if not material:
        return render(request, 'part3.html', {'error': '考卷中未找到對應音檔'})

    material_data = {
        'audio_url': material.audio_url,
        'transcript': material.transcript,
        'topic': material.topic,
        'accent': material.accent,
        'listening_level': material.listening_level,
    }

    questions_json = json.dumps(questions_data)

    # 建立使用者 session
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'material': material_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part3.html', context)


def part5(request):
    part_number = 5

    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part5.html', {'error': '目前沒有 Part 5 的考卷'})
    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    for eq in exam_questions:
        q = eq.question
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'difficulty_level': q.difficulty_level,
        })

    import json
    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part5.html', context)

def part6(request):
    part_number = 6

    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part6.html', {'error': '目前沒有 Part 6 的考卷'})
    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    passage = None
    for eq in exam_questions:
        q = eq.question
        if not passage and q.passage:
            passage = q.passage
        questions_data.append({
            'question_id': str(q.question_id),  # <-- 轉字串
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'difficulty_level': q.difficulty_level,
        })

    if not passage:
        return render(request, 'part6.html', {'error': '考卷中未找到對應文章'})

    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
    }

    import json
    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'passage': passage_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part6.html', context)



def part7(request):
    part_number = 7

    # 取得所有有 Part 7 題目的考卷
    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part7.html', {'error': '目前沒有 Part 7 的考卷'})

    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    # 取出這份考卷的所有 Part 7 題目
    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    passage = None
    for eq in exam_questions:
        q = eq.question
        if not passage and q.passage:
            passage = q.passage
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'difficulty_level': q.difficulty_level,
        })

    if not passage:
        return render(request, 'part7.html', {'error': '考卷中未找到對應文章'})

    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
    }

    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'passage': passage_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,  # <--- 傳給前端
    }
    return render(request, 'part7.html', context)


def exam_part_view(request, part_number):
    # 取得包含該 part 的所有考卷 ID（exam_id 是你的主鍵名稱）
    exam_ids_with_part = ExamQuestion.objects.filter(
        question__part=part_number
    ).values_list('exam_id', flat=True).distinct()

    if not exam_ids_with_part:
        return render(request, 'no_exam_found.html', {'part': part_number})

    selected_exam_id = random.choice(list(exam_ids_with_part))
    selected_exam = Exam.objects.get(exam_id=selected_exam_id)

    part_questions = ExamQuestion.objects.filter(
        exam=selected_exam, question__part=part_number
    ).select_related('question').order_by('question_order')

    # 對應每個 part 要使用的模板
    template_map = {
        2: 'part2.html',
        3: 'part3.html',
        5: 'part5.html',
        6: 'part6.html',
        7: 'part7.html',
    }
    template_name = template_map.get(part_number, 'default_exam_part.html')

    context = {
        'exam': selected_exam,
        'questions': [eq.question for eq in part_questions],
        'part': part_number,
    }
    return render(request, template_name, context)


@csrf_exempt
def update_exam_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        new_status = data.get('status')

        try:
            session = ExamSession.objects.get(session_id=session_id)

            # 根據狀態更新欄位
            if new_status == 'in_progress':
                session.status = 'in_progress'
                session.start_time = timezone.now()
            elif new_status == 'completed':
                session.status = 'completed'
                session.end_time = timezone.now()

            session.save()
            return JsonResponse({'success': True})
        except ExamSession.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Session not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})    

@login_required
def record(request):
    user = request.user

    # 歷史測驗紀錄
    exam_results = (
        ExamResult.objects
        .filter(session__user=user)
        .order_by('-completed_at')
        .select_related('session__exam')
    )

    # 設定每頁顯示的筆數 (可以根據需求修改)
    items_per_page = 15  # 或者 items_per_page = 20

    # 建立 Paginator 物件
    paginator = Paginator(exam_results, items_per_page)

    # 取得目前頁碼
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 為每個 ExamResult 物件增加 part_display 屬性
    for result in page_obj:
        result.part_display = result.session.exam.get_part_display()

    # 閱讀作答情況
    reading_total = UserAnswer.objects.filter(session__user=user, question__question_type='reading').count()
    reading_correct = UserAnswer.objects.filter(session__user=user, question__question_type='reading', is_correct=True).count()

    # 聽力作答情況
    listening_total = UserAnswer.objects.filter(session__user=user, question__question_type='listen').count()
    listening_correct = UserAnswer.objects.filter(session__user=user, question__question_type='listen', is_correct=True).count()

    # 計算百分比
    reading_progress = int((reading_correct / reading_total) * 100) if reading_total else 0
    listening_progress = int((listening_correct / listening_total) * 100) if listening_total else 0

    # 總學習時數
    total_answers = UserAnswer.objects.filter(session__user=user).count()
    study_hours = round(total_answers / 60, 1)  # 1題1分鐘，60題=1小時

    # --- 新增：按題目類別分析作答情況 ---
    category_performance = {}
    # 獲取 Question 模型中定義的題目類別選項，用於顯示名稱
    category_choices_dict = dict(QUESTION_CATEGORY_CHOICES)

    # 遍歷所有題目類別
    for category_key, category_display_name in QUESTION_CATEGORY_CHOICES:
        # 篩選出屬於當前類別的使用者作答
        # 注意：這裡的篩選是針對所有 question_type 的，因為 category 是 question 的屬性
        category_answers = UserAnswer.objects.filter(
            session__user=user,
            question__question_category=category_key
        )

        total_in_category = category_answers.count()
        correct_in_category = category_answers.filter(is_correct=True).count()

        percentage_in_category = int((correct_in_category / total_in_category) * 100) if total_in_category else 0

        category_performance[category_key] = {
            'display_name': category_display_name,
            'total': total_in_category,
            'correct': correct_in_category,
            'percentage': percentage_in_category,
        }
    # --- 新增結束 ---

    context = {
        'user': user,
        'page_obj': page_obj,  # 使用 page_obj 傳遞分頁後的 ExamResult 物件
        'reading_progress': reading_progress,
        'listening_progress': listening_progress,
        'study_hours': study_hours,
        'reading_total': reading_total,
        'reading_correct': reading_correct,
        'listening_total': listening_total,
        'listening_correct': listening_correct,
        'category_performance': category_performance,
        'learning_suggestions': get_learning_suggestions(category_performance),

    }
    return render(request, 'record.html', context)

def get_learning_suggestions(category_performance):
    suggestions = []
    for key, data in category_performance.items():
        if data['percentage'] < 60:  # 錯太多了！
            suggestions.append(f"你在「{data['display_name']}」類別正確率較低，建議多加強相關文法或單字練習。")
        elif data['percentage'] < 80:
            suggestions.append(f"你在「{data['display_name']}」類別有待提升，可複習該類題型的解題技巧。")
    if not suggestions:
        suggestions.append("太棒了！你目前表現穩定，請持續保持並多挑戰進階題目。")
    return suggestions