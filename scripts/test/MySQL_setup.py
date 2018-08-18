# describe accounts_user;
# describe auth_group;
# describe auth_group_permissions;
# describe auth_permission;
# describe auth_user;
# describe auth_user_groups;
# describe auth_user_user_permissions;
# describe django_admin_log;
# describe django_content_type;
# describe django_migrations;
# describe results_usertotalresult;
# describe results_userweekresult;
#
# drop table accounts_user;
# drop table auth_group;
# drop table auth_group_permissions;
# drop table auth_permission;
# drop table auth_user;
# drop table auth_user_groups;
# drop table auth_user_user_permissions;
# drop table django_admin_log;
# drop table django_content_type;
# drop table django_migrations;
# drop table results_usertotalresult;
# drop table results_userweekresult;
#
#
#
# ALTER TABLE django_migrations CHANGE name name CHAR(20);
#
# delete from django_migrations;
#
#
#
# rm -rf accounts/migrations/
# rm -rf fixtures/migrations/
# rm -rf picks/migrations/
# rm -rf results/migrations/
# rm -rf playoff_teams/migrations/
#
# python manage.py migrate --fake
#
# python manage.py makemigrations accounts
# python manage.py makemigrations fixtures
# python manage.py makemigrations picks
# python manage.py makemigrations results
# python manage.py makemigrations playoff_teams
#
# python manage.py migrate --fake-initial
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# .
