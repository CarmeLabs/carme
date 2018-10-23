wget https://raw.githubusercontent.com/CarmeLabs/carme/master/requirements.txt
sudo pip3 uninstall carme --yes
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
sudo pip3 install git+https://github.com/CarmeLabs/carme.git
rm requirements.txt
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
