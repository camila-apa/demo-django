from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.
from .forms import MensagemForm
from .models import Mensagem, Tag

def index(request):
    mensagens = Mensagem.objects.all()
    return render(request, "home/index.html", {"mensagens": mensagens})

def sobre(request):
    return render(request, "home/sobre.html")

def nova_mensagem(request):
    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save()

            tags_texto = form.cleaned_data["tags"]
            for pedaco in tags_texto.split(","):
                nome = slugify(pedaco)
                if nome:
                    tag, _ = Tag.objects.get_or_create(nome=nome)
                    mensagem.tags.add(tag)
                messages.success(request, "Mensagem publicada com sucesso!")

            return redirect("index")
    else:
        form = MensagemForm()

    return render(request, "home/nova.html", {"form": form})