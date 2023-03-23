# GUI

## Installation

Make sure python is installed if it isn't already. 

1. Install QT5: https://www.qt.io/download-qt-installer

2. Pull the repository if you haven't already: 

```bash
git clone https://github.com/ZenghaoWang/hyperloop-power-system.git hyperloop && cd hyperloop/gui
```
3. Setup and activate venv: 

```bash
python -m pip venv venv
```
4. Install python dependencies:
  
```bash
pip install -U -r requirements.txt
```

5. At the top of app.py, change the values of CANABLE_COM_PORT and ARDUINO_COM_PORT. 

## Running the Program

1. Navigate to the ``/gui`` directory.
2. Make sure your virtual environment is activated:

```bash
.\venv\Scripts\activate
```

3. Run the app.

```bash
python app.py
```


