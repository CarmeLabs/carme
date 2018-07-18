conda create --name carme-env
source activate carme-env
conda install -c anaconda pip
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/requirements.txt
pip uninstall carme --yes
pip install -r requirements.txt
pip install git+https://github.com/CarmeLabs/carme.git
rm requirements.txt
