pip install -r requirements.txt
cd ./source/commands
source generate.sh
cd ../../
cd ./source/packages
source generate.sh
cd ../../
make html
rm -rf ../docs
rm -rf ../doctrees
mv ../html ../docs
git add ../docs/*
git add ../docs-src/*
git commit -m "Built documentation"
git push
