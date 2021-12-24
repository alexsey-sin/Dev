# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from app.forms import NameForm, LizaPhraseForm, GermanPhraseForm
from app.models import LizaGroupPhrase, LizaPhrase, GermanGroupPhrase, GermanPhrase, File, Name
from datetime import datetime as dt
from django.contrib.auth import get_user_model
import os
from core.settings import MEDIA_ROOT



User = get_user_model()


@login_required(login_url="/login/")
def index(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    return render(request, 'app/index.html', context)
    
    
@login_required(login_url="/login/")
def names(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    data = []
    if request.method == 'POST':
        form = NameForm(request.POST)
        id_edit = request.POST.get('edit', None)
        id_delete = request.POST.get('delete', None)

        if id_edit:  # редактирование
            try:
                rec = get_object_or_404(Name, id=id_edit)
                rec.text = request.POST.get("text")
                rec.sex = request.POST.get("sex")
                rec.short_names = request.POST.get("short_names")
                rec.author = user
                rec.save()
            except:
                context['error_mess'] = 'Ошибка редактирования, возможно такое имя уже существует.'
        elif id_delete:
            rec = get_object_or_404(Name, id=id_delete)
            rec.delete()
        elif form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = user
            new_form.save()
        else:
            context['error_mess'] = 'Ошибка заполнения формы, возможно такое имя уже существует.'

    form = NameForm()
    context['form'] = form
    data = Name.objects.order_by('text')

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['segment'] = 'people_names'
    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'app/names.html', context)


@login_required(login_url="/login/")
def lizagroup(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    data = []
    if request.method == 'POST':
        id_group = request.POST.get('group_id', None)
        new_priority = request.POST.get('priority_value', None)
        newphrase = request.POST.get('newphrase_value', None)

        if new_priority and id_group:
            group = get_object_or_404(LizaGroupPhrase, id=id_group)
            group.priority = new_priority
            group.save()
        elif newphrase and id_group:
            try:
                n_phrase = LizaPhrase()
                n_phrase.text = newphrase
                group = get_object_or_404(LizaGroupPhrase, id=id_group)
                n_phrase.group = group
                n_phrase.author = user
                n_phrase.save()
            except:
                context['error_mess'] = 'Ошибка, возможно такая фраза уже существует.'
        else:
            context['error_mess'] = 'Ошибка редактирования/добавления.'

    gr_phrases = LizaGroupPhrase.objects.order_by('num_group')
    if gr_phrases:
        for gr in gr_phrases:
            group = {}
            group['id'] = gr.id
            group['num_group'] = gr.num_group
            group['priority'] = gr.priority
            group['text'] = gr.text
            phrase = LizaPhrase.objects.filter(group=gr.id).order_by('-pub_date')
            last = LizaPhrase.objects.filter(group=gr.id).order_by('pub_date').last()
            author = ''
            if last:
                str_date = last.pub_date.strftime('%H:%M %d.%m.%Y')
                author = last.author.get_full_name()
                if author.strip() == '':
                    author = last.author.username
                group['last_date'] = str_date
            group['author'] = author
            group['cnt_phrases'] = phrase.count()
            group['phrases'] = []
            c = 5
            for ptr in phrase:
                group['phrases'].insert(0, ptr.text)
                c -= 1
                if c == 0:
                    break
            data.append(group)
    else:
        context['error_mess'] = 'Нет групп фраз.'

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['segment'] = 'phrasesLiza'
    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request,'app/LizaGroup.html', context)


@login_required(login_url="/login/")
def lizaphrases(request, id_group):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    group = get_object_or_404(LizaGroupPhrase, id=id_group)
    context['group_name'] = group.text
    
    if request.method == 'POST':
        form = LizaPhraseForm(request.POST or None)
        id_edit = request.POST.get('edit', None)
        id_delete = request.POST.get('delete', None)

        if id_edit:  # редактирование
            try:
                rec = get_object_or_404(LizaPhrase, id=id_edit)
                rec.text = request.POST.get("text")
                rec.author = user
                rec.save()
            except:
                context['error_mess'] = 'Ошибка редактирования, возможно такая фраза уже существует.'
        elif id_delete:
            rec = get_object_or_404(LizaPhrase, id=id_delete)
            rec.delete()
        elif form.is_valid():
            new_form = form.save(commit=False)
            new_form.group = group
            new_form.author = user
            new_form.save()
        else:
            context['error_mess'] = 'Ошибка заполнения формы, возможно такая фраза уже существует.'

    form = LizaPhraseForm()
    context['form'] = form

    data = LizaPhrase.objects.filter(group=group.id).order_by('pub_date')
    context['cnt_phrases'] = data.count()
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'app/LizaPhrase.html', context)


