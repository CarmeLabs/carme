git clone https://github.com/CarmeLabs/carme
python3 -m venv carme-env
source carme-env/bin/activate
cd carme
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -e .
