# Carme
The **C**ontainerized **A**nalytics **R**untime and **M**anagement **E**ngine

## Developers
Install `python3` and `pip` using the recommended method for your platform.

Then run the following commands in a terminal:
```
python3 -m venv carme-env
cd carme-env
source bin/activate
git clone https://github.com/carmelabs/carme.git
cd carme
pip install -r requirements.txt
```

### Installing CLI in Development Mode
`pip install -e src`

### Running Tests
`python src/setup.py test`
