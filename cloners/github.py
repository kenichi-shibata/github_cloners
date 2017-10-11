from github import Github
import subprocess
import os
# First create a Github instance:
class GHRepos(): 
  def __init__(self, token):
    self.token = token 
    self.g = Github(token)
  #  api docs http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html

  def get_dir(self, path=None):
    path = path or os.getcwd()
    return path

  def get_username(self):
    ''' gets own username uses it'''
    return self.g.get_user()

  def get_orgs(self):
    ''' Creates a iteratable org list try vars(get_orgs()) to get full into  for org in get_orgs: org.name'''
    return self.g.get_user().get_orgs()

  def get_name(self):
    return self.get_username().login

  def get_repo_dict(self, verbose=False, excludeForks=False, parent=None):
    ''' creates a dictionary of repository to be used on cleaning, cloning and updating. Repos are all repositories which the user has write access
    Parameters
    ----------
    excludeForks : bool
      Whether to include forked repos in the list
    parent : str
      To filter out only specific parent, parent means either organization name or username 
      for example in the repo https://github.com/kenichi-shibata/route53-ssl the parent is kenichi-shibata 
      or on the repo  https://github.com/aws/aws-cli root name is aws
    Returns
    -----------
    dict
      dict(git_url: {count : int, fork: bool, parent: str})
    '''

    repos = self.get_username().get_repos()
    list_all = list(map(lambda x: ('https://{}:{}@{}'.format(self.get_name(), self.token, x.clone_url.split('https://')[1]) , x.full_name.split('/')[1], x.full_name.split('/')[0], x.fork), repos))
    dictionary = { key: { 'name': name, 'count': idx, 'fork': fork, 'parent': parent } for idx, (key, name, parent, fork) in enumerate(list_all) }
    if excludeForks:
      dictionary = dict({ k: { 'name': v['name'], 'count':v['count'], 'fork': v['fork'], 'parent': v['parent'] } for k, v in dictionary.items() if (v['fork'] == False) })
    if parent:
      dictionary = dict({ k: { 'name': v['name'], 'count':v['count'], 'fork': v['fork'], 'parent': v['parent'] } for k, v in dictionary.items() if (v['parent'] == parent) })
    if verbose:
      from pprint import pprint
      pprint(dictionary)
    return dictionary

  def clone_repos(self, repos, dest=None, dry_run=False):
    ''' clones all specified repos 
    Parameters
    -----------
    repos : dict
    '''
    for repo, params in repos.items():
      parent = params['parent']
      name = params['name']
      directory = os.path.join(self.get_dir(dest), parent, name)
      if not dry_run:
        os.makedirs(directory, exist_ok=True)
      try:
        print('cloning {} to {}'.format(repo, directory))
        if not dry_run:
          subprocess.check_call
          subprocess.check_call(['git', 'clone', repo, directory])
      except:
        continue

  def get_gists(self):
    gists = self.get_username().get_gists()
    gists_url = list(map(lambda x: x.git_pull_url, gists))
    os.makedirs('tmp', exist_ok=True)
    for gist in gists_url:
      gist = 'https://{}:{}@{}'.format(self.get_name(), self.token, gist.split('https://')[1])
      subprocess.check_output(['git', 'clone', gist],cwd='tmp')

  def clean_all(self, repos, dest, dry_run=False):
    ''' cleans up all the cloned repos
    Parameters
    ----------
    repos : dict
    '''
    import shutil
    del_dir = []
    for _, params in repos.items():
      parent = params['parent']
      name = params['name']
      directory = os.path.join(self.get_dir(dest), parent, '')
      del_dir.append(directory)
    del_dir = list(set(del_dir))  
    for directory in del_dir:
      if(os.path.exists(directory)):
        print('deleting {}'.format(directory))
        if not dry_run:
          shutil.rmtree(directory, ignore_errors=True)
