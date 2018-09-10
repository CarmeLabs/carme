python3 -m venv carme-env
source carme-env/bin/activate
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/activate.sh
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/requirements.txt
pip3 uninstall carme --yes
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install git+https://github.com/CarmeLabs/carme.git
rm requirements.txt
