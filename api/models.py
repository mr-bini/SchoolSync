from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    SCHOOL_YEARS = (
        ('9', '9th'),
        ('10', '10th'),
        ('11', '11th'),
        ('12', '12th'),
    )
    school_year = models.CharField(max_length=2, choices=SCHOOL_YEARS, blank=True)
    subjects = models.CharField(max_length=200, blank=True, help_text='Comma-separated subjects')

class HomeworkNote(models.Model):
    CATEGORY_CHOICES = [
        ('Q', 'Question'),
        ('T', 'Tip'),
        ('R', 'Resource'),
    ]
    TYPE_CHOICES = [
        ('HW', 'Homework'),
        ('EX', 'Exam Prep'),
        ('GEN', 'General'),
    ]

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
    grade = models.IntegerField(choices=[(i, str(i)) for i in range(9, 13)], default=9)
    subject = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='Q')
    note_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='HW')
    content = models.TextField(blank=True, default='')
    likes = models.ManyToManyField(CustomUser, related_name='liked_notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note {self.id} by {self.author.username}"


class HomeworkComment(models.Model):
    note = models.ForeignKey(HomeworkNote, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='homework_comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on {self.note.id} by {self.author.username}"


class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='owned_groups', blank=True)
    members = models.ManyToManyField(CustomUser, related_name='study_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group {self.name}"


class Message(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in {self.group.name} by {self.author.username}"


class QuizFolder(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='quiz_folders', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QuizFolder {self.name}"


class Quiz(models.Model):
    folder = models.ForeignKey(QuizFolder, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='quizzes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz {self.title} in {self.folder.name}"


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts')
    # store answers/attempt payload as JSON text
    answers = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'created_at']

    def __str__(self):
        return f"Attempt by {self.user.username} on {self.quiz.title}"


class ScheduleEvent(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedule_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.title} at {self.datetime} by {self.created_by.username}"


class Notification(models.Model):
    """Simple per-user notification model for site updates."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=500)
    url = models.CharField(max_length=300, blank=True, default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.user.username}: {self.message[:40]}"
