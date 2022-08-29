import os
import datetime 

print ('updating')

day = str(datetime.datetime.now())[:10]

root_path = os.getcwd() # gets current dir

os.chdir (os.path.join(root_path, '..')) # goes to parent sub_dir (reed)

curr_path = os.getcwd()

paths = {}
courses = []

def addPDF (course, folder, week, _file):

    _path = os.path.join ( curr_path, folder, week, _file )

    _out = os.path.join ( root_path , folder )

    if (not os.path.isdir (_out)):
        
        os.system (f"mkdir '{_out}'")

    cmd = f"cp '{_path}' '{_out}/{week}.pdf'"

    if (not os.path.isfile (f"'{_out}/{week}.pdf'")):

        os.system (cmd)
    
    paths[course].append(f'{course}/{week}.pdf')
    courses.append (course)

# updates all pdfs within a course
def updatePDF (course):

    paths[course] = []

    for folder in os.listdir  (curr_path):

        if (folder == course):

            for week in os.listdir (os.path.join (curr_path, folder)):

                if (week[0:1] != 'W'):
                    continue

                for _file in os.listdir( os.path.join (curr_path, folder, week ) ):

                    if (_file[-3:] == 'ynb'):
                        
                        _p = os.path.join( curr_path, folder, week )

                        os.system (f'jupyter nbconvert --to PDF "{_p}/{week}.ipynb"')

                    if (_file[-3:] == 'pdf'):

                        addPDF (course, folder, week, _file)

updatePDF('Math 111')
updatePDF('csci122')
updatePDF('Soc 221')

print (paths)

info_text = "## Information\nHi! I'm [Skye Kychenthal](https://www.skymocha.net). The purpose of this website is to facilitate an easier sharing of my homework for the purposes of collaboration! I am currently a freshmen at Reed College, so below is are the current classes I am taking, and the current work that I have published to this website. If you want a more detailed look at who I am, check out:\n\n* [www.skymocha.net](https://www.skymocha.net)\n* [Twitter.com/skymochi64](https://www.twitter.com/skymochi64)\n\nI periodically update this website through a [script](https://github.com/SkyMocha/skymocha.github.io/blob/main/update.py).\n\n"

os.chdir (root_path)

index = open ('README.md', 'w')

index_txt = f"{info_text}## Courses\n\n"

for c in courses:

    print (c)

    index_txt += f'* [{c.upper()}]({c}) \n'

    _class = open (f'{c}.md', 'w')

    _class_txt = f'{info_text}## {c} Class Notes & Homework \n'

    for p in paths[c]:

        print (p)

        _class_txt += f'* [{p.upper()}]({p}) \n'
        
        os.system (f'git add "{p}"')
    
    _class_txt += f'\n\nLast updated {day} using a [static site generation script](https://github.com/SkyMocha/skymocha.github.io/blob/main/update.py)'

    _class.write(_class_txt)

    _class.close()


    os.system (f'git add "{c}.md"')

index_txt += f'\n\nLast updated {day} using a [static site generation script](https://github.com/SkyMocha/skymocha.github.io/blob/main/update.py)'

index.write (index_txt)
index.close()

os.system (f'git add README.md')

os.system (f'git commit -m "UPDATE: {day}"')
os.system (f'git push')