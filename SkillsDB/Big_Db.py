'''
This code is data base allow ti the user to edit his data
'''
import sqlite3
import json

db=sqlite3.connect('BigDB.db')
cr=db.cursor()
cr.execute('CREATE TABLE IF NOT EXISTS skills(id INT, name TEXT, skill TEXT)')

values=[(1, 'Joudy', json.dumps({'python': 80, 'html':100, 'css':50})),
        (2, 'Hamza', json.dumps({'html': 100, 'js':80, 'css':80})),
        (3, 'Abd', json.dumps({'python': 90, 'database':100, 'AI':90}))]

cr.executemany('INSERT INTO skills(id, name, skill) VALUES (?, ?, ?)', values)

def exists():
    '''
    this method to ensur that user is in data base
    '''
    cr.execute(f'SELECT 1 FROM skills WHERE id={uid}')
    if cr.fetchone() is None:
        raise ValueError

def show_skills():
    '''
    this mathod to show user's skill
    '''
    cr.execute(f'SELECT skill FROM skills WHERE ID={uid}')
    row=cr.fetchone()
    skill_dict=json.loads(row[0])
    print(f'you have {len(skill_dict)} skills')
    if len(skill_dict)>0:
        for sk, prog in skill_dict.items():
            print(sk,' => ',prog)

def add_skill():
    '''
    this mathod to add one skill
    '''
    sk=input('enter skill that you need add to your data: ')
    prog=int(input('the progress is: '))
    cr.execute(f'SELECT skill FROM skills WHERE id={uid}')
    row=cr.fetchone()
    skill_dict=json.loads(row[0])
    skill_dict[sk]=prog
    cr.execute('UPDATE skills SET skill =? WHERE id=?', (json.dumps(skill_dict), uid))
    print('your skill is added.!')

def delete_skill():
    '''
    this mathod to delete one skill
    '''
    sk=input('enter the skill that you want delete it: ')
    cr.execute(f'SELECT skill FROM skills WHERE id={uid}')
    row=cr.fetchone()
    skill_dict=json.loads(row[0])
    del skill_dict[sk]
    if sk in skill_dict:
        cr.execute('UPDATE skills SET skill =? WHERE id=?', (json.dumps(skill_dict), uid))
        print('your skill is deleted.!')
    else:
        raise KeyError

def update_skill():
    '''
    this mathod to update progress's skill
    '''
    sk=input('enter the skill that you want edit its progress: ')
    cr.execute(f'SELECT skill FROM skills WHERE id ={uid}')
    row=cr.fetchone()
    skill_dict=json.loads(row[0])
    if sk in skill_dict:
        prog=int(input('enter new progress '))
        skill_dict[sk]=prog
        cr.execute('UPDATE skills SET skill=? WHERE id=?',(json.dumps(skill_dict), uid))
        print('your skill is updated.!')
    else: raise KeyError

try:
    uid=int(input('inter your id: '))
    exists()

    MessagInput='''
What do you want to do"
"s" Show your Data.
"a" Add skill.
"d" Delete skill.
"u" Ubdate your skills.
"q" Quit program.
your choose is: 
'''
    choose_input=input(MessagInput).strip().lower()
    choice=["s", "a", "d", "u", "q"]
    if choose_input in choice:
        if choose_input=='s':
            show_skills()
        elif choose_input=='a':
            add_skill()
        elif choose_input=='d':
            delete_skill()
        elif choose_input=='u':
            update_skill()
        else:
            print('program is ended.')
    else: raise

except sqlite3.Error as e:
    print(f'There is error as {e}')
except ValueError:
    print('your id not in data base')
except KeyError:
    print('the skill alredy is not in your skills.')
except:
    print('choice must be from input message.!')

finally:
    db.commit()
    db.close()
    print('data base is closed.')
