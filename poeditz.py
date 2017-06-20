#!/usr/bin/python
import polib, sys, os, random, subprocess

if not os.path.isfile(sys.argv[1]):
    sys.exit(0)
po_file = sys.argv[1]
if not os.path.exists(sys.argv[2]):
    sys.exit(0)
folder = sys.argv[2]

po = polib.pofile(po_file)
temp_name = '/tmp/temp_' + str(random.randint(0, 999)) + '.po'
os.system('cp ' + sys.argv[1] + ' ' + temp_name)
headers = po.ordered_metadata()


def is_excluded(folder, file, excluded):
    for exclude in excluded:
        if exclude.endswith('.php') and file.endswith('.php'):
            if exclude in os.path.join(folder, file):
                return True
        elif exclude in folder:
            return True
    return False


def replace_headers(original, updated):
        with open(original, 'r') as infile:
            headers = []
            for line in infile:
                headers.append(line)
                if line.startswith('#:'):
                     break
            infile.close()
        outfile = open(updated, 'r')
        i = 0
        for line in outfile:
            i += 1
            if line.startswith('#:'):
                break
        lines = list(outfile)
        outfile.close()
        outfile = open(updated, 'w')
        del lines[i - 1]
        lines = headers + lines
        lines = "\n".join(lines)
        outfile.write(lines)
        outfile.close()


files_list = ''
excluded = []
keyword = ''

for (header, value) in headers:
    if header.startswith('X-Poedit'):
        if header.startswith('X-Poedit-KeywordsList'):
            keywords = value.split(';')
            for single in keywords:
                keyword += '--keyword="' + single + '" '
        if header.startswith('X-Poedit-SearchPathExcluded'):
            excluded.append(value)

for root, dirs, files in os.walk(folder):
    for file in files:
        if not is_excluded(root, file, excluded):
            if file.endswith('.php'):
                files_list += os.path.join(root, file) + ' '

command = 'xgettext ' + keyword + ' --force-po --from-code=UTF-8'
command += ' --output=' + temp_name + ' ' + files_list
p = subprocess.check_output(command, shell=True)

command = 'msgmerge -N -U ' + po_file + ' ' + temp_name + ' 2>/dev/null'
p = subprocess.check_output(command, shell=True)

# Fix warning
command = 'sed --in-place ' + temp_name + ' --expression=s/CHARSET/UTF-8/'
p = subprocess.check_output(command, shell=True)

command = 'msguniq ' + temp_name + ' -o ' + temp_name + ' 2>&1'
p = subprocess.check_output(command, shell=True)

replace_headers(po_file, temp_name)

command = 'mv ' + temp_name + ' ' + po_file
os.system(command)

command = 'rm ' + po_file + '~'
os.system(command)
