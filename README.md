# pos-app-python

```bash
pyenv local 3.10.3
python -m venv venv 
source venv/bin/activate
python app.py
```


generate app .exe
```bash
pyinstaller --onefile --windowed --add-data "views/home_view.ui:views" app.py
```