from django.test import TestCase
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone

from encuestas.models import Question

# Create your tests here.

#helper function

def create_question( question_text, days ):
    """ Crea una encuesta con los valores dados de 'question_text'
    publicada hace un numero de 'days'
    (negativo para dias en el pasado, positivo para dias en el futuro). """
    time = timezone.now() + datetime.timedelta( days = days )
    return Question.objects.create( question_text = question_text, pub_date = time)

def create_choice( choice_text, votes, question ):
    
    return Choice.objects.create( choice_text = choice_text, vote = votes, question = question )

#clases

class QuestionMethodTest( TestCase ):
    def test_was_published_recently_con_encuestas_futuras( self ):
        """was_published_recently() deberia devolver falso para preguntas que
        tienen fecha de publicacion en el futuro."""
        time = timezone.now() + datetime.timedelta( days = 30 )
        future_question = Question( pub_date = time )
        self.assertEqual( future_question.was_published_recently(), False )

    def test_was_published_recently_con_encuestas_viejas( self ):
        """was_published_recently() deberia devolver falso para preguntas que
        fechas de publicacion con más de un día de antiguedad."""
        time = timezone.now() - datetime.timedelta( days = 30 )
        old_question = Question( pub_date = time )
        self.assertEqual( old_question.was_published_recently(), False )

    def test_was_published_recently_con_encuestas_recientes( self ):
        """was_published_recently() deberia devolver Verdad para preguntas que
        pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta( hours = 1 )
        recent_question = Question( pub_date = time )
        self.assertEqual( recent_question.was_published_recently(), True )


class QuestionIndexViewTest( TestCase ):
    def test_index_view_sin_encuestas( self ):
        """ Si la pregunta existe, un mensaje apropiado debe ser mostrado. """
        respuesta = self.client.get( reverse( 'encuestas:index' ) )
        self.assertEqual( respuesta.status_code, 200 )
        self.assertContains( respuesta, 'No hay encuestas disponibles.' )
        self.assertQuerysetEqual( respuesta.context[ 'ultimas_encuestas' ], [] )

    def test_index_view_con_una_encuesta_pasada( self ):
        """ Crea una pregunta con publicacion en el pasado """
        create_question( question_text = "Pregunta pasada.", days = -30 )
        respuesta = self.client.get(reverse( 'encuestas:index' ))
        self.assertQuerysetEqual( respuesta.context[ 'ultimas_encuestas' ], [ '<Question: Pregunta pasada.>' ] )

    def test_index_view_con_una_encuesta_futura( self ):
        """ Crea una pregunta con publicacion en el futuro,
        que no debería ser mostrado en el index. """
        create_question( question_text = "Pregunta futura.", days = 30 )
        respuesta = self.client.get( reverse( 'encuestas:index' ) )
        self.assertContains( respuesta, "No hay encuestas disponibles.", status_code = 200 )
        self.assertQuerysetEqual( respuesta.context[ 'ultimas_encuestas' ], [] )

    def test_index_view_con_encuestas_pasadas_y_futuras( self ):
        """ Aunque las dos existan, solo se debería mostrar la pasada. """
        create_question( question_text = "Pregunta pasada.", days = -30 )
        create_question( question_text = "Pregunta futura.", days = 30 )
        respuesta = self.client.get( reverse( 'encuestas:index' ) )
        self.assertQuerysetEqual( respuesta.context[ 'ultimas_encuestas' ], [ '<Question: Pregunta pasada.>' ] )

    def test_index_view_con_dos_encuestas_pasadas( self ):
        """ El index debería mostrar las dos preguntas. """
        create_question( question_text = "Pregunta pasada 1.", days = -30 )
        create_question( question_text = "Pregunta pasada 2.", days = -5 )
        respuesta = self.client.get( reverse( 'encuestas:index' ) )
        self.assertQuerysetEqual( respuesta.context[ 'ultimas_encuestas' ], [ '<Question: Pregunta pasada 2.>', '<Question: Pregunta pasada 1.>' ] )

class QuestionDetallesTests( TestCase ):
    def test_detalles_view_con_una_encuesta_futura( self ):
        """ El view detalles de una Pregunta futura debería devolver un 404. """
        pregunta_futura = create_question( question_text='Pregunta futura.', days = 5 )
        respuesta = self.client.get( reverse( 'encuestas:detalles', args = ( pregunta_futura.id, ) ) )
        self.assertEqual( respuesta.status_code, 404 )

    def test_detalles_view_con_una_encuesta_pasada(self):
        """ El view detalles de una Pregunta pasada debería devolver el question_text. """
        pregunta_pasada = create_question( question_text='Pregunta pasada.', days = -5 )
        respuesta = self.client.get( reverse( 'encuestas:detalles', args = ( pregunta_pasada.id, ) ) )
        self.assertContains( respuesta, pregunta_pasada.question_text, status_code = 200 )

class QuestionResultadosTest( TestCase ):
