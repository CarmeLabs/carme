#Generate az-server packages
wget -O file.tmp https://raw.githubusercontent.com/CarmeLabs/packages/master/az-server/docs/rst/az-server.rst && sed -e '/From the notebook included in the package:/r file.tmp' -e '$G' ./templates/az-server.template > az-server.rst && rm file.tmp
wget -O file.tmp https://raw.githubusercontent.com/CarmeLabs/packages/master/az-cluster/docs/rst/az-cluster.rst && sed -e '/From the notebook included in the package:/r file.tmp' -e '$G' ./templates/az-cluster.template > az-cluster.rst && rm file.tmp
wget -O file.tmp https://raw.githubusercontent.com/CarmeLabs/packages/master/gcp-cluster/docs/rst/gcp-cluster.rst && sed -e '/From the notebook included in the package:/r file.tmp' -e '$G' ./templates/gcp-cluster.template > gcp-cluster.rst && rm file.tmp
wget -O file.tmp https://raw.githubusercontent.com/CarmeLabs/packages/master/jupyterhub/docs/rst/jupyterhub.rst && sed -e '/From the notebook included in the package:/r file.tmp' -e '$G' ./templates/jupyterhub.template > jupyterhub.rst && rm file.tmp
#Change the ! to > for clear command line interactions.
sed -i '' s/\!//g *.rst
sed -i '' s/\$dryrun//g *.rst
sed -i '' s/\$yes//g *.rst
