from django.shortcuts import render, redirect
from django.db.models import Sum
from . models import Event, Participant, ParticipantEvent, CourseOffer
from .forms import EventForm, ParticipantForm, ParticipantEventForm, CourseOfferForm
from django.db.models import F, ExpressionWrapper, fields
from django.core.serializers import serialize
from django.db.models import Count
import datetime

def home(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        correct_password = "998877113355"

        if entered_password == correct_password:
            return redirect('section')

        else:
            return render(request, 'home.html', {'message': 'Incorrect password. Please try again.'})

    return render(request, 'home.html')




def sections(request):
    Section_list = ['HQ Trg Dte', 'Army Trg', 'Navy Trg', 'Air Trg', 'Joint Trg', 'Jt College']

    return render(request, 'sections.html', {'Section_list': Section_list})


def armytrg(request):
    godata = Event.objects.all()
    courseoffers = CourseOffer.objects.annotate(
        total_vacancies_accepted=ExpressionWrapper(
            F('vacancies_accepted_army') + F('vacancies_accepted_navy') + F('vacancies_accepted_air'),
            output_field=fields.IntegerField()
        )
    )

    # Query to get total vacancies offered, accepted, and regretted
    total_offered = courseoffers.aggregate(Sum('vacancies_offered'))
    total_accepted = courseoffers.aggregate(Sum('total_vacancies_accepted'))
    total_regretted = courseoffers.aggregate(Sum('vacancies_regretted'))

    # Calculate the percentage
    percentage_accepted = (total_accepted['total_vacancies_accepted__sum'] / total_offered['vacancies_offered__sum']) * 100
    percentage_regretted = (total_regretted['vacancies_regretted__sum'] / total_offered['vacancies_offered__sum']) * 100
    
    # Query for the number of vacancies offered and accepted for each country
    country_analysis = CourseOffer.objects.values('ff_country__name').annotate(
    total_offered=Sum('vacancies_offered'),
    total_accepted=ExpressionWrapper(
        Sum(F('vacancies_accepted_army') + F('vacancies_accepted_navy') + F('vacancies_accepted_air')),
        output_field=fields.IntegerField()
    ),
    total_regretted=Sum('vacancies_regretted')
)


    context = {
        'godata': godata,
        'courseoffers': courseoffers,
        'total_offered': total_offered['vacancies_offered__sum'],
        'total_accepted': total_accepted['total_vacancies_accepted__sum'],
        'total_regretted': total_regretted['vacancies_regretted__sum'],
        'percentage_accepted': percentage_accepted,
        'percentage_regretted': percentage_regretted,
        'country_analysis': country_analysis,
    }

    return render(request, 'armydashboard.html', context)



def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('armytrg')  
    else:
        form = EventForm()

    return render(request, 'event_form.html', {'form': form})



def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if participant with the same service_number already exists
            service_number = form.cleaned_data.get('service_number')
            if Participant.objects.filter(service_number=service_number).exists():
                # Participant already exists, you can handle this case as per your requirement
                # For example, you can display an error message to the user
                return render(request, 'participant_form.html', {'form': form, 'error_message': 'Participant with this service number already exists.'})
            else:
                # Participant does not exist, save the form
                form.save()
                return redirect('armytrg')
    else:
        form = ParticipantForm()

    return render(request, 'participant_form.html', {'form': form})



def participant_event(request):
    if request.method == 'POST':
        form = ParticipantEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('armytrg')  
    else:
        form = ParticipantEventForm()

    return render(request, 'participant_event_form.html', {'form': form})




def participant_view(request):
    participants = Participant.objects.all()
    partevents = ParticipantEvent.objects.all()

    combined_data = []

    for partevent in partevents:
        participant = partevent.participant
        event = partevent.event

        data = {
            'participant_service_number': participant.service_number,
            'participant_rank': participant.rank,
            'participant_name': participant.name,
            'event_name': event.event_name,
            'event_start_date': event.start_date,
            'event_end_date': event.end_date,
            'event_total_days': event.total_days,
            'event_govt_order': event.govt_order,
        }

        combined_data.append(data)

    # Count the total participants
    total_participants = len(combined_data)

    # Count participants by rank
    rank_counts = Participant.objects.values('rank').annotate(count=Count('participantevent')).order_by('rank')

    context = {
        'combined_data': combined_data,
        'total_participants': total_participants,
        'rank_counts': rank_counts,
    }

    return render(request, 'participant_views.html', context)


def creat_course_offer(request):
    if request.method == 'POST':
        form = CourseOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('armytrg')  
    else:
        form = CourseOfferForm()

    return render(request, 'course_offer_form.html', {'form': form})


def coffer_by_country(request):
    # Get the current year
    current_year = datetime.datetime.now().year
    

    # Course offer analysis by country and year
    country_analysis = CourseOffer.objects.values('ff_country__name', 'year').annotate(
        total_offered=Sum('vacancies_offered'),
        total_accepted=ExpressionWrapper(
            Sum(F('vacancies_accepted_army') + F('vacancies_accepted_navy') + F('vacancies_accepted_air')),
            output_field=fields.IntegerField()
        ),
        total_regretted=Sum('vacancies_regretted')
    ).order_by('ff_country__name', 'year')

    # Unique years in the data
    unique_years = CourseOffer.objects.values_list('year', flat=True).distinct()

    # Analysis for the current year
    current_year_analysis = country_analysis.filter(year=current_year)

    # Previous year
    previous_year = current_year - 1
    previous_year_analysis = country_analysis.filter(year=previous_year)

    # Top five countries offering courses
    top_five_countries = country_analysis.filter(year=current_year).order_by('-total_offered')[:5]

    # Lowest three countries offering courses
    lowest_three_countries = country_analysis.filter(year=current_year).order_by('total_offered')[:3]

    # Calculate additional metrics for the summary text
    current_year_total_offers = current_year_analysis.aggregate(Sum('total_offered'))['total_offered__sum']
    current_year_total_countries = current_year_analysis.count()
    current_year_accepted_offers = current_year_analysis.aggregate(Sum('total_accepted'))['total_accepted__sum']
    current_year_regretted_offers = current_year_analysis.aggregate(Sum('total_regretted'))['total_regretted__sum']

    # Assuming these are the actual variable names from your data
    current_year_top_countries = ', '.join([country['ff_country__name'] for country in top_five_countries])

    # Placeholder variables for previous year
    previous_year_total_offers = 0
    previous_year_accepted_offers = 0
    previous_year_regretted_offers = 0

    # Placeholder variable for lowest countries
    lowest_countries = ', '.join([country['ff_country__name'] for country in lowest_three_countries])

    # Convert QuerySet to list of dictionaries
    country_analysis_list = list(country_analysis)

    context = {
        'country_analysis': country_analysis_list,
        'unique_years': unique_years,
        'current_year_analysis': current_year_analysis,
        'previous_year_analysis': previous_year_analysis,
        'top_five_countries': top_five_countries,
        'lowest_three_countries': lowest_three_countries,

        # Variables for the summary text
        'current_year': current_year,
        'current_year_total_offers': current_year_total_offers,
        'current_year_total_countries': current_year_total_countries,
        'current_year_accepted_offers': current_year_accepted_offers,
        'current_year_regretted_offers': current_year_regretted_offers,
        'current_year_top_countries': current_year_top_countries,

        'previous_year': previous_year,
        'previous_year_total_offers': previous_year_total_offers,
        'previous_year_accepted_offers': previous_year_accepted_offers,
        'previous_year_regretted_offers': previous_year_regretted_offers,

        'lowest_countries': lowest_countries,
        
    }

    return render(request, 'country_coffer.html', context)




def codby_services(request):
    current_year = datetime.datetime.now().year
    previous_year = current_year - 1
    previous_previous_year = current_year - 2
    next_year = current_year + 1
    
    # Filter CourseOffer objects for the selected years
    ywandsvcwoffer = CourseOffer.objects.filter(year=current_year, service_name='army').count()
    current_year_offers_army = CourseOffer.objects.filter(offer_year=current_year, service_name='army').count()
    previous_year_offers_army = CourseOffer.objects.filter(offer_year=previous_year, service_name='army').count()
    previous_previous_year_offers_army = CourseOffer.objects.filter(offer_year=previous_previous_year, service_name='army').count()

    current_year_offers_navy = CourseOffer.objects.filter(offer_year=current_year, service_name='navy').count()
    previous_year_offers_navy = CourseOffer.objects.filter(offer_year=previous_year, service_name='navy').count()
    previous_previous_year_offers_navy = CourseOffer.objects.filter(offer_year=previous_previous_year, service_name='navy').count()

    current_year_offers_air = CourseOffer.objects.filter(offer_year=current_year, service_name='air').count()
    previous_year_offers_air = CourseOffer.objects.filter(offer_year=previous_year, service_name='air').count()
    previous_previous_year_offers_air = CourseOffer.objects.filter(offer_year=previous_previous_year, service_name='air').count()
    
    context = {
        'current_year': current_year,
        'previous_year': previous_year,
        'previous_previous_year': previous_previous_year,
        'next_year': next_year,
        'current_year_offers_army': current_year_offers_army,
        'previous_year_offers_army': previous_year_offers_army,
        'previous_previous_year_offers_army': previous_previous_year_offers_army,
        'current_year_offers_navy': current_year_offers_navy,
        'previous_year_offers_navy': previous_year_offers_navy,
        'previous_previous_year_offers_navy': previous_previous_year_offers_navy,
        'current_year_offers_air': current_year_offers_air,
        'previous_year_offers_air': previous_year_offers_air,
        'previous_previous_year_offers_air': previous_previous_year_offers_air,
    }
    return render(request, 'codby_svc.html', context)
   



