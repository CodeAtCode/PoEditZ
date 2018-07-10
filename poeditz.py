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


def reinsert_headers(original, updated):
        generated = open(updated, 'r')
        content = generated.read().splitlines()
        with open(original, 'r') as infile:
            for line in infile:
                if line.startswith('"X-Poedit'):
                    content.insert(4, line.replace('\n', ' ').replace('\r', ''))
                if line.startswith('#:'):
                    break
            infile.close()
        final = open(po_file, 'w')
        final.write("\n".join(content))
        final.close()


excluded = ''

for (header, value) in headers:
    if header.startswith('X-Poedit-SearchPathExcluded'):
        excluded += value + ','

command = 'wp i18n make-pot ' + folder + ' ' + temp_name + ' --skip-js --exclude=' + excluded + ' --merge=' + po_file
p = subprocess.check_output(command, shell=True)

reinsert_headers(po_file, temp_name)