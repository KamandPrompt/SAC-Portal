# SAC-Portal
SAC Portal for IIT Mandi

Hello fellow contributors! To get started with the project , go ahead and fork the repository . You should see the URL change to
```
https://github.com/Your Username/SAC-Portal
```

Cloning This Repository
--- 
To clone this repository , copy the URL. Open your terminal or git bash and enter the following aftering replacing your username. 
```
git clone https://github.com/Your Username/SAC-Portal.git
```

Staying Updated
--- 
Add the following lines to stay updated with the new commits being done in the master branch of the home repository. New commits may have happened to the home repository after you have cloned the repository.
```
git remote add upstream https://github.com/KamandPrompt/SAC-Portal.git
```

Type the following to update your local repository
```
git fetch upstream
git rebase upstream/master
```

Contributing
---

### Pushing files to your local repository
It is always recommended to work from different branches and give pull requests from the there . 
So create a new branch in your local machine using
```
git checkout -b <Branch-Name>
```

Now you should see a new folder called SAC-Portal being created in your home folder .
Create or make changes to files existing in the folder. After you are done , upload the files to your git repository.

Add files to this branch using 
```
git add <file-name>
git commit -m "Enter comments"
```

Commit the changes to your repository , The following command holds good if the new branch wasn't already made in your github page .
```
git push --set-upstream origin new_branch
```

For later commits just
`git push` will work

Then from your forked repository on github , make a pull request to the KamandPrompt page . 



