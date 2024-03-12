from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    host_country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    govt_order = models.CharField(max_length=150)
    govt_order_upload = models.FileField(upload_to='govt_orders/')

    def get_total_days(self):
        return (self.end_date - self.start_date).days

    def save(self, *args, **kwargs):
        self.total_days = self.get_total_days()
        super().save(*args, **kwargs)


    
    
class Participant(models.Model):
    SVC_CHOICES = [
        ("army", "Army"),
        ("navy", "Navy"),
        ("air_force", "Air Force"),
    ]

    RANK_CHOICES = [
        ('sainik', 'Sainik'),
        ('lcpl', 'Lance Corporal'),
        ('cpl', 'Corporal'),
        ('sgt', 'Sergeant'),
        ('wo', 'Warrant Officer'),
        ('swo', 'Senior Warrant Officer'),
        ('mwo', 'Master Warrant Officer'),
        ('cadet', 'Cadet Officer'),
        ('2_lt', '2 Lieutenant'),
        ('lt', 'Lieutenant'),
        ('capt', 'Captain'),
        ('major', 'Major'),
        ('lieutenant_colonel', 'Lieutenant Colonel'),
        ('colonel', 'Colonel'),
        ('brigadier', 'Brigadier General'),
        ('major_general', 'Major General'),
        ('lieutenant_general', 'Lieutenant General'),
        ('general', 'General'),
        ('2_lt_afns', '2 Lieutenant AFNS'),
        ('lt_afns', 'Lieutenant AFNS'),
        ('capt_afns', 'Captain AFNS'),
        ('major_afns', 'Major AFNS'),
        ('lieutenant_colonel_afns', 'Lieutenant Colonel AFNS'),

        ('sailor', 'Sailor'),
        ('leading_seaman', 'Leading Seaman'),
        ('petty_officer', 'Petty Officer'),
        ('chief_petty_officer', 'Chief Petty Officer'),
        ('sub_lieutenant', 'Sub Lieutenant'),
        ('lieutenant_commander', 'Lieutenant Commander'),
        ('commander', 'Commander'),
        ('captain_navy', 'Captain'),
        ('rear_admiral', 'Rear Admiral'),
        ('vice_admiral', 'Vice Admiral'),
        ('admiral', 'Admiral'),

        ('airman', 'Airman'),
        ('corporal', 'Corporal'),
        ('sergeant', 'Sergeant'),
        ('flight_sergeant', 'Flight Sergeant'),
        ('warrant_officer', 'Warrant Officer'),
        ('pilot_officer', 'Pilot Officer'),
        ('flying_officer', 'Flying Officer'),
        ('flight_lieutenant', 'Flight Lieutenant'),
        ('squadron_leader', 'Squadron Leader'),
        ('wing_commander', 'Wing Commander'),
        ('group_captain', 'Group Captain'),
        ('air_commodore', 'Air Commodore'),
        ('air_vice_marshal', 'Air Vice Marshal'),
        ('air_marshal', 'Air Marshal'),
        ('air_chief_marshal', 'Air Chief Marshal'),

        ('civilian', 'Civilian'),
    ]

    service_number = models.CharField(max_length=50)
    rank = models.CharField(max_length=30, choices=RANK_CHOICES)
    name = models.CharField(max_length=50)
    service = models.CharField(max_length=20, choices=SVC_CHOICES)

    def __str__(self):
        return f"{self.service_number} - {self.rank} - {self.name}"

class ParticipantEvent(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.participant} - {self.event}"
    
    
class Country(models.Model):
    class CountryClass(models.TextChoices):
        A = 'A', 'Class A'
        B = 'B', 'Class B'
        C = 'C', 'Class C'

    name = models.CharField(max_length=100, unique=True)
    country_class = models.CharField(max_length=1, choices=CountryClass.choices)

    def __str__(self):
        return self.name



class CourseOffer(models.Model):
    ff_country = models.ForeignKey("Country", on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    vacancies_offered = models.PositiveIntegerField(default=1)
    year = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1900),
        ]
    )
    vacancies_accepted_army = models.PositiveIntegerField(default=1)
    vacancies_accepted_navy = models.PositiveIntegerField(default=1)
    vacancies_accepted_air = models.PositiveIntegerField(default=1)
    vacancies_regretted = models.PositiveIntegerField(default=0)
    financial_offer_choices = [
        ("gratis", "Gratis"),
        ("non-gratis", "Non-Gratis"),
        ("partial-gratis", "Partial-Gratis"),
        ("reciprocal", "Reciprocal"),
    ]
    fin_offer = models.CharField(
        max_length=20,
        choices=financial_offer_choices,
        default='gratis'
    )

    def total_vacancies_accepted(self):
        return (
            self.vacancies_accepted_army +
            self.vacancies_accepted_navy +
            self.vacancies_accepted_air
        )

    def save(self, *args, **kwargs):
        # Calculate vacancies_regretted dynamically based on vacancies_offered and vacancies_accepted
        self.vacancies_regretted = max(0, self.vacancies_offered - self.total_vacancies_accepted())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ff_country} - {self.course_name} - {self.year}"
    
    
class OfficersandStaffs(models.Model):
    SVC_CHOICES = [
        ("army", "Army"),
        ("navy", "Navy"),
        ("air_force", "Air Force"),
    ]

    RANK_CHOICES = [
        ('sainik', 'Sainik'),
        ('lcpl', 'Lance Corporal'),
        ('cpl', 'Corporal'),
        ('sgt', 'Sergeant'),
        ('wo', 'Warrant Officer'),
        ('swo', 'Senior Warrant Officer'),
        ('mwo', 'Master Warrant Officer'),
        ('cadet', 'Cadet Officer'),
        ('2_lt', '2 Lieutenant'),
        ('lt', 'Lieutenant'),
        ('capt', 'Captain'),
        ('major', 'Major'),
        ('lieutenant_colonel', 'Lieutenant Colonel'),
        ('colonel', 'Colonel'),
        ('brigadier', 'Brigadier General'),
        ('major_general', 'Major General'),
        ('lieutenant_general', 'Lieutenant General'),
        ('general', 'General'),
        ('2_lt_afns', '2 Lieutenant AFNS'),
        ('lt_afns', 'Lieutenant AFNS'),
        ('capt_afns', 'Captain AFNS'),
        ('major_afns', 'Major AFNS'),
        ('lieutenant_colonel_afns', 'Lieutenant Colonel AFNS'),

        ('sailor', 'Sailor'),
        ('leading_seaman', 'Leading Seaman'),
        ('petty_officer', 'Petty Officer'),
        ('chief_petty_officer', 'Chief Petty Officer'),
        ('sub_lieutenant', 'Sub Lieutenant'),
        ('lieutenant_commander', 'Lieutenant Commander'),
        ('commander', 'Commander'),
        ('captain_navy', 'Captain'),
        ('rear_admiral', 'Rear Admiral'),
        ('vice_admiral', 'Vice Admiral'),
        ('admiral', 'Admiral'),

        ('airman', 'Airman'),
        ('corporal', 'Corporal'),
        ('sergeant', 'Sergeant'),
        ('flight_sergeant', 'Flight Sergeant'),
        ('warrant_officer', 'Warrant Officer'),
        ('pilot_officer', 'Pilot Officer'),
        ('flying_officer', 'Flying Officer'),
        ('flight_lieutenant', 'Flight Lieutenant'),
        ('squadron_leader', 'Squadron Leader'),
        ('wing_commander', 'Wing Commander'),
        ('group_captain', 'Group Captain'),
        ('air_commodore', 'Air Commodore'),
        ('air_vice_marshal', 'Air Vice Marshal'),
        ('air_marshal', 'Air Marshal'),
        ('air_chief_marshal', 'Air Chief Marshal'),

        ('civilian', 'Civilian'),
    ]
    
    SERVICE_STATUS_CHOICES = [
        ("commissioned_officer", "Commissioned Officer"),
        ("jco", "JCO"),
        ("other_rank", "Other Rank"),
        ("civilian", "Civilian"),
    ]

    service_number = models.CharField(max_length=50)
    rank = models.CharField(max_length=30, choices=RANK_CHOICES)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    service = models.CharField(max_length=20, choices=SVC_CHOICES)
    staffstatus = models.CharField(max_length=50, choices=SERVICE_STATUS_CHOICES)
    dateofjoin = models.DateField()
    dateofpostedout =  models.DateField(null=True, blank=True)

    def afdservice(self):
        if self.dateofpostedout:
            delta = self.dateofpostedout - self.dateofjoin
        else:
            delta = datetime.now().date() - self.dateofjoin
        
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return years, months, days
    @property
    def afdservice_display(self):
        years, months, days = self.afdservice()
        result = ""
        if years:
            result += f"{years} year{'s' if years > 1 else ''}"
        if months:
            result += f", {months} month{'s' if months > 1 else ''}"
        if days:
            result += f", {days} day{'s' if days > 1 else ''}"
        return result.strip()

    def __str__(self):
        return f"{self.service_number} - {self.rank} - {self.name} - {self.designation}"