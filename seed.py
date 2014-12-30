#!/usr/bin/python2
import gitlab
import argparse


class Seed(object):
    g = gitlab.Gitlab("http://185.63.188.217", "mAXctpECCiNGZ3ELJfS6")
    default_pass = "Passw0rd"
    username_base = "user_%d"
    
    def seed_users(self, cnt_from, cnt_to):
        for i in range(cnt_from, cnt_to):
            self.g.createuser(self.username_base % i, self.username_base % i, self.default_pass, self.username_base % i
                              + "@somemail.com")

    def update_users(self, user_id=None, project_id=None):
        page = 1
        if user_id:
            # todo!
            pass
            return
        while True:
            users = self.g.getusers(page=page, per_page=100)
            if not users:
                break
            page += 1

            for user in users:
                self.g.edituser(user['id'])
                if project_id:
                    print('Adding user to project')
                    self.g.addprojectmember(project_id, user['id'], 'master')

    def get_projects(self):
        page = 1
        while True:                        
            projects = self.g.getprojects(page=page, per_page=100)
            if not projects:
                break
            page += 1
            for project in projects:
                print('%s: %d' % (project['name'], project['id']))
                print('\n')

    def delete_user(self, user_id):
        self.g.deleteuser(user_id)

    def get_users(self):
        page = 1
        count = 0
        while True:
            users = self.g.getusers(page=page, per_page=100)
            if not users:
                break
            page += 1
            for user in users:
                print('%s - %d'%(user['name'], user['id']))
                count += 1
        print('Total %d' % count)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--project-id")
    parser.add_argument("--nfrom")
    parser.add_argument("--nto")
    parser.add_argument("--user-id")
    parser.add_argument("--project-fullname")
    args = parser.parse_args()
    seed = Seed()
    if args.action == "create":
        seed.seed_users(args.nfrom, args.nto)
    elif args.action == "projects":
        seed.get_projects()
    elif args.action == "users":
        seed.get_users()
    elif args.action == "delete":
        seed.delete_user(args.userid)
    elif args.action == "addmember":
        seed.update_users(args.user_id, args.project_id)
    else:
        print("Unknown action. Nothing to do.")

if __name__ == '__main__':
    main()