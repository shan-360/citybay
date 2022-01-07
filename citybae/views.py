from django.shortcuts import render, redirect
from .models import Search, User, Registration, RateCity, DistinctRateCity
import folium
import geocoder
from .forms import SearchForm, LoginForm, RegistrationForm, SearchCityForm, RateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def search(request):
    if request.user.is_active:
        form = SearchForm(request.POST)
        if (request.method == 'POST'):
            if form.is_valid():
                address = request.POST.get('search_address')
                location = geocoder.osm(address)
                report = form.save(commit=False)
                report.search_country = location.country
                form.save()
                save_country = Search.objects.all().last()
                print(save_country)
                save_country.search_country = location.country
                save_country.save()
                lat = location.lat
                lng = location.lng
                country = location.country
                if lat == None or lng == None:
                    return render(request, "failure.html")
                m = folium.Map(location=[lat, lng], zoom_start=2)
                folium.Marker(location=[lat, lng], tooltip='Click for more', popup=country).add_to(m)
                # get HTML representation of the map
                m = m._repr_html_()
                context = {
                    'm': m,
                    'form': form,
                    'address': address,
                    'country': country,
                    'lat': location.lat,
                    'lng': location.lng
                }
                form.save()
                return render(request, "search.html", context)
        else:
            form = SearchForm()
        m = folium.Map(location=[0, 0], zoom_start=2)
        folium.Marker(location=[0, 0], tooltip='Click for more').add_to(m)
        m = m._repr_html_()
        context = {
            'm': m,
            'form': form,
        }
        return render(request, "search.html", context)
    else:
        return redirect("login")


def login_view(request):
    form = LoginForm(request.POST)
    context = {"form": form}
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('user_pwd')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'success.html')
        else:
            messages.error(request, 'username or password not correct')
            context = {"form": form}
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST)
    if (request.method == 'POST'):
        if form.is_valid():
            if (Registration.objects.filter(reg_name=request.POST.get('reg_name')).exists()):
                messages.info(request, "Couldn't create account! This username is already used.")
            else:
                try:
                    username = request.POST.get('reg_name')
                    password = request.POST.get('reg_pwd')
                    password2 = request.POST.get('reg_pwd2')
                    if password == password2 and len(password) >= 6:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                        form.save()
                        return redirect('login')
                    else:
                        messages.info(request, 'Passwords do not match or Password is too short')
                except:
                    return render(request, "failure.html")

    context = {'form': form}
    return render(request, 'registration.html', context)


def rating_view(request):
    if request.user.is_active:
        form = RateForm(request.POST)
        if (request.method == 'POST'):
            if form.is_valid():
                form.save()
                new_city = RateCity.objects.all().last()
                new_city.overall = (
                                           new_city.food + new_city.nightlife + new_city.people + new_city.culture + new_city.accommodation) / 5
                new_city.save()
                if (DistinctRateCity.objects.filter(distinct_city__icontains=new_city.city,
                                                    distinct_country__icontains=new_city.country).exists()):
                    cities = RateCity.objects.filter(city__icontains=RateCity.objects.all().last())
                    sum_food = 0
                    sum_nightlife = 0
                    sum_culture = 0
                    sum_people = 0
                    sum_accommodation = 0
                    for city in cities:
                        sum_food = sum_food + city.food
                        sum_nightlife = sum_nightlife + city.nightlife
                        sum_culture = sum_culture + city.culture
                        sum_people = sum_people + city.people
                        sum_accommodation = sum_accommodation + city.accommodation
                    overwrite_obj = DistinctRateCity.objects.get(distinct_city__icontains=new_city.city,
                                                                 distinct_country__icontains=new_city.country)
                    overwrite_obj.distinct_counter = overwrite_obj.distinct_counter + 1
                    overwrite_obj.distinct_nightlife = sum_nightlife / overwrite_obj.distinct_counter
                    print(overwrite_obj.distinct_nightlife)
                    overwrite_obj.distinct_food = sum_food / overwrite_obj.distinct_counter
                    overwrite_obj.distinct_culture = sum_culture / overwrite_obj.distinct_counter
                    overwrite_obj.distinct_people = sum_people / overwrite_obj.distinct_counter
                    overwrite_obj.distinct_accommodation = sum_accommodation / overwrite_obj.distinct_counter
                    overwrite_obj.distinct_overall = (
                                                             overwrite_obj.distinct_nightlife + overwrite_obj.distinct_food + overwrite_obj.distinct_culture + overwrite_obj.distinct_people + overwrite_obj.distinct_accommodation) / 5
                    overwrite_obj.save()
                else:
                    rate_obj = RateCity.objects.all().last()
                    distinct_city = DistinctRateCity(
                        distinct_city=rate_obj.city,
                        distinct_country=rate_obj.country,
                        distinct_counter=1,
                        distinct_nightlife=rate_obj.nightlife,
                        distinct_food=rate_obj.food,
                        distinct_culture=rate_obj.culture,
                        distinct_people=rate_obj.people,
                        distinct_accommodation=rate_obj.accommodation,
                        distinct_overall=(
                                                 rate_obj.nightlife + rate_obj.food + rate_obj.culture + rate_obj.people + rate_obj.accommodation) / 5)
                    distinct_city.save()
                return render(request, "rating_success.html")
            else:
                return render(request, "failure.html")
        city_data = Search.objects.all().last()
        form = RateForm(
            initial={'city': city_data.search_address, 'user': request.user, 'country': city_data.search_country})
        form.fields['user'].widget.attrs['readonly'] = True
        context = {
            'form': form,
        }
        return render(request, "rating.html", context)
    else:
        return render(request, "failure.html")


