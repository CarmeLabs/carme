make html
rm -rf ../docs
mv ../html ../docs 
git commit -m 'Built documentation' -- ../docs
git push
