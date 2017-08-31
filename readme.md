# Git cloners
Clone all the repositories you have access to in Github and Gitlab (under dev)

# Installation
```
git clone https://github.com/kenichi-shibata/github_cloners
cd github_cloners
pip install .
```
# Usage
Clone everything
`cloners <personal-token> `


Clone user repos with forks 
`cloners <personal-token> --root-name <user-name>`


Clone user repos without forks
`cloners <personal-token> --root-name <user-name> --exclude-forks`


Clone organization repos with Forks
`cloners <personal-token> --root-name <org-name>`


Clone organization repos without Forks
`cloners <personal-token> --root-name <org-name> --exclude-forks `

To specifiy gitlab or github
`cloneres <personal-token> --type <gitlab|github>

## Delete the cloned repos
`cloners <personal-token> <arguments same as usage> --clean`

# Where?
By default all repos cloned and cleaned will be in the same directory where you cloned this repo

# TODO
* [x] --destination parameter
* [ ] add to PyPI to be able to do pip install pythonpackage

