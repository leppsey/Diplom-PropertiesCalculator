# Kак запускать????
##### жоска клоним проект
```
git clone https://github.com/leppsey/Diplom-PropertiesCalculator.git
cd Diplom-PropertiesCalculator/
```
##### устанавлваем питон эвайронмент и библиотеки
```
sudo apt install python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
##### самое сложное, нада закоммитить пару строк в библиотеке scipy
```
nano .venv/lib/python3.10/site-packages/scipy/interpolate/_bsplines.py
```
##### и коммитим эти строки:
1384 строка
```
if np.any(x[1:] == x[:-1]):
    raise ValueError("Expect x to not have duplicates")
```
1497 строка
```
if info > 0:
    raise LinAlgError("Collocation matrix is singular.")
    elif info < 0:
    raise ValueError('illegal value in %d-th argument of internal gbsv' % -info)
```
##### ну и непосредственно запуск
```
python manage.py runserver
```