@login_required(login_url="/login/")
def germangroup(request):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    data = []
    if request.method == 'POST':
        id_group = request.POST.get('group_id', None)
        new_priority = request.POST.get('priority_value', None)
        newphrase = request.POST.get('newphrase_value', None)
        group_answer_id = request.POST.get('group_answer_id', None)

        if new_priority and id_group:
            group = get_object_or_404(GermanGroupPhrase, id=id_group)
            group.priority = new_priority
            group.save()
        elif newphrase and id_group:
            try:
                n_phrase = GermanPhrase()
                n_phrase.text = newphrase
                group = get_object_or_404(GermanGroupPhrase, id=id_group)
                n_phrase.group = group
                n_phrase.author = user
                n_phrase.save()
            except:
                context['error_mess'] = 'Ошибка, возможно такая фраза уже существует.'
        elif group_answer_id:
            group = get_object_or_404(GermanGroupPhrase, id=group_answer_id)
            files = request.FILES.getlist('newAnswerFile')
            if files:
                for f in files:
                    fl = File()
                    fl.file = f
                    fl.group = group
                    fl.author = user
                    fl.save()
        else:
            context['error_mess'] = 'Ошибка редактирования/добавления.'


    gr_phrases = GermanGroupPhrase.objects.order_by('num_group')
    if gr_phrases:
        for gr in gr_phrases:
            group = {}
            group['id'] = gr.id
            group['num_group'] = gr.num_group
            group['priority'] = gr.priority
            group['text'] = gr.text
            phrase = GermanPhrase.objects.filter(group=gr.id).order_by('-pub_date')
            last_phrase = GermanPhrase.objects.filter(group=gr.id).order_by('pub_date').last()
            author = ''
            if last_phrase:
                str_date = last_phrase.pub_date.strftime('%H:%M %d.%m.%Y')
                author = last_phrase.author.get_full_name()
                if author.strip() == '':
                    author = last_phrase.author.username
                group['last_date_phrase'] = str_date
            group['author_phrase'] = author
            group['cnt_phrases'] = phrase.count()
            group['phrases'] = []
            c = 5
            for ptr in phrase:
                group['phrases'].insert(0, ptr.text)
                c -= 1
                if c == 0:
                    break
            files = File.objects.filter(group=gr.id).order_by('-pub_date')
            last_files = File.objects.filter(group=gr.id).order_by('pub_date').last()
            author = ''
            if last_files:
                str_date = last_files.pub_date.strftime('%H:%M %d.%m.%Y')
                author = last_files.author.get_full_name()
                if author.strip() == '':
                    author = last_files.author.username
                group['last_date_answer'] = str_date
            group['author_answer'] = author
            group['answers'] = []
            c = 5
            for fl in files:
                group['answers'].insert(0, os.path.basename(fl.file.name))
                c -= 1
                if c == 0:
                    break
            data.append(group)
    else:
        context['error_mess'] = 'Нет групп фраз.'

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['segment'] = 'phrasesGerman'
    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'app/GermanGroup.html', context)


