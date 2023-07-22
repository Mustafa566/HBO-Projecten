from django.contrib import admin
from .models import *


class OpenQAdmin(admin.ModelAdmin):
    list_display = (
        "question_id",
        "question_text",
        "is_hidden",
    )


class MultipleChoiceQAdmin(admin.ModelAdmin):
    list_display = (
        "mc_id",
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "is_hidden",
    )


class AdministratorAdmin(admin.ModelAdmin):
    list_display = (
        "admin_id",
        "email",
        "last_name",
        "first_name",
        "is_admin",
    )


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "team_member_id",
        "email",
        "last_name",
        "first_name",
        "is_admin",
    )


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        "survey_id",
        "admin",
        "title",
        "description",
        "is_anonymous",
        "date_sent",
        "get_open_q",
        "get_mc_q",
        "url",
    )

    # Gets a list from all open and mc questions for survey model
    def get_open_q(self, obj):
        return ", ".join([q.question_text for q in obj.open_q.all()])
    get_open_q.short_description = "OpenQ"

    def get_mc_q(self, obj):
        return ", ".join([q.question_text for q in obj.mc_q.all()])
    get_mc_q.short_description = "MultipleChoiceQ"


class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "response_id",
        "survey",
        "tm_email",
        "get_answers",
        "date_submitted",
    )

    def get_answers(self, obj):
        return ", ".join([q.question_text for q in obj.answers.all()])
    get_answers.short_description = "openQuestions"


admin.site.register(OpenQ, OpenQAdmin)
admin.site.register(MultipleChoiceQ, MultipleChoiceQAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
