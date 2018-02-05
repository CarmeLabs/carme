# Carme
The **C**ontainerized **A**nalytics **R**untime and **M**anagement **E**ngine

## Developers
Install `python3` and `pip` using the recommended method for your platform.

Then run the following commands in a terminal:
```
python3 -m venv carme-env
cd carme-env
source bin/activate
pip install --upgrade pip
git clone https://github.com/carmelabs/carme.git
cd carme
pip install -r requirements.txt
```

### Installing CLI in Development Mode
```
cd ..  # (should be in carme-env)
pip install -e carme
```

### Running Tests
`python carme/setup.py test`
