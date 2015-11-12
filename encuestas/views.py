from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from encuestas.models import Question, Choice


class IndexView( generic.ListView ):
    template_name = "encuestas/index.html"
    context_object_name = "ultimas_encuestas"
    def get_queryset(self):
        """Devuelve las ultimas cinco encuestas creadas
        (sin incluir las encuestas con fechas futuras)."""
        now = timezone.now()
        orden = '-pub_date'
        return Question.objects.filter( pub_date__lte = now ).order_by( orden )[:5]

class DetallesView( generic.DetailView ):
    model = Question
    template_name = 'encuestas/detalles.html'
    def get_queryset(self):
        """ Excludes any questions that aren’t published yet. """
        return Question.objects.filter( pub_date__lte = timezone.now() )

class ResultadosView( generic.DetailView ):
    model = Question
    template_name = 'encuestas/resultados.html'
    def get_queryset(self):
        """ Excluye todas las preguntas que tengan publicación futura. """
        return Question.objects.filter( pub_date__lte = timezone.now() )

def votos( request, question_id ):
    encuesta = get_object_or_404( Question, pk = question_id )
    try:
        selected_choice = encuesta.choice_set.get( pk = request.POST[ 'choice' ])
    except ( KeyError, Choice.DoesNotExist ): #revisa que no levante el error de no existir choice en POST o la choice en la db
        # Redisplay the question voting form.
        return render( request, "encuestas/votos.html", { "question": encuesta, "error_message": "No seleccionaste una respuesta válida", } )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    #Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect( reverse( "encuestas:resultados", args = ( encuesta.id, ) ) )
# Create your views here.
