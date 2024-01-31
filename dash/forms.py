from django.forms import ModelForm
from .models import Employer

class EmpForm(ModelForm):
    class Meta:
        model = Employer
        fields = ['ism', 'yosh', 'lavozim', 'maosh', 'maosh_type']
        # exclude = ['yosh'] # kerak bolmaganlar
        