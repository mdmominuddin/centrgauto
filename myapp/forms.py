from django import forms
from .models import Event, Participant, ParticipantEvent, CourseOffer, OfficersandStaffs

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['total_days']  

    def save(self, commit=True):
        instance = super().save(commit=False)

        
        instance.total_days = (instance.end_date - instance.start_date).days

        if commit:
            instance.save()

        return instance



class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('service_number', 'rank', 'name', 'service')




class ParticipantEventForm(forms.ModelForm):
    class Meta:
        model = ParticipantEvent
        fields = ('participant', 'event',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

      
        self.fields['event'].widget = forms.Select(choices=[(event.id, event.event_name) for event in self.fields['event'].queryset])

        
        self.fields['participant'].widget = forms.Select(choices=[(participant.id, f"{participant.rank} - {participant.name}") for participant in self.fields['participant'].queryset])
    
    
    
class CourseOfferForm(forms.ModelForm):
    class Meta:
        model = CourseOffer
        fields = [
            'ff_country',
            'course_name',
            'vacancies_offered',
            'year',
            'vacancies_accepted_army',
            'vacancies_accepted_navy',
            'vacancies_accepted_air',
            'fin_offer',
        ]

    def __init__(self, *args, **kwargs):
        super(CourseOfferForm, self).__init__(*args, **kwargs)

        # Add 'form-control' class to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OfficersandStaffsForm(forms.ModelForm):
    class Meta:
        model = OfficersandStaffs
        fields = '__all__'
        widgets = {
            'service_number': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'staffstatus': forms.Select(attrs={'class': 'form-control'}),
            'dateofjoin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dateofpostedout': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }