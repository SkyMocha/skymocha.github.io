import os
import datetime 

print ('updating')

day = str(datetime.datetime.now())[:10]

root_path = os.getcwd() # gets current dir

os.chdir (os.path.join(root_path, '..')) # goes to parent sub_dir (reed)

curr_path = os.getcwd()

paths = {}
courses = []

# updates all pdfs within a course
def updatePDF (course):

    paths[course] = []

    for folder in os.listdir  (curr_path):

        if (folder == course):

            for week in os.listdir (os.path.join (curr_path, folder)):

                for _file in os.listdir( os.path.join (curr_path, folder, week ) ):

                    if (_file[-3:] == 'pdf'):

                        _path = os.path.join ( curr_path, folder, week, _file )

                        _out = os.path.join ( root_path , folder )

                        if (not os.path.isdir (_out)):
                            
                            os.system (f"mkdir '{_out}'")

                        cmd = f"cp '{_path}' '{_out}/{week}.pdf'"

                        if (not os.path.isfile (f"'{_out}/{week}.pdf'")):

                            os.system (cmd)
                        
                        paths[course].append(f'{course}/{week}.pdf')
                        courses.append (course)
                        
updatePDF('Math 111')

print (paths)

os.chdir (root_path)

index = open ('README.md', 'w')

index_txt = "## Courses\n"

for c in courses:

    index_txt += f'* [{c}]({c}) \n'

    _class = open (f'{c}.md', 'w')

    _class_txt = f'## {c} Class Notes & Homework \n'

    for p in paths[c]:

        _class_txt += f'* [p]({p}) \n'
        
        os.system (f'git add "{p}"')
    
    _class_txt += f'{day}'

    _class.write(_class_txt)

    _class.close()


    os.system (f'git add "{c}.md"')

index_txt += f'\nLast updated {day}'

index.write (index_txt)
index.close()

os.system (f'git add README.md')

os.system (f'git commit -m "UPDATE: {day}"')
os.system (f'git push')