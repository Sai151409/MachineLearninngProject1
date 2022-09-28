# MachineLearningProject1
This is my first machine learning project


Required Softwares for Machine Learning Project

1. [Github Account] : (https://github.com)
2. [Heroku Account] : (https://dashboard.heroku.com/login)
3. [VS Code IDE] : (https://code.visualstudio.com/download)
4. [Git Cli] : (https://git-scm.com/downloads)

Creating Conda Environment
````
conda create -p venv python==3.7 -y 
`````

activate conda env
`````
conda activate venv/
`````

OR

`````
conda activate venv
`````

intsall requirements file in project

`````
pip install -r requirements.txt
`````

To add the file in git
`````
git add .
``````

OR

`````
git add <file_name>
`````

 Note : To ignore file or folder from git we can write name of file/folder in .gitignore file


To check the status of git 

`````
git status
`````

To check the versions in git 
`````
git log
`````

To create version/commit all changes by git

`````
git commit -m "message"
`````

To send the versions/changes to the git repo

`````
git push origin main
`````

To check remote url

`````
git remove -v
`````

To setup CI/CD pipline in heroku we need 3 information



Build Docker Image
`````
docker build -t <image name> : <tag name> .
`````

> Note : Image name for the docker file must be lowercase


To check the docker images

`````
docker images
`````

Run docker Image

``````
docker run -p 5000:5000 -e PORT=5000 8cc871cd9739
``````

To check the containers in docker

``````
docker ps
``````

To stop the docker container

```````
docker stop <container ID>
````````