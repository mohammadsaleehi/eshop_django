# Eshop Django Project

Hello in this is first project me.im happy

---

## How to tun

If You're On A Windows Machine , Make Environment Ready By Following Steps Below:

1. Install `python3`, `pip`, `virtualenv`
2. Clone the project using:  `git clone https://github.com/MohammadSaleehi/Eshop_django.git`.
3. Make Environment Ready Like This:

``` Command Prompt
cd eshop_project
python -m venv venv # Create Virtualenv with python.exe
venv\Scripts\activate
pip install -r requirements.txt
copy .env-sample .env
# create setting to file .env
python manage.py migrate # Create Database Tables
```

4. Run `Eshop djanog` using `python manage.py runserver`
5. Go to [http://localhost:8000](http://localhost:8000) to see your eshop django version.
