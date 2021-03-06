from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib import messages
from user_auth.forms import UserCreationForm
from django.urls import reverse_lazy
from calc.forms import HeirForm, DeceasedForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import *
from waffle.mixins import WaffleFlagMixin, WaffleSwitchMixin

import waffle


class HomePage(TemplateView):
	template_name="calc/home.html"

	def get(self, request, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse( 'calc:index'))
		else:
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)
class Terms(TemplateView):
	template_name="calc/terms.html"
class Privacy(TemplateView):
	template_name="calc/privacy.html"
class About(TemplateView):
	template_name="calc/about.html"
class DeceasedCreate(CreateView):
	model = Deceased
	fields = ['first_name','last_name','sex', 'estate']

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.deceased_set.count() >= 1:
			messages.error(request,_("Decease already exist"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		return super().form_valid(form)

class DeceasedUpdate(UpdateView):
	model = Deceased
	fields = ['first_name','last_name', 'estate']

class DeceasedDelete(DeleteView):
	model = Deceased
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.calc = self.object.calc # assuming that deceased have a foreignkey reference to Calculation model
		self.calc.heir_set.all().delete()
		self.object.delete()
		success_url = self.get_success_url()
		return HttpResponseRedirect(success_url)

	def get_success_url(self):
		calc = self.calc
		return reverse(  # no need for lazy here
			'calc:detail',
			 kwargs={'pk': calc.id}
		)
class MotherCreate(CreateView):
	model = Mother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.heir_set.instance_of(Mother).count() >= 1:
			messages.error(request,_("Mother already exist"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_mother(self.object)
		return super().form_valid(form)

class FatherCreate(CreateView):
	model = Father
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.heir_set.instance_of(Father).count() >= 1:
			messages.error(request,_("Father already exist"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_father(self.object)
		return super().form_valid(form)

class HusbandCreate(CreateView):
	model = Husband
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.heir_set.instance_of(Husband).count() >= 1:
			messages.error(request,_("Husband already exist"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_husband(self.object)
		return super().form_valid(form)

class WifeCreate(CreateView):
	model = Wife
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.heir_set.instance_of(Wife).count() >= 4:
			messages.error(request,_("Cann't have more than 4 wifes"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_wife(self.object)
		return super().form_valid(form)

class DaughterCreate(CreateView):
	model = Daughter
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex ="F"
		self.object.save()
		if form.instance.calc.deceased_set.first().sex =='M':
			father = form.instance.calc.deceased_set.first()
			if form.instance.calc.deceased_set.first().male_marriages.count()==1:
				mother =form.instance.calc.deceased_set.first().male_marriages.first().female
			elif form.instance.calc.deceased_set.first().male_marriages.count()==0:
				mother = None
			else:
				mother = get_object_or_404(Wife, pk=self.request.POST.get('mother'))
		else:
			 mother = form.instance.calc.deceased_set.first()
			 if form.instance.calc.deceased_set.first().female_marriages.count()==1:
				 father = form.instance.calc.deceased_set.first().female_marriages.first().male
			 else:
				 father = None
		form.instance.calc.add_daughter(self.object, mother=mother, father=father)
		return super().form_valid(form)

class SonCreate(CreateView):
	model = Son
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		if form.instance.calc.deceased_set.first().sex =='M':
			father = form.instance.calc.deceased_set.first()
			if form.instance.calc.deceased_set.first().male_marriages.count()==1:
				mother =form.instance.calc.deceased_set.first().male_marriages.first().female
			elif form.instance.calc.deceased_set.first().male_marriages.count()==0:
				mother = None
			else:
				mother = get_object_or_404(Wife, pk=self.request.POST.get('mother'))
		else:
			 mother = form.instance.calc.deceased_set.first()
			 if form.instance.calc.deceased_set.first().female_marriages.count()==1:
				 father = form.instance.calc.deceased_set.first().female_marriages.first().male
			 else:
				 father = None
		form.instance.calc.add_son(self.object, mother=mother, father=father)
		return super().form_valid(form)

class BrotherCreate(WaffleFlagMixin, CreateView):
	model = Brother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "Brother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_brother(self.object)
		return super().form_valid(form)

class SisterCreate(WaffleFlagMixin, CreateView):
	model = Sister
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "Sister"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_sister(self.object)
		return super().form_valid(form)

class GrandFatherCreate(WaffleFlagMixin, CreateView):
	model = GrandFather
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "GrandFather"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		if self.calc.heir_set.instance_of(GrandFather).count() >= 1:
			messages.error(request,_("Father already exist"))
			return HttpResponseRedirect(reverse( 'calc:error'))
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_grandFather(self.object)
		return super().form_valid(form)

class GrandMotherCreate(WaffleFlagMixin, CreateView):
	model = GrandMother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "GrandMother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_grandMother(self.object)
		return super().form_valid(form)

class SonOfSonCreate(WaffleFlagMixin, CreateView):
	model = SonOfSon
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "SonOfSon"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_sonOfSon(self.object)
		return super().form_valid(form)

class DaughterOfSonCreate(WaffleFlagMixin, CreateView):
	model = DaughterOfSon
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "DaughterOfSon"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_daughterOfSon(self.object)
		return super().form_valid(form)

class PaternalSisterCreate(WaffleFlagMixin, CreateView):
	model = PaternalSister
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "PaternalSister"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_paternalSister(self.object)
		return super().form_valid(form)

class PaternalBrotherCreate(WaffleFlagMixin, CreateView):
	model = PaternalBrother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "PaternalBrother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_paternalBrother(self.object)
		return super().form_valid(form)

class MaternalSisterCreate(WaffleFlagMixin, CreateView):
	model = MaternalSister
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "MaternalSister"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="F"
		self.object.save()
		form.instance.calc.add_maternalSister(self.object)
		return super().form_valid(form)

class MaternalBrotherCreate(WaffleFlagMixin, CreateView):
	model = MaternalBrother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "MaternalBrother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_maternalBrother(self.object)
		return super().form_valid(form)

class SonOfBrotherCreate(WaffleFlagMixin, CreateView):
	model = SonOfBrother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "SonOfBrother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_sonOfBrother(self.object)
		return super().form_valid(form)

class SonOfPaternalBrotherCreate(WaffleFlagMixin, CreateView):
	model = SonOfPaternalBrother
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "SonOfPaternalBrother"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_sonOfPaternalBrother(self.object)
		return super().form_valid(form)

class UncleCreate(WaffleFlagMixin, CreateView):
	model = Uncle
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "Uncle"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_uncle(self.object)
		return super().form_valid(form)

class PaternalUncleCreate(WaffleFlagMixin, CreateView):
	model = PaternalUncle
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "PaternalUncle"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_paternalUncle(self.object)
		return super().form_valid(form)

class SonOfUncleCreate(WaffleFlagMixin, CreateView):
	model = SonOfUncle
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "SonOfUncle"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_sonOfUncle(self.object)
		return super().form_valid(form)

class SonOfPaternalUncleCreate(WaffleFlagMixin, CreateView):
	model = SonOfPaternalUncle
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'
	waffle_flag = "SonOfPaternalUncle"

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['calc_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		"""
		Overridden to add the relation to the calculation instance.
		"""
		form.instance.calc = self.calc
		self.object = form.save()
		self.object.sex="M"
		self.object.save()
		form.instance.calc.add_sonOfPaternalUncle(self.object)
		return super().form_valid(form)

class HeirUpdate(UpdateView):
	model = Heir
	fields = ['first_name','last_name']
	template_name = 'calc/heir_form.html'

class HeirDelete(DeleteView):
	model = Heir
	template_name = 'calc/heir_confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.calc = self.object.calc # assuming that deceased have a foreignkey reference to Calculation model
		self.object.delete()
		success_url = self.get_success_url()
		return HttpResponseRedirect(success_url)

	def get_success_url(self):
		calc = self.calc
		return reverse(  # no need for lazy here
			'calc:detail',
			 kwargs={'pk': calc.id}
		)
class LoginRequired(View):
	"""
	Redirects to login if user is anonymous
	"""
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequired, self).dispatch(*args, **kwargs)

class IndexView(LoginRequired, generic.ListView):
	template_name = 'calc/index.html'
	context_object_name = 'calculation_list'

	def get_queryset(self):
		return Calculation.objects.filter(user=self.request.user)


class DetailView(LoginRequired, generic.DetailView):
	model = Calculation
	template_name = 'calc/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Father'] = self.object.heir_set.instance_of(Father)
		context['Mother'] = self.object.heir_set.instance_of(Mother)
		context['Wife'] = self.object.heir_set.instance_of(Wife)
		context['Husband'] = self.object.heir_set.instance_of(Husband)
		context['Daughter'] = self.object.heir_set.instance_of(Daughter)
		context['Son'] = self.object.heir_set.instance_of(Son)
		context['Brother'] = self.object.heir_set.instance_of(Brother)
		context['Sister'] = self.object.heir_set.instance_of(Sister)
		context['GrandFather'] = self.object.heir_set.instance_of(GrandFather)
		context['Heirs'] = self.object.heir_set.order_by('polymorphic_ctype_id')
		return context

class NewResultsView(WaffleFlagMixin, LoginRequired, generic.DetailView):
	model = Calculation
	template_name = 'calc/new_results.html'
	waffle_flag= "new_results"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Father'] = self.object.heir_set.instance_of(Father)
		context['Mother'] = self.object.heir_set.instance_of(Mother)
		context['Wife'] = self.object.heir_set.instance_of(Wife)
		context['Husband'] = self.object.heir_set.instance_of(Husband)
		context['Daughter'] = self.object.heir_set.instance_of(Daughter)
		context['Son'] = self.object.heir_set.instance_of(Son)
		context['Brother'] = self.object.heir_set.instance_of(Brother)
		context['Sister'] = self.object.heir_set.instance_of(Sister)
		context['GrandFather'] = self.object.heir_set.instance_of(GrandFather)
		context['female_asaba'] = self.object.heir_set.filter(asaba=True,sex="F")
		context['asaba'] = self.object.heir_set.filter(asaba=True).order_by('polymorphic_ctype_id')
		context['Heirs'] = self.object.heir_set.filter(asaba=False).order_by('polymorphic_ctype_id')
		context['Spouse'] = self.object.heir_set.instance_of(Husband, Wife)
		context['No_Spouse'] = self.object.heir_set.not_instance_of(Husband, Wife)
		return context

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['pk'])
		self.calc.compute()
		return super().dispatch(request, *args, **kwargs)

class ResultsView(LoginRequired, generic.DetailView):
	model = Calculation
	template_name = 'calc/results.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Father'] = self.object.heir_set.instance_of(Father)
		context['Mother'] = self.object.heir_set.instance_of(Mother)
		context['Wife'] = self.object.heir_set.instance_of(Wife)
		context['Husband'] = self.object.heir_set.instance_of(Husband)
		context['Daughter'] = self.object.heir_set.instance_of(Daughter)
		context['Son'] = self.object.heir_set.instance_of(Son)
		context['Brother'] = self.object.heir_set.instance_of(Brother)
		context['Sister'] = self.object.heir_set.instance_of(Sister)
		context['GrandFather'] = self.object.heir_set.instance_of(GrandFather)
		context['female_asaba'] = self.object.heir_set.filter(asaba=True,sex="F")
		context['asaba'] = self.object.heir_set.filter(asaba=True).order_by('polymorphic_ctype_id')
		context['Heirs'] = self.object.heir_set.filter(asaba=False).order_by('polymorphic_ctype_id')
		context['Spouse'] = self.object.heir_set.instance_of(Husband, Wife)
		context['No_Spouse'] = self.object.heir_set.not_instance_of(Husband, Wife)
		return context

	def dispatch(self, request, *args, **kwargs):
		"""
		Overridden so we can make sure the `calc` instance exists
		before going any further.
		"""
		self.calc = get_object_or_404(Calculation, pk=kwargs['pk'])
		self.calc.compute()
		return super().dispatch(request, *args, **kwargs)

class CalculationUpdate(UpdateView):
	model = Calculation
	fields = ['name']

def new(request):
	name = request.POST["name"]
	if name == "":
		messages.error(request,_("Must enter a name for your calcualtion") )
		return HttpResponseRedirect(reverse('calc:error'))

	user = request.user
	calc = Calculation.objects.create (name=name, user=user)
	if 'next' in request.POST and request.POST['next'] != "":
		return HttpResponseRedirect(reverse('calc:detail', args=(calc.id,)))
	else:
		return HttpResponseRedirect(reverse('calc:index'))

def father(request, pk):
	calc = get_object_or_404(Calculation, pk=pk)
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	calc.add_father(first_name=first_name, last_name=last_name)
	return HttpResponseRedirect(reverse('calc:detail', args=(calc.id,)))


def delete(request, pk):
	calc = get_object_or_404(Calculation, pk=pk)
	if calc.user == request.user:
		calc.delete()
		return HttpResponseRedirect(reverse('calc:index'))
	else:
		messages.error(request,_("user not allowed") )
		return HttpResponseRedirect(reverse('calc:error'))

def error(request):
	return render(request, 'calc/error.html')

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'