@login_required(login_url="/login/")
def germanphrases(request, id_group):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    group = get_object_or_404(GermanGroupPhrase, id=id_group)
    context['group_name'] = group.text
    
    if request.method == 'POST':
        form = GermanPhraseForm(request.POST or None)
        id_edit = request.POST.get('edit', None)
        id_delete = request.POST.get('delete', None)

        if id_edit:  # редактирование
            try:
                rec = get_object_or_404(GermanPhrase, id=id_edit)
                rec.text = request.POST.get("text")
                rec.author = user
                rec.save()
            except:
                context['error_mess'] = 'Ошибка редактирования, возможно такая фраза уже существует.'
        elif id_delete:
            rec = get_object_or_404(GermanPhrase, id=id_delete)
            rec.delete()
        elif form.is_valid():
            new_form = form.save(commit=False)
            new_form.group = group
            new_form.author = user
            new_form.save()
        else:
            context['error_mess'] = 'Ошибка заполнения формы, возможно такая фраза уже существует.'

    form = GermanPhraseForm()
    context['form'] = form

    data = GermanPhrase.objects.filter(group=group.id).order_by('pub_date')

    context['cnt_phrases'] = data.count()
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'app/GermanPhrase.html', context)


@login_required(login_url="/login/")
def germananswers(request, id_group):
    user = request.user
    u_name = user.get_full_name()
    if u_name.strip() == '':
        u_name = user.username
    context = {'u_name': u_name}

    group = get_object_or_404(GermanGroupPhrase, id=id_group)
    context['group_name'] = group.text
    
    if request.method == 'POST':
        id_delete = request.POST.get('delete', None)
        group_answer_id = request.POST.get('group_answer_id', None)

        if id_delete:
            rec = get_object_or_404(File, id=id_delete)
            rec.delete()
        elif group_answer_id:
            files = request.FILES.getlist('newAnswerFile')
            if files:
                for f in files:
                    fl = File()
                    fl.file = f
                    fl.group = group
                    fl.author = user
                    fl.save()
        else:
            context['error_mess'] = 'Ошибка редактирования/добавления.'

    data = []
    files = File.objects.filter(group=group).order_by('pub_date')
    for fl in files:
        row = {
            'file_url': fl.file.url,
            'id': fl.id,
            'filename': os.path.basename(fl.file.name),
            'author': fl.author,
            'pub_date': fl.pub_date,
        }
        data.append(row)

    context['id_group'] = id_group
    context['cnt_answers'] = len(data)
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context['page_number'] = page_number
    context['page'] = page
    context['paginator'] = paginator

    return render(request, 'app/GermanAnswer.html', context)

