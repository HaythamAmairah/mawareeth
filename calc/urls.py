from django.urls import path
from . import views

app_name = 'calc'
urlpatterns = [
	path('calc/', views.IndexView.as_view(), name='index'),
	path('', views.HomePage.as_view(), name='home'),
	path('terms/', views.Terms.as_view(), name='terms'),
	path('privacy/', views.Privacy.as_view(), name='privacy'),
	path('about/', views.About.as_view(), name='about'),
	path('new/', views.new, name='new'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/delete/', views.delete, name='delete'),
	path('<int:calc_id>/deceased', views.DeceasedCreate.as_view(), name='deceased'),
	path('<int:pk>/deceased_delete', views.DeceasedDelete.as_view(), name='deceased_delete'),
	path('<int:pk>/deceased_update', views.DeceasedUpdate.as_view(), name='deceased_update'),
	path('<int:pk>/calc_update', views.CalculationUpdate.as_view(), name='calc_update'),
	path('<int:calc_id>/mother', views.MotherCreate.as_view(), name='mother'),
	path('<int:pk>/heir_delete', views.HeirDelete.as_view(), name='heir_delete'),
	path('<int:pk>/heir_update', views.HeirUpdate.as_view(), name='heir_update'),
	path('<int:calc_id>/father', views.FatherCreate.as_view(), name='father'),
	path('<int:calc_id>/husband', views.HusbandCreate.as_view(), name='husband'),
	path('<int:calc_id>/wife', views.WifeCreate.as_view(), name='wife'),
	path('<int:calc_id>/daughter', views.DaughterCreate.as_view(), name='daughter'),
	path('<int:calc_id>/son', views.SonCreate.as_view(), name='son'),
	path('<int:calc_id>/bother', views.BrotherCreate.as_view(), name='brother'),
	path('<int:calc_id>/sister', views.SisterCreate.as_view(), name='sister'),
	path('<int:calc_id>/grandFather', views.GrandFatherCreate.as_view(), name='grandFather'),
	path('<int:calc_id>/grandMother', views.GrandMotherCreate.as_view(), name='grandMother'),
	path('<int:calc_id>/sonOfSon', views.SonOfSonCreate.as_view(), name='sonOfSon'),
	path('<int:calc_id>/daughterOfSon', views.DaughterOfSonCreate.as_view(), name='daughterOfSon'),
	path('<int:calc_id>/paternalSister', views.PaternalSisterCreate.as_view(), name='paternalSister'),
	path('<int:calc_id>/paternalBrother', views.PaternalBrotherCreate.as_view(), name='paternalBrother'),
	path('<int:calc_id>/maternalSister', views.MaternalSisterCreate.as_view(), name='maternalSister'),
	path('<int:calc_id>/maternalBrother', views.MaternalBrotherCreate.as_view(), name='maternalBrother'),
	path('<int:calc_id>/sonOfBrother', views.SonOfBrotherCreate.as_view(), name='sonOfBrother'),
	path('<int:calc_id>/sonOfPaternalBrother', views.SonOfPaternalBrotherCreate.as_view(), name='sonOfPaternalBrother'),
	path('<int:calc_id>/uncle', views.UncleCreate.as_view(), name='uncle'),
	path('<int:calc_id>/paternalUncle', views.PaternalUncleCreate.as_view(), name='paternalUncle'),
	path('<int:calc_id>/sonOfUncle', views.SonOfUncleCreate.as_view(), name='sonOfUncle'),
	path('<int:calc_id>/sonOfPaternalUncle', views.SonOfPaternalUncleCreate.as_view(), name='sonOfPaternalUncle'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:pk>/new-results/', views.NewResultsView.as_view(), name='new_results'),
	path('error/', views.error, name='error'),
	path('signup/', views.SignUp.as_view(), name='signup'),
]
