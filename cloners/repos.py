from .github import GHRepos

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
  p.add_argument('--dry-run', '-y', action='store_true', help='check the repositories to be cloned')
  p.add_argument('--dest', '-d', default=None, help='where the repositories will be cloned')
  p.add_argument('--type', '-t', default='github-repo' ,help='Github or Gitlab Repos')
  args = p.parse_args()
  
  if args.type == 'github-repo' or 'github-gist':
    r = GHRepos(args.token)
  elif args.type == 'gitlab-snippet' or args.type == 'gitlab-repo': 
    raise NotImplemented
  else:
    print('only 4 types are supported gitlab-repo|gitlab-snippet|github-repo|github-gist')
    raise ValueError('Wrong Type')

  kwargs = {}
  if args.root_name:
    kwargs.update({'parent': args.root_name})
  if args.exclude_forks:
    kwargs.update({'excludeForks': args.exclude_forks})
  if args.verbose:
    print('using https://api.github.com with credentials {}'.format(args.token))
    print('Repos {}'.format(r.get_name()))
    kwargs.update({'verbose': args.verbose})
    print_kwargs(**kwargs)
  
  if args.type == 'github-repo' or args.type == 'gitlab-repo':
    repos = r.get_repo_dict(**kwargs)
    if args.dry_run and not args.clean:
      print('fake cloning')
      r.clone_repos(repos, args.dest, dry_run=True)
    elif args.dry_run and args.clean:
      print('fake cleaning')
      r.clean_all(repos, args.dest, dry_run=True)
    elif not args.dry_run and args.clean:
      print('cleaning')
      r.clean_all(repos, args.dest)
    else:
      print('cloning ')
      r.clone_repos(repos, args.dest)

  elif args.type == 'gitlab-snippet' or args.type == 'github-gist':
    print ('snippets or gist')
    r.get_gists()

