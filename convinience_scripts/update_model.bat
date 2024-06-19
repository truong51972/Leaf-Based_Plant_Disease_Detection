git add .
git commit -m 'commit to update model from truong-img-classifier'
git switch truong-img-classifier
git pull
git switch main
git checkout truong-img-classifier -- model
git add .
git commit -m 'update model successfully!'