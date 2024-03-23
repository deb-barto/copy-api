from django.db import models
class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class MRRReport(models.Model):
    date_generated = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return f"Relatório MRR gerado em {self.date_generated.strftime('%Y-%m-%d %H:%M')}"