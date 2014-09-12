import operator
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import os
import random
import string
from PIL import Image, ImageEnhance
from django.utils.encoding import smart_str
import shutil
from sorl.thumbnail import get_thumbnail
from HTMLParser import HTMLParser
from settings import MEDIA_ROOT
global str


def get_ajax_form_errors(form):
    '''
    Get form errors for ajax request
    '''
    fields = {}

    for k,v in form.errors.items():
        fields[k] = ''
        for e in v:
            fields[k] += unicode(e)

    return fields


def get_main_user_name(user):
    '''
    Get form errors for ajax request
    '''
    try:
        return user.email[0:user.email.index('@')]
    except:
        return 'undefined name'

def random_string(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def site_url(request):
    return 'http://' + request.META['HTTP_HOST']


def model_add_related(main_items, parent_name, RelatedModel, related_name):

    if type(main_items) is list:
        main_list = OrderedDict()
        for obj in main_items:
            main_list[obj.id] = obj
        id_parent = [obj.id for obj in main_items]
    else:
        main_list = OrderedDict()
        for item in main_items:
            main_list[item.id] = item
        id_parent = [key for key,obj in main_list.items()]

    parent_name_in = "".join([parent_name,'__id__in'])
    sort_params = {parent_name_in:id_parent}
    found_related = RelatedModel.objects.filter(**sort_params)
    relation_dict = {}
    parent_name_id = "".join([parent_name,'_id'])
    for obj in found_related:
        relation_dict.setdefault(getattr(obj,parent_name_id), []).append(obj)
    for id, related_items in relation_dict.items():
        if not hasattr(main_list[id],related_name):
            setattr(main_list[id],related_name,related_items)

    return main_list


def url_get_param_replace(request, field, value):

    dict_ = request.GET.copy()
    if value:
        dict_[field] = value
    else:
        if field in dict_:
            del dict_[field]

    return dict_.urlencode()

def count_to_right_str(count, variant_1, variant_3, variant_7):
    # variant_1 - пример 1-год, 1-день
    # variant_3 - пример 3-года, 3-дня
    # variant_7 - пример 7-лет, 5-дней
    count = 1230
    if count != 0:
        if count > 100:
            num = int(str(count)[-2:])
        else:
            num = count
        if 5 <= num <= 14:
            result = variant_7
        else:
            num = int(str(num)[-1:])
            if num == 0 or 5 <= num <=9:
                result = variant_7
            if num == 1:
                result = variant_1
            if 2 <= num <= 4:
                result = variant_3
        return result
    else:
        return variant_7

def clean_folder(target_dir=''):
        # Gather directory contents
    contents = [os.path.join(target_dir, i) for i in os.listdir(target_dir)]

    # Iterate and remove each item in the appropriate manner
    [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]

    return 1


from sorl.thumbnail import delete

def add_watermark(main_folder, image_file, path_watermark, all_size={'x':0,'x2':100,'y':0,'y2':100},opacity=0.5):
    if all_size['x']=="" or all_size['x2']=="" or all_size['y']=="" \
        or all_size['y2']=="" or all_size['w_view']=="" or all_size['h_view']=="":
        return False

    path_to_folder = MEDIA_ROOT + main_folder
    result_file = WATERMARK_PREFIX + image_file
    path_watermark = MEDIA_ROOT + path_watermark

    if os.path.isfile(path_to_folder+image_file):
        shutil.copyfile(path_to_folder+image_file, path_to_folder+result_file)

        if os.path.isfile(path_to_folder+result_file):
            os.chmod(path_to_folder+result_file, 0755)
            result_file_path = path_to_folder+result_file

            # Открываем текущее изобразение изображение
            image = Image.open(result_file_path, 'r')

            w_orig = image.size[0]
            h_orig = image.size[1]
            w_koef = float(w_orig)/int(all_size['w_view'])
            h_koef = float(h_orig)/int(all_size['h_view'])

            x = int(int(all_size['x'])*w_koef)
            x2 = int(int(all_size['x2'])*w_koef)
            y = int(int(all_size['y'])*h_koef)
            y2 = int(int(all_size['y2'])*h_koef)
            w_watermark = x2 - x
            h_watermark = y2 - y

            if w_watermark!=0 and h_watermark!=0:
                watermark_size = str(w_watermark)+'x'+str(h_watermark)
                path_watermark = MEDIA_ROOT.replace('/media/','')+get_thumbnail(path_watermark, watermark_size,
                                                           crop='center', quality=99).url
                # Открываем водяной знак
                if os.path.isfile(path_watermark):
                    watermark = Image.open(path_watermark, 'r')
                    assert opacity >= 0 and opacity <= 1
                    if opacity < 1:
                        if watermark.mode != 'RGBA':
                            watermark = watermark.convert('RGBA')
                        else:
                            watermark = watermark.copy()
                        alpha = watermark.split()[3]
                        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                        watermark.putalpha(alpha)

                    layer = Image.new('RGBA', image.size, (0,0,0,0))
                    layer.paste(watermark, (x, y))

                    Image.composite(layer,  image,  layer).save(result_file_path)
                    Image.composite(layer,  image,  layer).save(result_file_path)



                    # Delete the Key Value Store reference but **not** the file.
                    # Use this if you have changed the source
                    delete(main_folder + result_file, delete_file=False)

                    return result_file
    return False

def copyFile(path, dest, relative=0):
    if os.path.isfile(path):
        if len(path) > 255:
            if os.sep in path:
                moveTo, path = path.split(os.sep, 1)
                os.chdir(moveTo)
                copyFile(path, dest, relative + 1)
        else:
            src_filename = path[path.rfind(os.sep)+1:]
            if len(src_filename)>100:
                return 0

            path_base = ['..'] * relative
            path_rel = path_base + [dest]
            shutil.copyfile(path, os.path.join(*path_rel))
            if os.path.isfile(os.path.join(*path_rel)):
                return 1
    return 0


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