###############################################################################
###############################################################################
backup_data = {
    'backupfolder': 'backup/',
    'nestedfolder': 'last/',
    'filename_names': 'names.txt',
    'filename_liza_gr_phrases': 'liza_gr_phrases.txt',
    'filename_liza_phrases': 'liza_phrases.txt',
    'filename_german_gr_phrases': 'german_gr_phrases.txt',
    'filename_german_phrases': 'german_phrases.txt',
    'filename_german_answers': 'german_answers.txt',
}
@login_required(login_url="/login/")
def backup(request):
    '''
        Ссылки доступны только суперпользователю.

        http://django.domconnect.ru/backup
        http://127.0.0.1:8000/backup

        Функция для резервного копирования данных таблиц Name, LizaGroupPhrase, LizaPhrase.
        Сохранение происходит в папку backup/last/ если её нет, она создается.
        Создаются файлы с именами соответствующих таблиц и расширением txt

    '''
    # Проверяем пользователя
    user = request.user
    if request.POST or not user.is_superuser:
        return redirect(reverse('app:home'))
    
    result = ''
    message = ''
    cnt_err = 0

    # Проверяем путь
    filepath = backup_data['backupfolder']
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filepath += backup_data['nestedfolder']
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    # ============= модель Name ============= 
    buffer = ''
    try:
        names = Name.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        names = None
    if names:
        cnt_i = 0
        for n in names:
            r = n.sex + ';' + n.text + ';' + n.short_names + ';' + n.pub_date.strftime('%H:%M %d.%m.%Y') + ';' + n.author.username + '\n'
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_names']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели Name<br>'

        message += f'Модель: Name -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: Name -> нет записей.<br>'

    # ============= модель LizaGroupPhrase ============= 
    buffer = ''
    try:
        grphrases = LizaGroupPhrase.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        grphrases = None
    if grphrases:
        cnt_i = 0
        for gr in grphrases:
            r = gr.text + ';' + str(gr.num_group) + ';' + str(gr.priority) + '\n'
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_liza_gr_phrases']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели LizaGroupPhrase<br>'

        message += f'Модель: LizaGroupPhrase -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: LizaGroupPhrase -> нет записей.<br>'

    # ============= модель LizaPhrase ============= 
    buffer = ''
    try:
        phrases = LizaPhrase.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        phrases = None
    if phrases:
        cnt_i = 0
        for phr in phrases:
            r = (phr.text + ';' + str(phr.group.num_group) + ';' + phr.pub_date.strftime('%H:%M %d.%m.%Y')
                + ';' + phr.author.username + '\n')
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_liza_phrases']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели LizaPhrase<br>'

        message += f'Модель: LizaPhrase -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: LizaPhrase -> нет записей.<br>'

    # ============= модель GermanGroupPhrase ============= 
    buffer = ''
    try:
        grphrases = GermanGroupPhrase.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        grphrases = None
    if grphrases:
        cnt_i = 0
        for gr in grphrases:
            r = gr.text + ';' + str(gr.num_group) + ';' + str(gr.priority) + '\n'
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_german_gr_phrases']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели GermanGroupPhrase<br>'

        message += f'Модель: GermanGroupPhrase -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: GermanGroupPhrase -> нет записей.<br>'

    # ============= модель GermanPhrase ============= 
    buffer = ''
    try:
        phrases = GermanPhrase.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        phrases = None
    if phrases:
        cnt_i = 0
        for phr in phrases:
            r = (phr.text + ';' + str(phr.group.num_group) + ';' + phr.pub_date.strftime('%H:%M %d.%m.%Y')
                + ';' + phr.author.username + '\n')
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_german_phrases']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели GermanPhrase<br>'

        message += f'Модель: GermanPhrase -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: GermanPhrase -> нет записей.<br>'

    # ============= модель File ============= 
    buffer = ''
    try:
        files = File.objects.all()
    except:
        cnt_err += 1
        message += 'Ошибка загрузки модели Name<br>'
        files = None
    if files:
        cnt_i = 0
        for fl in files:
            r = (fl.file.name + ';' + str(fl.group.num_group) + ';' + fl.pub_date.strftime('%H:%M %d.%m.%Y')
                + ';' + fl.author.username + '\n')
            buffer += r
            cnt_i += 1
        try:
            filename = filepath + backup_data['filename_german_answers']
            with open(filename, 'w', encoding='utf-8') as outfile:
                outfile.write(buffer)
        except:
            cnt_err += 1
            message += 'Ошибка сохранения модели File<br>'

        message += f'Модель: File -> сохранено {cnt_i} записей.<br>'
    else:
        message += 'Модель: File -> нет записей.<br>'

    # ============================================== 
    if cnt_err:
        result = f'Errors: {cnt_err}'
        result_style = 'danger'
    else:
        result = 'Ok'
        result_style = 'success'
    
    context = {
        'result': result,
        'message': message,
        'result_style': result_style,
    }
    return render(request, 'app/show_mess_and_redirect.html', context)


