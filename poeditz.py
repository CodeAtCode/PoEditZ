#!/usr/bin/python
import polib, sys, os, random

po = polib.pofile(sys.argv[1]) 
temp_name = '/tmp/temp_' + str(random.randint(0,999)) + '.po'
os.system('cp ' + sys.argv[1] + ' ' + temp_name)
headers = po.ordered_metadata()
folder = '/var/www/VVV/www/demo/htdocs/wp-content/plugins/glossary-pro/'

def is_excluded(folder, file, excluded):
    for exclude in excluded:
        if exclude.endswith('.php') and file.endswith('.php'):
            if exclude in os.path.join(folder,file):
                return True
        elif exclude in folder:
            return True
    return False

files_list = ''
excluded = []
keyword = ''

for (header,value) in headers:
    if header.startswith('X-Poedit'):
        if header.startswith('X-Poedit-KeywordsList'):
            keyword = '--keyword=' + value.replace(';',',') + ''
        if header.startswith('X-Poedit-SearchPathExcluded'):
            excluded.append(value)
            
for root, dirs, files in os.walk(folder):
    for file in files:
        if not is_excluded(root, file, excluded):
            if file.endswith('.php'):
                files_list += os.path.join(root, file) + ' '

command = 'xgettext ' + keyword + ' --force-po --debug -c --join-existing --output=' + temp_name + ' ' + files_list
os.system(command)
