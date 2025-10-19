from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import StudyGroupSerializer, MessageSerializer, HomeworkNoteSerializer, HomeworkCommentSerializer
from .models import StudyGroup, Message, HomeworkNote, HomeworkComment
from .serializers import QuizFolderSerializer, QuizSerializer
from .models import QuizFolder, Quiz, QuizAttempt, ScheduleEvent, Notification
from .serializers import ScheduleEventSerializer
from .serializers import NotificationSerializer
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def schedule_list_create(request):
    if request.method == 'GET':
        events = ScheduleEvent.objects.filter(created_by=request.user).order_by('datetime')
        serializer = ScheduleEventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)
    else:
        serializer = ScheduleEventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            event = ScheduleEvent.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data.get('description',''),
                datetime=serializer.validated_data['datetime'],
                created_by=request.user
            )
            # notify other users about the new event (non-blocking)
            try:
                from .models import CustomUser
                recipients = CustomUser.objects.exclude(pk=request.user.pk)
                snippet = event.title or 'Event'
                notify_msg = f"New event: {snippet}"
                for u in recipients:
                    Notification.objects.create(user=u, message=notify_msg, url='/schedule/')
            except Exception:
                pass
            return Response(ScheduleEventSerializer(event, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def schedule_detail(request, pk):
    try:
        event = ScheduleEvent.objects.get(pk=pk, created_by=request.user)
    except ScheduleEvent.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    if request.method == 'GET':
        return Response(ScheduleEventSerializer(event, context={'request': request}).data)
    elif request.method == 'PUT':
        serializer = ScheduleEventSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        event.delete()
        return Response({'detail': 'Deleted'}, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_quiz_attempts(request):
    """Return a summary of the current user's quiz activity: best score, last score, attempts count, and quiz info."""
    qs = QuizAttempt.objects.filter(user=request.user).select_related('quiz', 'quiz__folder').order_by('-created_at')
    summary = {}
    for a in qs:
        qid = a.quiz.id
        if qid not in summary:
            summary[qid] = {
                'quiz': {'id': a.quiz.id, 'title': a.quiz.title, 'folder_id': a.quiz.folder.id if a.quiz.folder else None, 'folder_name': a.quiz.folder.name if a.quiz.folder else ''},
                'best_score': a.score,
                'last_score': a.score,
                'attempts_count': 1,
                'last_attempt_at': a.created_at,
            }
        else:
            entry = summary[qid]
            entry['attempts_count'] += 1
            entry['last_score'] = a.score
            # update best_score if this attempt is higher (None-safe)
            try:
                if a.score is not None and (entry['best_score'] is None or a.score > entry['best_score']):
                    entry['best_score'] = a.score
            except Exception:
                pass
            # last_attempt_at already set by order
    # return as list
    out = list(summary.values())
    return Response(out)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # For simplicity, just perform client-side token deletion. Server-side blacklist not configured.
        django_logout(request)
        return Response({'detail':'Logged out'}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

# Frontend views
def frontend_login(request):
    # If POST from the login form (traditional form submit), attempt Django session login
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # If authentication by username failed, try to authenticate by email lookup
        if user is None:
            try:
                user_obj = CustomUser.objects.get(email=username)
            except CustomUser.DoesNotExist:
                user_obj = None
            if user_obj is not None:
                user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('dashboard')
        else:
            # Render template with error
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    # serve the existing static login page as template
    return render(request, 'login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    # fetch user's notes to show on the dashboard
    from .models import HomeworkNote
    notes = HomeworkNote.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home.html', {'username': request.user.username, 'user': request.user, 'notes': notes})


def frontend_groups(request):
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    return render(request, 'groups.html', {'username': request.user.username})


def frontend_homework(request):
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    # pass user and any recent notes so the template's sidebar/profile can render
    from .models import HomeworkNote
    notes = HomeworkNote.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'homework.html', {'username': request.user.username, 'user': request.user, 'notes': notes})


def frontend_homework_preview(request):
    """Render the homework template without authentication for visual preview/testing.
    This is a dev helper and should not be used in production."""
    # pass an anonymous user placeholder and empty notes to let the template render
    class _User: id = 0; username = 'Preview'; school_year = ''
    from .models import HomeworkNote
    notes = HomeworkNote.objects.none()
    return render(request, 'homework.html', {'username': 'Preview', 'user': _User(), 'notes': notes})


def frontend_quizzes(request):
    """Render the quizzes frontend page. Requires authentication."""
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    # provide minimal context used by the template (username, user)
    return render(request, 'quizzes.html', {'username': request.user.username, 'user': request.user})


def frontend_quizzes_folder(request, pk):
    """Render a page showing quizzes inside a folder (minimal template that fetches quizzes via API)."""
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    # render a small template that will call /api/quizzes/<pk>
    return render(request, 'quizzes_folder.html', {'username': request.user.username, 'user': request.user, 'folder_id': pk})


def frontend_quiz_take(request, pk):
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    return render(request, 'quiz_take.html', {'username': request.user.username, 'user': request.user, 'quiz_id': pk})


def frontend_schedule(request):
    if not request.user.is_authenticated:
        return redirect('frontend_login')
    return render(request, 'schedule.html', {'username': request.user.username, 'user': request.user})


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def groups_list_create(request):
    if request.method == 'GET':
        qs = StudyGroup.objects.all()
        serializer = StudyGroupSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudyGroupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = StudyGroup.objects.create(
                name=serializer.validated_data['name'],
                subject=serializer.validated_data.get('subject',''),
                owner=request.user
            )
            group.members.add(request.user)
            return Response(StudyGroupSerializer(group, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def groups_join(request, pk):
    try:
        group = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    group.members.add(request.user)
    return Response(StudyGroupSerializer(group, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def groups_leave(request, pk):
    try:
        group = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    # Owner cannot leave; they should delete the group if they want
    if group.owner is not None and group.owner.pk == request.user.pk:
        return Response({'detail':'Owner cannot leave the group. Delete the group instead.'}, status=403)
    group.members.remove(request.user)
    return Response({'detail':'Left group'}, status=200)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def groups_delete(request, pk):
    try:
        group = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    # Only owner can delete
    if group.owner is None or group.owner.pk != request.user.pk:
        return Response({'detail':'Only the owner can delete this group.'}, status=403)
    group.delete()
    return Response({'detail':'Deleted'}, status=200)


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def group_messages(request, pk):
    try:
        group = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    # Only members can view or post messages
    if not group.members.filter(pk=request.user.pk).exists():
        return Response({'detail':'You must join the group to view or post messages.'}, status=403)
    if request.method == 'GET':
        qs = group.messages.order_by('created_at')
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)
    else:
        text = request.data.get('text','')
        if not text:
            return Response({'text':'This field is required.'}, status=400)
        msg = Message.objects.create(group=group, author=request.user, text=text)
        # create notifications for other group members (simple per-user rows)
        try:
            members = group.members.exclude(pk=request.user.pk)
            if isinstance(text, str):
                snippet = text if len(text) <= 120 else text[:117] + '...'
            else:
                snippet = str(text)[:120]
            note_text = f"New message in group '{group.name}': {snippet}"
            for m in members:
                Notification.objects.create(user=m, message=note_text, url=f"/groups/{group.id}/")
        except Exception:
            # don't fail message creation if notifications fail
            pass
        return Response(MessageSerializer(msg).data, status=201)


# Homework endpoints
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def homework_list_create(request):
    if request.method == 'GET':
        qs = HomeworkNote.objects.all().order_by('-created_at')
        # filters
        grade = request.GET.get('grade')
        subject = request.GET.get('subject')
        category = request.GET.get('category')
        note_type = request.GET.get('note_type')
        if grade: qs = qs.filter(grade=grade)
        if subject: qs = qs.filter(subject__iexact=subject)
        if category: qs = qs.filter(category=category)
        if note_type: qs = qs.filter(note_type=note_type)
        serializer = HomeworkNoteSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
    else:
        serializer = HomeworkNoteSerializer(data=request.data)
        if serializer.is_valid():
            note = HomeworkNote.objects.create(
                author=request.user,
                grade=serializer.validated_data.get('grade',9),
                subject=serializer.validated_data.get('subject',''),
                category=serializer.validated_data.get('category','Q'),
                note_type=serializer.validated_data.get('note_type','HW'),
                content=serializer.validated_data.get('content','')
            )
            # notify other users about the new homework (non-blocking)
            try:
                from .models import CustomUser
                recipients = CustomUser.objects.exclude(pk=request.user.pk)
                snippet = (note.content or '')
                if len(snippet) > 120:
                    snippet = snippet[:117] + '...'
                notify_msg = f"New homework posted: {snippet or note.subject or 'Homework'}"
                for u in recipients:
                    Notification.objects.create(user=u, message=notify_msg, url='/homework/')
            except Exception:
                pass
            return Response(HomeworkNoteSerializer(note, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def homework_detail(request, pk):
    try:
        note = HomeworkNote.objects.get(pk=pk)
    except HomeworkNote.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    if request.method == 'GET':
        serializer = HomeworkNoteSerializer(note, context={'request': request})
        return Response(serializer.data)
    else:
        # delete only by author
        if note.author.pk != request.user.pk:
            return Response({'detail':'Only the author can delete this note.'}, status=403)
        note.delete()
        return Response({'detail':'Deleted'}, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def homework_like(request, pk):
    try:
        note = HomeworkNote.objects.get(pk=pk)
    except HomeworkNote.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    if request.user in note.likes.all():
        note.likes.remove(request.user)
        return Response({'liked': False, 'likes_count': note.likes.count()})
    else:
        note.likes.add(request.user)
        return Response({'liked': True, 'likes_count': note.likes.count()})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def homework_comment_create(request, pk):
    try:
        note = HomeworkNote.objects.get(pk=pk)
    except HomeworkNote.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    text = request.data.get('text','').strip()
    if not text:
        return Response({'text':'This field is required.'}, status=400)
    comment = HomeworkComment.objects.create(note=note, author=request.user, text=text)
    return Response(HomeworkCommentSerializer(comment).data, status=201)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def homework_comment_delete(request, pk):
    try:
        comment = HomeworkComment.objects.get(pk=pk)
    except HomeworkComment.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    if comment.author.pk != request.user.pk:
        return Response({'detail':'Only the author can delete this comment.'}, status=403)
    comment.delete()
    return Response({'detail':'Deleted'}, status=200)


# Allow owners to edit group metadata
@api_view(['PUT','PATCH'])
@permission_classes([permissions.IsAuthenticated])
def groups_edit(request, pk):
    try:
        group = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    if group.owner is None or group.owner.pk != request.user.pk:
        return Response({'detail':'Only the owner can edit this group.'}, status=403)
    serializer = StudyGroupSerializer(group, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# Message detail: edit/delete by author
@api_view(['PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def message_detail(request, pk):
    try:
        msg = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    # Only author may edit or delete
    if msg.author.pk != request.user.pk:
        return Response({'detail':'Only the author can modify this message.'}, status=403)
    if request.method == 'PUT':
        text = request.data.get('text','').strip()
        if not text:
            return Response({'text':'This field is required.'}, status=400)
        msg.text = text
        msg.save()
        return Response(MessageSerializer(msg).data)
    else:
        msg.delete()
        return Response({'detail':'Deleted'}, status=200)


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_folders_list_create(request):
    if request.method == 'GET':
        qs = QuizFolder.objects.all().order_by('-created_at')
        serializer = QuizFolderSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
    else:
        serializer = QuizFolderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                folder = QuizFolder.objects.create(
                    name=serializer.validated_data.get('name',''),
                    description=serializer.validated_data.get('description',''),
                    created_by=request.user
                )
            except Exception as e:
                # Return a simple error payload so frontend can show details
                return Response({'detail': str(e)}, status=500)
            return Response(QuizFolderSerializer(folder, context={'request': request}).data, status=201)
        return Response({'detail': serializer.errors}, status=400)


@api_view(['GET','DELETE','PUT','PATCH'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_folder_detail(request, pk):
    try:
        folder = QuizFolder.objects.get(pk=pk)
    except QuizFolder.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    if request.method == 'GET':
        serializer = QuizFolderSerializer(folder, context={'request': request})
        return Response(serializer.data)
    # Only owner/creator can delete or update
    if folder.created_by is None or folder.created_by.pk != request.user.pk:
        return Response({'detail':'Only the creator can modify this folder.'}, status=403)
    if request.method == 'DELETE':
        folder.delete()
        return Response({'detail':'Deleted'}, status=200)
    # update
    serializer = QuizFolderSerializer(folder, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({'detail': serializer.errors}, status=400)


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_list_create(request):
    if request.method == 'GET':
        qs = Quiz.objects.all().order_by('-created_at')
        serializer = QuizSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
    # create quiz
    data = request.data.copy()
    # if questions are passed in, store them in content as JSON
    try:
        import json
        if 'questions' in data:
            data['content'] = json.dumps({'questions': data.pop('questions')})
    except Exception:
        pass
    serializer = QuizSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        folder_id = request.data.get('folder_id')
        try:
            folder = QuizFolder.objects.get(pk=folder_id)
        except Exception:
            return Response({'detail':'Folder not found'}, status=400)
        # Only the folder creator may create quizzes inside it
        try:
            if folder.created_by is None or folder.created_by.pk != request.user.pk:
                return Response({'detail':'Only the folder creator can add quizzes.'}, status=403)
        except Exception:
            return Response({'detail':'Permission check failed'}, status=403)
        quiz = Quiz.objects.create(
            folder=folder,
            title=serializer.validated_data.get('title',''),
            content=serializer.validated_data.get('content',''),
            created_at=serializer.validated_data.get('created_at', None)
        )
        # set created_by if model supports it
        try:
            quiz.created_by = request.user
            quiz.save()
        except Exception:
            pass
        # notify other users about the new quiz (non-blocking)
        try:
            from .models import CustomUser
            recipients = CustomUser.objects.exclude(pk=request.user.pk)
            snippet = quiz.title or 'Quiz'
            notify_msg = f"New quiz posted: {snippet}"
            for u in recipients:
                Notification.objects.create(user=u, message=notify_msg, url=f"/quizzes/{quiz.id}/")
        except Exception:
            pass
        return Response(QuizSerializer(quiz, context={'request': request}).data, status=201)
    return Response({'detail': serializer.errors}, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    serializer = QuizSerializer(quiz, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_in_folder_v2(request, pk):
    try:
        folder = QuizFolder.objects.get(pk=pk)
    except QuizFolder.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    qs = folder.quizzes.order_by('-created_at')
    serializer = QuizSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quizzes_in_folder(request, pk):
    try:
        folder = QuizFolder.objects.get(pk=pk)
    except QuizFolder.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    qs = folder.quizzes.order_by('-created_at')
    serializer = QuizSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def quiz_submit_attempt(request, pk):
    """Submit an attempt for quiz `pk`. Expects JSON body with `answers` (list or dict).
    A naive scoring is applied: if quiz content stores questions with `correct` index, compare answers.
    """
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    data = request.data.copy()
    import json
    answers = data.get('answers', None)
    try:
        answers_json = json.dumps(answers)
    except Exception:
        answers_json = json.dumps({'answers': answers})

    # attempt naive scoring
    score = None
    try:
        content = json.loads(quiz.content or 'null')
        questions = content.get('questions') if isinstance(content, dict) else None
        if isinstance(questions, list) and isinstance(answers, (list, dict)):
            total = len(questions)
            correct = 0
            for idx, q in enumerate(questions):
                correct_idx = q.get('correct') if isinstance(q, dict) else None
                user_ans = answers[idx] if isinstance(answers, list) and idx < len(answers) else answers.get(str(idx)) if isinstance(answers, dict) else None
                if correct_idx is not None and str(user_ans) == str(correct_idx):
                    correct += 1
            score = (correct / total) * 100 if total > 0 else 0
    except Exception:
        score = None

    attempt = QuizAttempt.objects.create(quiz=quiz, user=request.user, answers=answers_json, score=score)
    return Response({'id': attempt.id, 'score': attempt.score}, status=201)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quiz_leaderboard(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    qs = quiz.attempts.order_by('-score', 'created_at')[:20]
    # return user and score
    out = [{'user': {'id': a.user.id, 'username': a.user.username}, 'score': a.score, 'created_at': a.created_at} for a in qs]
    # find current user's rank (simple, counting better scores)
    my_rank = None
    try:
        my_best = quiz.attempts.filter(user=request.user).order_by('-score').first()
        if my_best:
            better = quiz.attempts.filter(score__gt=my_best.score).count()
            my_rank = better + 1
    except Exception:
        my_rank = None
    return Response({'leaderboard': out, 'my_rank': my_rank})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications_list(request):
    qs = request.user.notifications.all()
    serializer = NotificationSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notification_mark_read(request, pk):
    try:
        n = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response({'detail':'Not found'}, status=404)
    n.is_read = True
    n.save()
    return Response({'detail':'Marked read'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notifications_seed_for_user(request):
    """Dev helper: create a test notification for the current user."""
    try:
        n = Notification.objects.create(user=request.user, message='Test notification (personal)', url='/')
        return Response({'detail':'Created','id': n.id}, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notifications_seed_all(request):
    """Dev helper (staff only): seed a test notification for all users."""
    if not request.user.is_staff:
        return Response({'detail':'Forbidden'}, status=403)
    try:
        from .models import CustomUser
        count = 0
        for u in CustomUser.objects.exclude(pk=request.user.pk):
            Notification.objects.create(user=u, message='Test notification (all users)', url='/')
            count += 1
        return Response({'detail':'Created','count': count}, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notifications_create(request):
    """Create a notification for the current user. Payload: { message: str, url: str (optional) }"""
    message = request.data.get('message') or request.data.get('msg')
    url = request.data.get('url', '')
    if not message:
        return Response({'detail': 'message is required'}, status=400)
    try:
        n = Notification.objects.create(user=request.user, message=message, url=url)
        return Response({'id': n.id, 'message': n.message, 'created_at': n.created_at}, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notifications_mark_all_read(request):
    """Mark all notifications for the current user as read."""
    qs = request.user.notifications.filter(is_read=False)
    updated = qs.update(is_read=True)
    return Response({'detail': 'Marked all read', 'count': updated})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def notifications_trigger_event_sweep(request):
    """Manually trigger the event notifier sweep (for testing). Staff only."""
    if not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=403)
    # reuse the management command logic inline to avoid overhead
    from django.utils import timezone
    now = timezone.now()
    due = ScheduleEvent.objects.filter(datetime__lte=now, notified=False)
    created = 0
    for ev in due:
        try:
            recipients = CustomUser.objects.exclude(pk=ev.created_by.pk)
            msg = f"Event starting: {ev.title}"
            for u in recipients:
                Notification.objects.create(user=u, message=msg, url=f"/schedule/{ev.id}/")
            ev.notified = True
            ev.save()
            created += recipients.count()
        except Exception:
            pass
    return Response({'detail': 'Triggered', 'events': due.count(), 'notifications_created': created})
