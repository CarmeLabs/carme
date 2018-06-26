pip install -r requirements.txt
make html
rm -rf ../docs
rm -rf ../doctrees
mv ../html ../docs
git add ../docs/*
git add ../docs-src/*
git commit -m "Built documentation"
git push
