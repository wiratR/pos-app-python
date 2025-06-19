# pos-app-python

```bash
pyenv local 3.10.3
python -m venv venv 
source venv/bin/activate
cp .env.sample .env
python app.py
```


generate app .exe
```bash
pyinstaller --onefile --windowed --add-data "resources/ui/home_view.ui:resources/ui" app.py
```

