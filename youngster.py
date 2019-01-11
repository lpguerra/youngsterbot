from youngster_lib import *

arq = open("C:\\Users\\User\\Documents\\Leonardo Guerra\\youngsterbot\\db\\text_db.txt", "w+")
arq.close()


reader = Reader()
writer = Writer()

cwd = os.getcwd()

logs = reader.extract_dir_logs(cwd+'/raw_data/')

for l in logs:
    log = l.split('\n')
    writer.record_battle(log, cwd + '/db/text_db.txt')
