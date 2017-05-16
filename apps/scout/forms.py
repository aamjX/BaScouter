from django import forms
from datetime import *
from apps.scout.models import Player, Championship, Squad

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario para la edicion de la plantilla'''

'''----------------------------------------------------------------------------------------------------------'''

class SquadForm(forms.ModelForm):
    class Meta:
        model = Squad
        fields = [
            'title',
            'description',
        ]
        labels = {
            'title': 'Nombre de tu equipo',
            'description': 'Descripción',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Descripción'}),
        }

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario y renderizado de datos para la busqueda avanzada'''

'''----------------------------------------------------------------------------------------------------------'''

class BusquedaAvanzadaForm(forms.Form):

    #Seleccionando las competiciones

    competiciones = []
    objs_c = Championship.objects.all()
    for o in objs_c:
        tupla = (o.id, o.name)
        competiciones.append(tupla)

    #Seleccionando las nacionalidades
    nacionalidades = []
    objs_n = Player.objects.values('nationality').distinct()
    for i in range(len(objs_n)):
        tupla =(objs_n[i]['nationality'],objs_n[i]['nationality'])
        nacionalidades.append(tupla)

    #Seleccionando posiciones
    posiciones = []
    objs_p = Player.objects.values('position').distinct()
    for i in range(len(objs_p)):
        if objs_p[i]['position'] != '':
            tupla = (objs_p[i]['position'], objs_p[i]['position'])
            posiciones.append(tupla)
        else:
            next
    posiciones = sorted(tuple(posiciones))

    #Seleccionando proveedor
    proveedores = []
    objs_pro = Player.objects.values('outfitter').distinct()
    for i in range(len(objs_pro)):
        if objs_pro[i]['outfitter'] != '':
            tupla = (objs_pro[i]['outfitter'], objs_pro[i]['outfitter'])
            proveedores.append(tupla)
        else:
            next
    proveedores = sorted(tuple(proveedores))

    #Seleccionando agente
    agentes = []
    objs_a = Player.objects.values('agent').distinct()
    for i in range(len(objs_a)):
        if objs_a[i]['agent'] != '':
            tupla = (objs_a[i]['agent'], objs_a[i]['agent'])
            agentes.append(tupla)
        else:
            next
    agentes = sorted(tuple(agentes))

    #Pie
    pies = []
    pies.append(('Cualquiera', 'Cualquiera'))
    objs_pies = Player.objects.values('foot').distinct()
    for i in range(len(objs_pies)):
        if objs_pies[i]['foot'] != '':
            tupla = (objs_pies[i]['foot'], objs_pies[i]['foot'])
            pies.append(tupla)
        else:
            next
    pies = tuple(pies)

    def myStartDate(self):
        return datetime.date(year=date.today().year-20, month=date.today().month, day=date.today().day)

    def myEndDate(self):
        return datetime.date(year=date.today().year+10, month=date.today().month, day=date.today().day)

    nacionalidades = sorted(tuple(nacionalidades))

    utilizarRating = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onchange':'a_d_temporada();'}), required=False)
    temporada = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'disabled':'true'}), choices=(('16/17','16/17'),('15/16','15/16'), ('Toda la carrera deportiva del jugador','Toda la carrera deportiva del jugador')), required=False)
    agente = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices=agentes, required=False)
    proveedor = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices=proveedores,required=False)
    competicion = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=competiciones, required=False)
    nacionalidad = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices=nacionalidades, required=False)
    alias = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Alias'}), max_length=100, required=False)
    nombreCompleto = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Nombre completo'}),max_length=200, required=False)
    dorsal = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Dorsal'}),required=False)
    mayor_de = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'placeholder':'Mayor de'}),initial='01/01/1990')
    menor_de = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'placeholder':'Menor de'}),initial='01/01/2000')
    mayor_valor_de = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'min':'0'}),initial=0,required=False)
    menor_valor_de = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'min':'0'}),initial=1000000000, required=False)
    posicion = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices = posiciones,required=False)
    mayor_altura_de = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'min':'0', 'step':'0.1'}),initial=0,required=False)
    menor_altura_de = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'min':'0', 'step':'0.1'}),initial=2.5, required=False)
    pie = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control', 'placeholder':'pie'}),required=False, choices=pies)
    contratoHasta = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Año', 'min':'0'}), required=False)
    fichado = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Año'}), required=False)
    agente = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices=agentes, required=False)
    proveedor = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}), choices=proveedores,required=False)







