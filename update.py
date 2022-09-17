import os
import datetime

print('updating')

day = str(datetime.datetime.now())[:10]

root_path = os.getcwd()  # gets current dir

os.chdir(os.path.join(root_path, '..'))  # goes to parent sub_dir (reed)

curr_path = os.getcwd()

paths = {}
courses = []


def addPDF(course, folder, week, _file):

    _path = os.path.join(curr_path, folder, week, _file)

    _out = os.path.join(root_path, folder)

    if (not os.path.isdir(_out)):

        os.system(f"mkdir '{_out}'")

    cmd = f"cp '{_path}' '{_out}/{week}.pdf'"

    # if (not os.path.isfile (f"'{_out}/{week}.pdf'")):

    os.system(cmd)

    paths[course].append(f'{course}/{week}.pdf')

    if (course not in courses):
        courses.append(course)

# updates all pdfs within a course


def updatePDF(course):

    paths[course] = []

    for folder in os.listdir(curr_path):

        if (folder == course):

            for week in os.listdir(os.path.join(curr_path, folder)):

                # Make sure it starts with a W or week
                # to not upload a folder (IE. homework) put a _ before it
                # so while being worked on Week1Proof would be _Week1Proof
                if (week[0:1] != 'W'):
                    continue

                for _file in os.listdir(os.path.join(curr_path, folder, week)):

                    if (_file[-3:] == 'ynb'):

                        _p = os.path.join(curr_path, folder, week)

                        os.system(
                            f'jupyter nbconvert --to PDF "{_p}/{week}.ipynb"')

                    if (_file[-3:] == 'pdf'):

                        addPDF(course, folder, week, _file)


updatePDF('Math 111')
# updatePDF('csci 122')
# updatePDF('Soc 211')
# updatePDF('Hum 110')

print(paths)

header_text = "\n* [Index](/)\n* [Publications](/publications)\n* [Reading](/reading)\n* [Resume](/resume.pdf)\n* [Twitter](https://www.twitter.com/skymochi64)\n\n"
info_text = "## Hello!\nI'm [Skye Kychenthal](https://www.skymocha.net). The purposes of this website are:\n* To facilitate an easier sharing of my class notes & getting in an open-source mindset.\n* To upload publications. \n* To upload static files IE. [publications](/publications) & [resume.pdf](/resume.pdf).\n\n"
notes_text = '\n## Notes\nAll courses taken are at [Reed College](https://www.reed.edu). The most up-to-date course catalog can be found [here](https://www.reed.edu/catalog/). As all notes & work done here are written by Skye Kychenthal, they should NOT be submitted as your own original work. This is called plagarism.\n\n'

os.chdir(root_path)

index = open('README.md', 'w')

index_txt = f"{header_text}{info_text}## Courses\n\n"

for c in courses:

    print(c)

    index_txt += f'* [{c.upper()}]({c}) \n'

    _class = open(f'{c}.md', 'w')

    _class_txt = f'{header_text}## {c.upper()} Class Notes & Homework \n'

    for p in paths[c]:

        print(p)

        _p_split = p.split('/')

        _class_txt += f'* [{_p_split[0].upper()} / {_p_split[1]}]({p})\n'

        os.system(f'git add "{p}"')

    _class_txt += notes_text

    _class_txt += f'\n\nLast updated {day} using a [static site generation script](https://github.com/SkyMocha/skymocha.github.io/blob/main/update.py)'

    _class.write(_class_txt)

    _class.close()

    os.system(f'git add "{c}.md"')

index_txt += notes_text

index_txt += f'\n\nLast updated {day} using a [static site generation script](https://github.com/SkyMocha/skymocha.github.io/blob/main/update.py)'

index.write(index_txt)
index.close()

os.system(f'git add README.md')

os.system(f'git commit -m "UPDATE: {day}"')
os.system(f'git push')
