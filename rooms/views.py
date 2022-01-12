from django.core import paginator
from django.views.generic import ListView, DetailView, View
from django.http import Http404
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django_countries import countries
from . import models, forms


### 1-1.class based View - Paginator
class HomeView(ListView):  # room_list.html

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# 2-1 class based - usding DetailView
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room
    # Http404 알아서 해줌


""" 2-2 function based - not using DetailView
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
        # return redirect(reverse("core:home"))
"""


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


"""
def search(request):  # 검색창
    ### 3-2. using form API
    form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})

    ### 3-1. using python ~#13.6
    city = request.GET.get("city", "Anywhere")  # 기본값:Anywhere
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    s_room_type = int(request.GET.get("room_type", 0))
    room_types = models.RoomType.objects.all()
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    super_host = bool(request.GET.get("super_host", False))
    s_amenities = request.GET.getlist("amenities")
    amenities = models.Amenity.objects.all()
    s_facilities = request.GET.getlist("facilities")
    facilities = models.Facility.objects.all()

    form = {
        "city": city,
        "s_room_type": s_room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # 필터링
    filter_args = {}  # Dict

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country  # key

    if s_room_type != 0:
        filter_args["room_type__pk"] = s_room_type

    if price != 0:
        filter_args["price__lte"] = price

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if super_host is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_a in s_amenities:
            filter_args["amenities__pk"] = int(s_a)

    if len(s_facilities) > 0:
        for s_f in s_facilities:
            filter_args["facilities__pk"] = int(s_f)

    f_rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "f_rooms": f_rooms})


def all_rooms(request):
    page = int(request.GET.get("page", 1))  # 1: 기본값
    
    ### 1-2.fuction based View - Paginator
    room_list = models.Room.objects.all()  # QuerySet
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.get_page(int(page))
        return render(request, "rooms/all_rooms.html", {"pages": rooms})
    except EmptyPage:
        rooms = paginator.get_page(1)
        return redirect("/")


    ### 1-3.python 이용한 Paginator
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]  # limit at SQL
    page_count = models.Room.objects.count() / page_size
    

    return render(
        request,
        "rooms/all_rooms.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": math.ceil(page_count),
            "page_range": range(1, math.ceil(page_count) + 1),
        },
        
    )  # template
    
  """
