from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView

from menu.forms import *
from .models import *


def recetas_modifier(request, pk):
    receta = Receta.objects.get(id=pk)
    form = RecetaForm(instance=receta)
    # Create the formset class
    RecetaCompFormset = inlineformset_factory(Receta, RecetaComp, exclude=[])
    # Create the formset
    formset = RecetaCompFormset(instance=receta, queryset=RecetaComp.objects.filter(receta=receta))

    try:
        err = request.GET['err']
    except KeyError:
        err = None

    dict = {
        "form": form
        , "formset": formset
        , "instance": receta
        , "error": err
    }

    if request.method == "POST":
        form = RecetaForm(request.POST, instance=receta)
        formset = RecetaCompFormset(request.POST, instance=receta)

        if form.is_valid() and formset.is_valid():
            client_mod = form.save()
            id = client_mod.id
            formset.save()

            # TODO redirect to receta view
            return HttpResponseRedirect(reverse('menu:recetas'))
        else:
            return HttpResponseRedirect(
                "/menu/recetas/%(id)s/?err=warning" % {"id": pk}
            )

    return render(request, 'menu/receta_edit_form.html', dict)


class IngredienteUpdateView(UpdateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = 'menu/ingrediente_edit.html'

    def dispatch(self, *args, **kwargs):
        self.item_id = kwargs['pk']
        return super(IngredienteUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        item = Ingrediente.objects.get(id=self.item_id)
        # TODO view edited item
        return redirect("menu:ingredientes")


def analisis(request):
    context = {
        'platillosgood': Platillo.objects.filter(bebida=False).order_by('-ganancia')[:5],
        'platillosbad': Platillo.objects.filter(bebida=False).order_by('ganancia')[:5],
        'bebidasgood': Platillo.objects.filter(bebida=True).order_by('-ganancia')[:5],
        'bebidasbad': Platillo.objects.filter(bebida=True).order_by('ganancia')[:5]
    }
    return render(request, 'menu/analisis.html', context)


def proveedores(request):
    if request.method == "POST":
        fields = {
            'restaurante': request.user.restaurante,
            'nombre': request.POST['nombre'],
            'telefono': request.POST['telefono'],
            'representante': request.POST['representante'],
            'telefono_de_representante': request.POST['telefono_de_representante'],
            'correo_electronico': request.POST['correo_electronico'],
        }
        Proveedor.objects.create(**fields)
        return HttpResponseRedirect(reverse('menu:proveedores'))
    else:
        prov = Proveedor.objects.filter(restaurante__id=request.user.restaurante.id)
        context = {
            'proveedores': prov,
            'form': ProveedorForm(),
        }
        return render(request, 'menu/proveedores.html', context)


def platillos(request):
    if request.method == "POST":
        return create_platillo(request)
    else:
        rest = request.user.restaurante
        plats = Platillo.objects.filter(restaurante__id=rest.id, bebida=False)
        context = {
            'restaurante': rest,
            'platillos': plats,
            'ingredientes': Ingrediente.objects.filter(restaurante__id=rest.id),
            'recetas': Receta.objects.filter(restaurante__id=rest.id),
            'tipo': 'platillo',
            'form': PlatilloForm(),
        }
        return render(request, 'menu/platillos.html', context)


def create_platillo(request):
    mi_ingredientes = Ingrediente.objects.filter(
        pk__in=request.POST.getlist('added-ing[]'))
    mi_recetas = Receta.objects.filter(
        pk__in=request.POST.getlist('added-rec[]'))
    fields = {
        'restaurante': request.user.restaurante,
        'nombre': request.POST['nombre'],
        'precio': request.POST['precio'],
        'bebida': 'bebidas' in request.resolver_match.view_name,
        'costo': 0  # temp for first save
    }
    cost = 0
    platillo = Platillo.objects.create(**fields)
    for ing in mi_ingredientes:
        q = float(request.POST['ing-' + str(ing.id)])
        ing_fields = {
            'platillo': platillo,
            'ingrediente': ing,
            'cantidad': q
        }
        cost += ing.unit_cost * q
        PlatilloIng.objects.create(**ing_fields)
    for rec in mi_recetas:
        q = float(request.POST['rec-' + str(rec.id)])
        rec_fields = {
            'platillo': platillo,
            'receta': rec,
            'cantidad': q
        }
        cost += rec.unit_cost * q
        PlatilloRec.objects.create(**rec_fields)
    platillo.costo = cost
    platillo.save()
    if 'bebidas' in request.resolver_match.view_name:
        redirect_to = 'menu:bebidas'
    else:
        redirect_to = 'menu:platillos'
    return redirect(redirect_to)


def del_platillo(request):
    for _id in request.POST.getlist('plat-del[]'):
        Platillo.objects.get(id=_id).delete()
    return redirect('menu:bebidas' if 'bebidas' in request.resolver_match.view_name else 'menu:platillos')


def bebidas(request):
    if request.method == "POST":
        return create_platillo(request)
    else:
        rest = request.user.restaurante
        plats = Platillo.objects.filter(restaurante__id=rest.id, bebida=True)
        context = {
            'restaurante': rest,
            'platillos': plats,
            'ingredientes': Ingrediente.objects.filter(restaurante__id=rest.id),
            'recetas': Receta.objects.filter(restaurante__id=rest.id),
            'tipo': 'bebida',
            'form': PlatilloForm(),
        }
        return render(request, 'menu/platillos.html', context)


def ingredientes(request):
    if request.method == "POST":
        fields = {
            'restaurante': request.user.restaurante,
            'nombre': request.POST['nombre'],
            'marca': request.POST['marca'],
            'proveedor': Proveedor.objects.get(
                id=request.POST['input-proveedor']),
            'costo': request.POST['costo'],
            'medida': request.POST['medida'],
            'cantidad': request.POST['cantidad']
        }
        Ingrediente.objects.create(**fields)
        return redirect('menu:ingredientes')
    else:
        context = {
            'restaurante': request.user.restaurante,
            'ingredientes': Ingrediente.objects.filter(restaurante__id=request.user.restaurante.id),
            'proveedores': Proveedor.objects.filter(restaurante__id=request.user.restaurante.id),
            'form': IngredienteForm(),
        }
        return render(request, 'menu/ingredientes.html', context)


def del_ingredient(request):
    for _id in request.POST.getlist('ing-del[]'):
        Ingrediente.objects.get(id=_id).delete()
    return redirect('menu:ingredientes')


def recetas(request):
    if request.method == "POST":
        mi_ingredientes = Ingrediente.objects.filter(
            pk__in=request.POST.getlist('added-ing[]'))
        fields = {
            'restaurante': request.user.restaurante,
            'nombre': request.POST['nombre'],
            'medida': request.POST['medida'],
            'cantidad': request.POST['cantidad'],
        }

        cost = 0
        receta = Receta.objects.create(**fields)
        for ing in mi_ingredientes:
            ing_fields = {
                'receta': receta,
                'ingrediente': ing,
                'cantidad': request.POST['ing-' + str(ing.id)]
            }
            cost += ing.costo
            RecetaComp.objects.create(**ing_fields)

        receta.costo = cost
        receta.save()

        return HttpResponseRedirect(reverse('menu:recetas'))
    else:
        form = RecetaForm()
        context = {
            'recetas': Receta.objects.filter(restaurante__id=request.user.restaurante.id),
            'ingredientes': Ingrediente.objects.filter(restaurante__id=request.user.restaurante.id),
            'form': form
        }
        return render(request, 'menu/recetas.html', context)


def del_receta(request):
    for _id in request.POST.getlist('rec-del[]'):
        Receta.objects.get(id=_id).delete()
    return redirect('menu:recetas')

