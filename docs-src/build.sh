make html
rm -rf ../docs
rm -rf ../doctrees
mv ../html ../docs 
git add ../docs/*
git commit -m "Built documentation"
git push
