from django.views.generic import ListView, DetailView
from django.http import Http404
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect, render
from django_countries import countries
from . import models


### 1.class based View - Paginator
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


# 1) class based - usding DetailView
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room
    # Http404 알아서 해줌


""" 2) function based - not using DetailView
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
        # return redirect(reverse("core:home"))
"""


def search(request):  # 검색창
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
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
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

    return render(request, "rooms/search.html", {**form, **choices})


"""
def all_rooms(request):
    page = int(request.GET.get("page", 1))  # 1: 기본값
    
    ### 2.fuction based View - Paginator
    room_list = models.Room.objects.all()  # QuerySet
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.get_page(int(page))
        return render(request, "rooms/all_rooms.html", {"pages": rooms})
    except EmptyPage:
        rooms = paginator.get_page(1)
        return redirect("/")


    ### 3.python 이용한 Paginator
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
