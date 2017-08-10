from github import Github
from . import access
import subprocess
import os
# First create a Github instance:
class Repos(): 
	def __init__(self, token):
		self.g = Github(token)
	#
	# Then play with your Github objects:
	# http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html

	def get_dir(self):
		return os.path.dirname(os.path.realpath(__file__))

	def get_username(self):
		''' gets own username uses it'''
		return self.g.get_user()

	def get_orgs(self):
		''' Creates a iteratable org list try vars(get_orgs()) to get full into  for org in get_orgs: org.name'''
		return self.g.get_user().get_orgs()

	def get_name(self):
		return self.get_username().login

	def get_repo_dict(self, excludeForks=False, parent=None):
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
		list_all = list(map(lambda x: (x.ssh_url, x.full_name.split('/')[1], x.full_name.split('/')[0], x.fork), repos))
		dictionary = { key: { 'name': name, 'count': idx, 'fork': fork, 'parent': parent } for idx, (key, name, parent, fork) in enumerate(list_all) }
		if excludeForks:
			dictionary = dict({ k: { 'name': v['name'], 'count':v['count'], 'fork': v['fork'], 'parent': v['parent'] } for k, v in dictionary.items() if (v['fork'] == False) })
		if parent:
			dictionary = dict({ k: { 'name': v['name'], 'count':v['count'], 'fork': v['fork'], 'parent': v['parent'] } for k, v in dictionary.items() if (v['parent'] == parent) })
		return dictionary

	def clone_repos(self, repos):
		''' clones all specified repos 
		Parameters
		-----------
		repos : dict
		'''
		for repo, params in repos.items():
			parent = params['parent']
			name = params['name']
			directory = os.path.join(self.get_dir(), parent, name)
			os.makedirs(directory, exist_ok=True)
			try:
				print('cloning {} to {}'.format(repo, directory))
				subprocess.check_call(['git', 'clone', repo, directory])
			except:
				continue

	def clean_all(self, repos):
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
			directory = os.path.join(self.get_dir(), parent, '')
			del_dir.append(directory)
		del_dir = list(set(del_dir))	
		for directory in del_dir:
			if(os.path.exists(directory)):
				print('deleting {}'.format(directory))
				shutil.rmtree(directory, ignore_errors=True)

def print_kwargs(**kwargs):
	print(','.join(['{} = {}'.format(k, v) for k,v in kwargs.items()]))

def main():
	import argparse
	p = argparse.ArgumentParser()
	p.add_argument('token', help='Your github personal token')
	p.add_argument('--root-name', help='clone only repos with the root_name (i.e. root_name is kenichi-shibata in https://github.com/kenichi-shibata/test')
	p.add_argument('--clean', action='store_true', help='remove all directories cloned with cloners')
	p.add_argument('--exclude-forks', action='store_true',help='only clones sources')
	p.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
	p.add_argument('--dry-run', '-d', action='store_true', help='check the repositories to be cloned')
	args = p.parse_args()
	r = Repos(args.token)

	kwargs = {}
	if args.root_name:
		kwargs.update({'parent': args.root_name})
	if args.exclude_forks:
		kwargs.update({'excludeForks': args.exclude_forks})
	if args.verbose:
		print('using https://api.github.com with credentials {}'.format(args.token))
		print('Cloning as {}'.format(r.get_name()))
		print_kwargs(**kwargs)
	if args.dry_run:
		print('repos to be clones {}'.format(r.get_repo_dict(**kwargs)))
	elif args.clean:
		raise NotImplemented
	else:
		repos = r.get_repo_dict(**kwargs)
		print('cloning ')
		r.clone_repos(repos)