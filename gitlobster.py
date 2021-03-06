#!/usr/bin/python2
from subprocess import call
import os
import random
import argparse


def get_branch_name(cnt):
    return 'b_%d' % cnt


def get_file_name(cnt):
    return 'f_%d.txt' % cnt


def create_file(path, size):
    with open(path, 'w') as f:
        f.write(get_random_text(size))


def get_random_text(size):
    # return ''.join(random.choice(string.hexdigits) for i in range(size))
    size *= 1024  # Convert to Kb
    return '%030x' % random.randrange(16**size) + '\n'


def new_branch(branch_name):
    call(['git', 'checkout', '-b', branch_name])


def commit():
    call(['git', 'commit', '.', '-m', 'Automaticaly commited changes'])


def add():
    call(['git', 'add', '.'])


def init(base_dir):
    if not os.path.exists(base_dir+'.git'):
        call(['git', 'init'])
        with open('initial_readme.md', 'w') as f:
            f.write('Process started\n')
        add()
        commit()
        return False
    return True


def checkout_master():
    call(['git', 'checkout', 'master'])


def push_all(pool_first):
    if pool_first:
        call(['git', 'pull'])
    call(['git', 'push', '--all', 'origin'])


def push_current(branch_name):
    call(['git', 'push', '-u', 'origin', branch_name])
    call(['git', 'push'])


def add_origin(remote_origin):
    call(['git', 'remote', 'add', 'origin', remote_origin])


def checkout(branch):
    call(['git', 'checkout', branch])


class GitLobster(object):
    def __init__(self, working_dir, size, number_of_files, branch_from, branch_to, remote_origin):
        self.size = size
        self.number_of_files = number_of_files
        self.base_path = working_dir if working_dir.endswith('/') else working_dir + '/'
        os.chdir(self.base_path)
        self.branch_from = branch_from
        self.branch_to = branch_to
        self.repo_exists = init(self.base_path)
        if remote_origin:
            add_origin(remote_origin)

    def _create_brunch_folder(self, branch_counter):
        os.makedirs(self.base_path + get_branch_name(branch_counter))

    def do_work(self, push_after=None, push=None):
        push_cnt = 0
        for branch_num in range(self.branch_from, self.branch_to + 1):
            branch = get_branch_name(branch_num)
            new_branch(branch)
            for file_num in range(0, self.number_of_files):
                create_file(self.base_path + get_branch_name(branch_num)+'_' + get_file_name(file_num), self.size)
            add()
            commit()
            push_cnt += 1
            if push and push_cnt == 40:
                push_all(self.repo_exists)
                push_cnt = 0
            checkout_master()
        push_all(self.repo_exists)


def main():
    parser = argparse.ArgumentParser(description='Tiny util to flood git repositories')
    parser.add_argument("directory", help='full path to git project, default /home/coon/gitlobster/')
    parser.add_argument("--branch-from", "-f", required=True, type=int, help='-f branch counter range start')
    parser.add_argument("--branch-to", "-t", required=True, type=int, help='-t branch counter range stop')
    parser.add_argument("--file-amount", "-a", required=True, type=int, help='-a Amount of files in each branch')
    parser.add_argument("--size", "-s", required=True, type=int, help='-s File Size, kb')
    parser.add_argument("--push", "-p", required=False,  action="store_true", default=False,
                        help='<Optional> -p push every branch after creation')
    parser.add_argument("--push-after", required=False,  action="store_false", default=False,
                        help='<Optional> push all branches after repo being flooded')
    parser.add_argument("--origin", "-o", required=False,
                        help='<Optional> -o remote origin to to push into \n E.g.: '
                        'http://apinaev.example.com/root/gitlobstertests.git')

    args = parser.parse_args()
    lobster = GitLobster(args.directory, args.size, args.file_amount, args.branch_from, args.branch_to, args.origin)
    lobster.do_work(args.push_after, args.push)

if __name__ == '__main__':
    main()