from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ContactForm
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'home.html', context=None)

class AboutPageView(TemplateView):
	template_name = 'projects.html'

# Contact
def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the 
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['isobel.django@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('thanks')

    return render(request, 'contact.html', {'form': form_class,})

def thanks(request):
	return render(request, 'thanks.html')
