from django.views.generic import ListView
from django.views.generic.edit import CreateView

from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from .models import UserProfile


# Create your views here.
class ContactUsView(CreateView):
	template_name = 'contact_module/contact_us_page.html'
	success_url = '/'
	form_class = ContactUsModelForm

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		setting = SiteSetting.objects.filter(is_main_setting=True).only('site_name',
																		'address', 'phone', 'fax', 'email').first()
		context['site_setting'] = setting
		return context


def store_file(file):
	with open(f'temp/{file}', mode='wb+') as dest:
		for chunk in file.chunks():
			dest.write(chunk)


class CreateProfileView(CreateView):
	template_name = 'contact_module/create_profile_page.html'
	model = UserProfile
	fields = '__all__'
	# form_class = ProfileForm
	success_url = '/contact-us/create-profile/'
	# def get(self, request):
	#     form = ProfileForm()
	#     return render(request, 'contact_module/create_profile_page.html', {'form': form})
	#
	# def post(self, request):
	#     submited_form = ProfileForm(request.POST, request.FILES)
	#     if submited_form.is_valid():
	#         # store_file(request.FILES['image'])
	#         profile = UserProfile(image=request.FILES['user_image'])
	#         profile.save()
	#         return redirect('home_page')
	#     return render(request, 'contact_module/create_profile_page.html', {'form': submited_form})


class ProfilesView(ListView):
	model = UserProfile
	template_name = 'contact_module/profiles_list_page.html'
	context_object_name = 'profiles'