@login_required(login_url="/login/")
def restore(request):
    '''
        Ссылки доступны только суперпользователю.

        http://django.domconnect.ru/restore
        http://127.0.0.1:8000/restore

        Функция для восстановления данных таблиц Name, GroupPhrase, Phrase.
        Загрузка происходит из папки backup/last/
        Перед операцией восстановления проверяется наличие файлов всех таблиц.
        Внимание! Перед восстановлением все данные из таблиц удаляются.

    '''
    # Проверяем пользователя
    user = request.user
    if request.POST or not user.is_superuser:
        return redirect(reverse('app:home'))

    result = ''
    message = ''
    cnt_err = 0

    # ============= модель Name ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_names']
    if os.path.exists(filename):
        Name.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    name = Name()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели Name.<br>'
                    break
                
                lst = row.split(';')
                name.sex = lst[0].strip()
                name.text = lst[1].strip()
                name.short_names = lst[2].strip()
                name.pub_date = dt.strptime(lst[3].strip(), '%H:%M %d.%m.%Y')
                try:
                    r_user = User.objects.get(username=lst[4].strip())
                except:
                    r_user = user
                name.author = r_user
                name.save()
                cnt_i += 1
        message += f'Модель: Name -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели Name. Нет файла {backup_data["filename_names"]}<br>'

    # ============= модель LizaGroupPhrase ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_liza_gr_phrases']
    if os.path.exists(filename):
        LizaGroupPhrase.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    grphrase = LizaGroupPhrase()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели LizaGroupPhrase.<br>'
                    break
                
                lst = row.split(';')
                grphrase.text = lst[0].strip()
                grphrase.num_group = int(lst[1].strip())
                grphrase.priority = int(lst[2].strip())
                grphrase.save()
                cnt_i += 1
        message += f'Модель: LizaGroupPhrase -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели LizaGroupPhrase. Нет файла {backup_data["filename_liza_gr_phrases"]}<br>'

    # ============= модель LizaPhrase ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_liza_phrases']
    if os.path.exists(filename):
        LizaPhrase.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    phrase = LizaPhrase()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели LizaPhrase.<br>'
                    break
                
                lst = row.split(';')
                phrase.text = lst[0].strip()
                try:
                    group = LizaGroupPhrase.objects.get(num_group=lst[1].strip())
                except:
                    cnt_err += 1
                    message += f'Ошибка создания объекта модели LizaPhrase. Не найдена группа по номеру {lst[1].strip()}<br>'
                    break
                phrase.group = group
                phrase.pub_date = dt.strptime(lst[2].strip(), '%H:%M %d.%m.%Y')
                try:
                    r_user = User.objects.get(username=lst[3].strip())
                except:
                    r_user = user
                phrase.author = r_user
                phrase.save()
                cnt_i += 1
        message += f'Модель: LizaPhrase -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели LizaPhrase. Нет файла {backup_data["filename_liza_phrases"]}<br>'

    # ============= модель GermanGroupPhrase ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_german_gr_phrases']
    if os.path.exists(filename):
        GermanGroupPhrase.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    grphrase = GermanGroupPhrase()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели GermanGroupPhrase.<br>'
                    break
                
                lst = row.split(';')
                grphrase.text = lst[0].strip()
                grphrase.num_group = int(lst[1].strip())
                grphrase.priority = int(lst[2].strip())
                grphrase.save()
                cnt_i += 1
        message += f'Модель: GermanGroupPhrase -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели GermanGroupPhrase. Нет файла {backup_data["filename_german_gr_phrases"]}<br>'

    # ============= модель GermanPhrase ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_german_phrases']
    if os.path.exists(filename):
        GermanPhrase.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    phrase = GermanPhrase()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели GermanPhrase.<br>'
                    break
                
                lst = row.split(';')
                phrase.text = lst[0].strip()
                try:
                    group = GermanGroupPhrase.objects.get(num_group=lst[1].strip())
                except:
                    cnt_err += 1
                    message += f'Ошибка создания объекта модели GermanPhrase. Не найдена группа по номеру {lst[1].strip()}<br>'
                    break
                phrase.group = group
                phrase.pub_date = dt.strptime(lst[2].strip(), '%H:%M %d.%m.%Y')
                try:
                    r_user = User.objects.get(username=lst[3].strip())
                except:
                    r_user = user
                phrase.author = r_user
                phrase.save()
                cnt_i += 1
        message += f'Модель: GermanPhrase -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели GermanPhrase. Нет файла {backup_data["filename_german_phrases"]}<br>'

    # ============= модель File ============= 
    # Проверяем файл
    filename = backup_data['backupfolder'] + backup_data['nestedfolder'] + backup_data['filename_german_answers']
    if os.path.exists(filename):
        File.objects.all().delete()
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = infile.readlines()
            cnt_i = 0
            for row in reader:
                try:
                    file = File()
                except:
                    cnt_err += 1
                    message += 'Ошибка создания объекта модели File.<br>'
                    break
                
                lst = row.split(';')
                f_name = lst[0].strip()
                full_name = os.path.join(MEDIA_ROOT, f_name)
                if not os.path.exists(full_name):
                    break
                file.file = f_name
                try:
                    group = GermanGroupPhrase.objects.get(num_group=lst[1].strip())
                except:
                    cnt_err += 1
                    message += f'Ошибка создания объекта модели File. Не найдена группа по номеру {lst[1].strip()}<br>'
                    break
                file.group = group
                file.pub_date = dt.strptime(lst[2].strip(), '%H:%M %d.%m.%Y')
                try:
                    r_user = User.objects.get(username=lst[3].strip())
                except:
                    r_user = user
                file.author = r_user
                file.save()
                cnt_i += 1
        message += f'Модель: File -> загружено {cnt_i} записей.<br>'
    else:
        cnt_err += 1
        message += f'Ошибка загрузки модели File. Нет файла {backup_data["filename_german_answers"]}<br>'

    # ============================================== 
    if cnt_err:
        result = f'Errors: {cnt_err}'
        result_style = 'danger'
    else:
        result = 'Ok'
        result_style = 'success'
    
    context = {
        'result': result,
        'message': message,
        'result_style': result_style,
    }
    return render(request, 'app/show_mess_and_redirect.html', context)
