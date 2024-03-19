import pandas
from sys import getdefaultencoding
t = r'\\gold585.int\uk\Общее хранилище файлов\Служба аналитики\МЮР\tg_tn\.xlsx'.encode()
t1  = t.decode('utf-8')
p = pandas.read_excel(t1)
print(p)
