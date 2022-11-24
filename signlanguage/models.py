from django.db import models

# Create your models here.
class AiModel(models.Model):
    ai_model = models.FileField(blank=True)
    version = models.CharField(max_length=10)
    is_selected = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
class Result(models.Model):
    aimodel = models.ForeignKey(AiModel, on_delete=models.CASCADE,null=True)
    image = models.ImageField(blank=True)
    answer = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    is_correct_answer = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

class AiModelStat(models.Model):
    ai_model_id = models.CharField(max_length=10)
    total_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    version = models.CharField(max_length=10)
    def get_correct_ratio (self):
        return self.correct_count / self.total_count *100
