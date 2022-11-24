from django.contrib import admin

# Register your models here.
from .models import Result, AiModel, AiModelStat
from django.db import connection


# 관리에서 Result 객체에 대해  기본 CRUD 관리를 한다.

class ResultAdmin(admin.ModelAdmin) :
    list_display = ('id', 'pub_date', 'is_correct_answer', 'aimodel')
admin.site.register(Result,ResultAdmin)

# class AiModelAdmin(admin.ModelAdmin) :
#     list_display = ('id', 'version','is_selected','pub_date')
# admin.site.register(AiModel,AiModelAdmin)

@admin.register(AiModel)
class AiModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'version','is_selected','pub_date')


    def changelist_view(self, request, extra_context=None):
        # join을 아래와 같이 하는 방법은 표준은 아니지만, 개인적으로 갯수가 적을때 즐겨 사용하는 문법입니다.
        stat_queryset = AiModelStat.objects.raw("SELECT aimodel_id as id,"
                                                      " aimodel_id,"
                                                      " count(*) total_count,"
                                                      " m.version,"
                                                     " ("
                                                          " select count(*)"
                                                          "   from signlanguage_result sr"
                                                          " where sr.aimodel_id = t.aimodel_id"
                                                          " and sr.is_correct_answer = true "
                                                      " )correct_count "
                                                "  FROM signlanguage_result t, "
                                                "       signlanguage_aimodel m"
                                                " WHERE t.aimodel_id = m.id "
                                                " GROUP BY aimodel_id")

        results = []
        for stat in stat_queryset :
            # stat_row = []
            # stat_row.append(stat.aimodel_id)
            # total_ratio = stat.correct_count / stat.total_count *100
            # stat_row.append(total_ratio)
            # results.append(stat_row)
            results.append(stat)
        context = {
            'results': results,
        }

        return super().changelist_view(request, extra_context=context)
