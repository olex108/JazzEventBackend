import logging
from urllib.request import Request

from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView, FormView

from django_filters.views import FilterView
from .filters import EventFilter, VideoFilter

from users.models import User
from content.models import LineUp, Event, Video, Image, LineUpComposition
from .forms import ClientMessageForm

from .servises.forms_services import FormsServices
from users.services.message_service import ClientMessageServices


user_loger = logging.getLogger("users")
message_loger = logging.getLogger("messages")
stats_loger = logging.getLogger("stats")


class HomeView(TemplateView):
    template_name = "content/home.html"

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to add keys for context data

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_image - path to header background image !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)

        context["line_up_list"] = LineUp.objects.all()
        context["featured_events"] = Event.objects.order_by('-priority')[:3]

        context["header_image"] = "image/header/header_home.jpg"
        context["event_video"] = "video/video_header.mp4"

        # context["home_video"] = "image/header/home_header.png"
        context["home_image"] = "image/pages/home_page_event_image.jpg"

        return context


class EventFilterListView(FilterView):
    """
    View of events list with filter by

    line_up_list - list of all line_up (count of groups) to add in page
    instruments -
    is_vocal -
    """

    model = Event
    template_name = "content/events_list.html"
    filterset_class = EventFilter
    context_object_name = "events_list"

    def get(self, request: Request, *args, **kwargs):
        stats_loger.info(f"{request.method} - {request.path} - {request.GET.dict()}")
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to order events by "priority" and filter 10 items

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_video - path to header background video !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)

        elements_list = context["events_list"]
        context["events_list"] = elements_list.filter(is_publicate=True).order_by("-priority")[:10]

        context["header_video"] = "video/video_header.mp4"

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "content/event_detail.html"
    context_object_name = "event"

    def get(self, request: Request, *args, **kwargs):
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """

        """

        context = super().get_context_data(**kwargs)

        context["event_video_list"] = self.object.videos.all()
        context["photo_list"] = self.object.images.all()
        context["header_image"] = "image/header/home_header.png"
        # 1. Берем целевое количество из связанного поля line_up
        # target_count = self.object.line_up.count
        #
        # # 2. Получаем список ID инструментов ТЕКУЩЕГО объекта (события/продукта)
        # instrument_ids = self.object.instruments.values_list('id', flat=True)
        #
        # # 3. Находим единственный состав одним запросом
        # composition = LineUpComposition.objects.filter(
        #     line_up=self.object.line_up,  # Совпадает тип лайнапа
        #     instruments__id__in=instrument_ids  # Инструменты из нашего списка
        # ).annotate(
        #     actual_count=Count('instruments')  # Считаем инструменты в найденных составах
        # ).filter(
        #     actual_count=target_count  # Сверяем с эталоном из LineUp
        # ).distinct().first()
        #
        # context["line_up_composition"] = composition
        return context


class VideoFilterListView(FilterView):
    model = Video
    template_name = "content/video_list.html"
    filterset_class = VideoFilter
    context_object_name = "video_list"

    def get(self, request: Request, *args, **kwargs):
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to order videos by "number" and filter 10 items

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_video - path to header background video !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)

        elements_list = context["video_list"]

        context["video_list"] = elements_list.order_by("-priority")[:10]

        context["header_video"] = "video/video_header.mp4"

        return context


class PhotoListView(ListView):
    model = Image
    template_name = "content/photo_list.html"
    context_object_name = "photo_list"

    def get(self, request: Request, *args, **kwargs):
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to order videos by "number" and filter 10 items

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_video - path to header background video !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)

        context["events_for_collage"] = Event.objects.order_by("-priority")[:3]

        # context["header_video"] = "video/video_header.mp4"
        context["header_image"] = "image/header/header_home.jpg"

        return context


class PriceView(FormView):

    form_class = ClientMessageForm
    template_name = "content/price_page.html"
    success_url = reverse_lazy("content:price")

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to add keys for context data

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_image - path to header background image !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)

        context["line_up_list"] = LineUp.objects.all()
        context["header_image"] = "image/header/header.jpg"
        # context["header_image"] = "image/header/home_header.png"

        return context

    def form_valid(self, form: ClientMessageForm) -> HttpResponse:
        """
        Валидация формы при заполнении полей
        Если номера телефона нет в базе данных сохраняет нового клиента и сохраняет новое сообщение
        Если номер есть в базе данных сохраняется новое сообщение с комментариями в виде реквизитов клиента

        В случае указания почты пользователю отправляется сообщение

        Реализована функция уведомления администратора через почту
        """

        selected_plan = self.request.POST.get('plan_type')
        selected_lineup_id = self.request.POST.get('lineup_id')

        extra_message_data = f"\nДетали заказа\nТариф: {selected_plan}\nID Состава: {selected_lineup_id}"

        client_message_obj = FormsServices.handling_feedback_form(form)
        ClientMessageServices.add_comments(client_message_obj, extra_message_data)


        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Форма отправлена!'})

        return super().form_valid(form)

    def form_invalid(self, form: ClientMessageForm) -> HttpResponse:

        # Если форма не прошла валидацию и это AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors.get_json_data()  # Передаем список ошибок
            }, status=400)  # Статус 400 заставит JS перейти в блок catch или else

        return super().form_invalid(form)


class LineUpListView(ListView):
    model = LineUp
    template_name = "content/line_up_page.html"
    context_object_name = "line_up_list"

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to add keys for context data

        line_up_list - list of all line_up (count of groups) to add in page slider
        Can be changed in admin LineUp / "Составы"

        header_image - path to header background image !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)
        context["header_image"] = "image/header/header_2.jpg"

        return context


class Contacts(FormView):

    form_class = ClientMessageForm
    template_name = "content/contact_page.html"
    success_url = reverse_lazy("content:contacts")

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        stats_loger.info(f"{request.method} - {request.path}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Method to add keys for context data

        !!! contacts - !!!

        header_image - path to header background image !!! Now is static !!!
        """

        context = super().get_context_data(**kwargs)
        context["header_image"] = "image/header/home_header.png"

        return context

    def form_valid(self, form: ClientMessageForm) -> HttpResponse:

        FormsServices.handling_feedback_form(form)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Форма отправлена!'})


        return super().form_valid(form)

    def form_invalid(self, form: ClientMessageForm) -> HttpResponse:

        # Если форма не прошла валидацию и это AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors.get_json_data()  # Передаем список ошибок
            }, status=400)  # Статус 400 заставит JS перейти в блок catch или else

        return super().form_invalid(form)
