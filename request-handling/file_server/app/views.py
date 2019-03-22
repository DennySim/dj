import datetime, time, os

from django.shortcuts import render
from django.views.generic import TemplateView


class FileList(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, date=None):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        files = []
        file_dir = os.getcwd() + '/files/'
        filelist = os.listdir(file_dir)
        date_filter = None

        if date:
            date_items = date.split('-')
            date_items = [int(i) for i in date_items]
            date_filter = datetime.datetime(*date_items).timestamp()

        for file in filelist:

            file_path = file_dir + file
            statinfo = os.stat(file_path)
            ctime = statinfo.st_ctime
            mtime = statinfo.st_mtime

            if date_filter:
                if ctime < date_filter:
                    files.append({'name': file,
                                  'ctime': time.ctime(ctime),
                                  'mtime': time.ctime(mtime)})
            else:
                files.append({'name': file,
                              'ctime': time.ctime(ctime),
                              'mtime': time.ctime(mtime)})

        if date:
            return {
                'files': files,
                'date': time.ctime(date_filter)
                # 'date': datetime.date(date)  # Этот параметр необязательный
            }
        else:
            return {
                'files': files,
            }


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = os.getcwd() + '/files/' + name
    file_content = open(file_path, 'r')
    text = file_content.read()

    return render(
        request,
        'file_content.html',
        # context={'file_name': 'file_name_1.txt', 'file_content': 'File content!'}
        context={'file_name': name, 'file_content': text}
    )