###############################################################################
###############################################################################


@login_required(login_url="/login/")
def load(request):  # http://127.0.0.1:8000/load/
    import json
    # Проверяем пользователя
    user = request.user
    if request.POST or not user.is_superuser:
        return redirect(reverse('app:home'))
    
    # from core.settings import MEDIA_ROOT

    # print(MEDIA_ROOT)
    # f_name = os.path.join(MEDIA_ROOT, 'audio/wav/zvuk1.wav')
    # f_name = MEDIA_ROOT + '/' + 'audio/wav/zvuk1.wav'
    # if os.path.exists(f_name):
    #     print(f_name)
#     except:
    #         message = 'Ошибка сохранения'
    # elif target == 'load_groupphrases':  # http://127.0.0.1:8000/backup/load_groupphrases
    #     filename = backupfolder + nestedfolder + filename_gr_phrases
    #         except:
    #             message = 'Ошибка загрузки'
    #     else:
    #         message = 'Нет файла'
    # elif target == 'save_phrases':  # http://127.0.0.1:8000/backup/save_phrases
    #     pass
    # elif target == 'load_phrases':  # http://127.0.0.1:8000/backup/load_phrases
    #     pass



    
    # group = get_object_or_404(GroupPhrase, num_group=num_group)
    # phrases = Phrase.objects.filter(group=group).order_by('text')
    # lst = []
    # for phr in phrases:
    #     lst.append(phr.text)
   # group = get_object_or_404(GroupPhrase, num_group=6)
    # with open('tp.txt', 'r', encoding='utf-8') as f:
    #     reader = f.readlines()
    #     for row in reader:
    #         phrase = Phrase()
    #         phrase.text = row.strip()
    #         phrase.group = group
    #         phrase.author = user
    #         try:
    #             phrase.save()
    #             cnt += 1
    #         except:
    #             err += 1




    # cnt = 0
    # with open('NAME.csv', 'r', encoding='utf-8') as f:
    #     reader = f.readlines()
    #     for row in reader:
    #         lst = row.split(sep=';')
    #         nic = lst[1]
    #         dct = json.loads(lst[2])
    #         sex = dct.get('sex').upper()
    #         name = dct.get('name')
    #         print(name)
    #         rec = Name()
    #         rec.text = name
    #         rec.sex = sex
    #         rec.author = user
    #         rec.short_names = nic
    #         rec.save()
    #         cnt += 1

    # print('loaded:', cnt)

    # return redirect('app:names')
    return redirect(reverse('app:home'))


@login_required(login_url="/login/")
def clear(request):  # http://127.0.0.1:8000/clear/
    user = request.user
    if not user.is_superuser:
        return redirect(reverse('app:home'))

    # Name.objects.all().delete()
    # return redirect('app:tables', get_table='people_names')


    # group = get_object_or_404(GroupPhrase, num_group=6)
    # phrases = Phrase.objects.filter(group=group)
    # for phr in phrases:
    #     phr.delete()

    return redirect(reverse('app:home'))

###############################################################################
###############################################################################
