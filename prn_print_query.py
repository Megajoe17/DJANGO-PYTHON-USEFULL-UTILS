import inspect
from django.utils.encoding import smart_str
import re
from django.db import connection

def prn(value, level=0):

    max_level_show = 1

    def is_last_level(value):
        if type(value) in [unicode, long, float, int, str]:
            return 1
        return 0

    def print_like_string(value):
        if type(value) in [unicode, long, float, int, str, bool]:
            return smart_str(value)+'('+smart_str(type(value))+')'
        if type(value) in [list, dict, set]:
            return smart_str(value)+'('+smart_str(type(value))+')'
        return ''

    if level == 0:
        print ''
    if level == 0:
        frame = inspect.currentframe()
        try:
            context = inspect.getframeinfo(frame.f_back).code_context
            caller_lines = ''.join([line.strip() for line in context])
            m = re.search(r'echo\s*\((.+?)\)$', caller_lines)
            if m:
                caller_lines = m.group(1)
            print "********************   "+caller_lines.replace('prn(','')[:-1]+"  ***********************"
            print ''
        finally:
            del frame
        try:
            print smart_str(type(value))+' = '+smart_str(value)
        except:
            print 'no field found'

    print ''

    level_str = '   '
    cur_level = level
    while level!=0:
        level_str += '   '
        level -= 1


    if type(value) in [list, set]:
         for key, sub_value in enumerate(value):
             print level_str+'['+str(key)+'] = ' + print_like_string(sub_value)
             if cur_level < max_level_show and not is_last_level(sub_value):
                prn(sub_value,cur_level+1)
    elif type(value) in [dict, OrderedDict]:
         for key,sub_value in value.items():
             print level_str+'['+smart_str(key)+'] = ' + print_like_string(sub_value)

             if cur_level < max_level_show and not is_last_level(sub_value):
                prn(sub_value,cur_level+1)
    else:
        string_print = print_like_string(value)
        if string_print:
           print level_str + string_print
        else:
            try:
                for key in value.__dict__.keys():
                    cur_value = getattr(value, key)
                    try:
                        print level_str+'['+str(key)+'] = ' + print_like_string(cur_value)
                    except cur_value.EmptyResultSet:
                        print level_str+'['+str(key)+'] = no data'
                    if type(cur_value) in [dict, list]:
                        if cur_level < max_level_show and not is_last_level(cur_value) :
                            prn(cur_value, cur_level+1)
            except AttributeError:
                pass

    print '**********************************************************************'
    print ' '



def print_query():
    #print database all queries
    print ' '
    print '****DATABASE QUERY****'
    i = 1
    for i, query in enumerate(connection.queries):
        print str(i+1)+'. '+query['sql']
        print '         Time: '+query['time']

    print '****END DATABASE QUERY****'
    print ''