def rating_overview_view(request):
    form = SearchCityForm(request.POST)
    if (request.method == 'POST'):
        if form.is_valid():
            course_instance = DistinctRateCity.objects.filter(distinct_city__icontains=request.POST.get('city'))
            return render(request, "rating_overview.html", {'ratings': course_instance, 'form': form})
        else:
            return render(request, "failure.html")

    detail_ratings = RateCity.objects.all()
    ratings = DistinctRateCity.objects.all()
    return render(request, "rating_overview.html", {'ratings': ratings, 'detail_ratings': detail_ratings, 'form': form})


def rating_detail_view(request, pk):
    if request.user.is_active:
        rating = DistinctRateCity.objects.get(id=pk)
        all_ratings = RateCity.objects.filter(city__icontains=rating.distinct_city,
                                              country__icontains=rating.distinct_country)
        print(all_ratings)
        context = {
            'id': rating.id,
            'city': rating.distinct_city,
            'overall': rating.distinct_overall,
            'food': rating.distinct_food,
            'nightlife': rating.distinct_nightlife,
            'culture': rating.distinct_culture,
            'people': rating.distinct_people,
            'accommodation': rating.distinct_accommodation,
            'ratings': all_ratings
        }
        return render(request, "rating_detail.html", context)
    else:
        return render(request, "failure.html")


def single_rating_detail_view(request, pk):
    if request.user.is_active:
        rating_id = RateCity.objects.get(id=pk)
        field_user = RateCity._meta.get_field('user')
        field_city = RateCity._meta.get_field('city')
        field_country = RateCity._meta.get_field('country')
        field_overall = RateCity._meta.get_field('overall')
        field_food = RateCity._meta.get_field('food')
        field_nightlife = RateCity._meta.get_field('nightlife')
        field_culture = RateCity._meta.get_field('culture')
        field_people = RateCity._meta.get_field('people')
        field_accommodation = RateCity._meta.get_field('accommodation')
        user = field_user.value_from_object(rating_id)
        city = field_city.value_from_object(rating_id)
        country = field_country.value_from_object(rating_id)
        overall = field_overall.value_from_object(rating_id)
        food = field_food.value_from_object(rating_id)
        nightlife = field_nightlife.value_from_object(rating_id)
        culture = field_culture.value_from_object(rating_id)
        people = field_people.value_from_object(rating_id)
        accommodation = field_accommodation.value_from_object(rating_id)
        context = {
            'user': user,
            'id': rating_id,
            'city': city,
            'country': country,
            'overall': overall,
            'food': food,
            'nightlife': nightlife,
            'culture': culture,
            'people': people,
            'accommodation': accommodation
        }
        return render(request, "single_rating_detail.html", context)
    else:
        return render(request, "failure.html")


def logout_view(request):
    logout(request)
    return render(request, "login.html")


def success_view(request):
    return render(request, "success.html")


def failure_view(request):
    return render(request, "failure.html")
