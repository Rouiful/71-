from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, Question, ReadingPassage, ListeningMaterial, REJECTION_REASON_CHOICES

# ---- User 管理 ----
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'nickname', 'is_staff', 'point']
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nickname', 'point')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, CustomUserAdmin)

# ---- Question 管理 ----
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'part', 'question_type', 'difficulty_level')
    list_filter = ('part', 'question_type', 'difficulty_level')
    search_fields = ('question_text',)

admin.site.register(Question, QuestionAdmin)

# ---- 自訂表單 for ReadingPassage ----
class ReadingPassageForm(forms.ModelForm):
    class Meta:
        model = ReadingPassage
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_approved = cleaned_data.get('is_approved')
        if is_approved:
            cleaned_data['rejection_reason'] = None
        return cleaned_data

@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    form = ReadingPassageForm
    list_display = ('title', 'reading_level', 'topic', 'is_approved', 'rejection_reason', 'created_at')
    list_filter = ('reading_level', 'is_approved')
    search_fields = ('title', 'content')
    list_editable = ('is_approved',)

# ---- 自訂表單 for ListeningMaterial ----
class ListeningMaterialForm(forms.ModelForm):
    class Meta:
        model = ListeningMaterial
        fields = '__all__'
        widgets = {
            'rejection_reason': forms.Select(choices=REJECTION_REASON_CHOICES)
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_approved'):
            cleaned_data['rejection_reason'] = None
        return cleaned_data

@admin.register(ListeningMaterial)
class ListeningMaterialAdmin(admin.ModelAdmin):
    form = ListeningMaterialForm
    list_display = ('listening_level', 'topic', 'is_approved', 'rejection_reason', 'created_at')
    list_filter = ('listening_level', 'is_approved')
    search_fields = ('transcript', 'topic')
    list_editable = ('is_approved',)
