from core.model import TeaDeer
from core.packing import sort
td = TeaDeer() # Общий класс
td.load('models/best_seg.pt') # Подгрузка модели из файла
results = td.detect('media')
for result in results:
    td.plot(result)