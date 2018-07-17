git clone https://github.com/CarmeLabs/carme
python3 -m venv carme-env
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/activate.sh
source carme-env/bin/activate
cd carme
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -e .
cd ..
