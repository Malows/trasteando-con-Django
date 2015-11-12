from django.contrib import admin
from encuestas.models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    #esto sirve para el display de tabla del admin
    list_display = ['question_text','pub_date','was_published_recently']
    #un manejo mas picante de fields, el fieldsets
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information',{'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInline]
    #lista de filtros win win
    list_filter = [ 'pub_date' ]
    #magic, pongo esto y reconoce la fecha y zap! filtros instantaneos y relacionados
    #it's a kind of magic
    search_fields = [ 'question_text' ]

admin.site.register(Question, QuestionAdmin)


#lo que hago con este ultimo cambio es hacer que dentro de question puedo agregar las choices de una
