from rest_framework import serializers
from .models import CustomUser, HomeworkNote, HomeworkComment, StudyGroup, Message, QuizFolder, Quiz, QuizAttempt
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'school_year', 'subjects')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            school_year=validated_data.get('school_year',''),
            subjects=validated_data.get('subjects',''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username','email','school_year','subjects')

class HomeworkCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = HomeworkComment
        fields = ('id','author','text','created_at')


class HomeworkNoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = HomeworkCommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = HomeworkNote
        fields = ('id','author','grade','subject','category','note_type','content','likes_count','liked','comments','created_at')

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'author', 'author_id', 'text', 'timestamp')

    def get_author(self, obj):
        return {'username': obj.author.username} if obj.author else None

class StudyGroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_member = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = ('id','name','subject','owner','is_member','is_owner')

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(pk=request.user.pk).exists()
        return False

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner is not None and obj.owner.pk == request.user.pk
        return False


class QuizSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    num_questions = serializers.SerializerMethodField()
    attempts_count = serializers.IntegerField(source='attempts.count', read_only=True)

    class Meta:
        model = Quiz
        fields = ('id','title','content','created_at','created_by','num_questions','attempts_count')

    def get_num_questions(self, obj):
        # if content stores questions as JSON list, try to parse
        try:
            import json
            data = json.loads(obj.content or 'null')
            if isinstance(data, dict) and 'questions' in data:
                return len(data.get('questions') or [])
        except Exception:
            pass
        return 0


class QuizAttemptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ('id', 'quiz', 'user', 'answers', 'score', 'created_at')


class QuizFolderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    quizzes_count = serializers.IntegerField(source='quizzes.count', read_only=True)
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)

    class Meta:
        model = QuizFolder
        fields = ('id','name','description','created_by','created_by_id','created_at','quizzes_count')


class ScheduleEventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = None  # set below to avoid circular import issues when file loaded
        fields = ('id', 'title', 'description', 'datetime', 'created_by', 'created_at')

# Attach model dynamically (import at bottom to avoid import cycles)
from .models import ScheduleEvent
ScheduleEventSerializer.Meta.model = ScheduleEvent


from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id','message','url','is_read','created_at')
