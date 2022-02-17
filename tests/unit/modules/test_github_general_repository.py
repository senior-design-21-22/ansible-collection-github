from __future__ import (absolute_import, division, print_function)
from unittest import result
__metaclass__ = type

from ansible.module_utils import basic
from utils import ModuleTestCase, set_module_args, exit_json, AnsibleExitJson
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
import json
import collections
import unittest


def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo_name=dict(type='str', default=''),
        team_id=dict(type='int', default=0),
        private=dict(type='bool', default=False),
        has_issues=dict(type='bool', default=True),
        has_wiki=dict(type='bool', default=True),
        auto_init=dict(type='bool', default=False),
        has_downloads=dict(type='bool', default=False),
        has_projects=dict(type='bool', default=True),
        allow_squash_merge=dict(type='bool', default=True),
        allow_merge_commit=dict(type='bool', default=True),
        allow_rebase_merge=dict(type='bool', default=True),
        delete_branch_on_merge=dict(type='bool', default=False),
        description=dict(type='str', default=''),
        homepage=dict(type='str', default=''),
        license_template=dict(type='str', default=''),
        gitignore_template=dict(type='str', default=''),
        state=dict(type='str', default='present'),
    )

    valid_states = ["absent", "present"]

    valid_gitignore_templates = ['Actionscript',
                                 'Ada',
                                 'Agda',
                                 'Android',
                                 'AppEngine',
                                 'AppceleratorTitanium',
                                 'ArchLinuxPackages',
                                 'Autotools',
                                 'C++',
                                 'C',
                                 'CFWheels',
                                 'CMake',
                                 'CONTRIBUTING.md',
                                 'CUDA',
                                 'CakePHP',
                                 'ChefCookbook',
                                 'Clojure',
                                 'CodeIgniter',
                                 'CommonLisp',
                                 'Composer',
                                 'Concrete5',
                                 'Coq',
                                 'CraftCMS',
                                 'D',
                                 'DM',
                                 'Dart',
                                 'Delphi',
                                 'Drupal',
                                 'EPiServer',
                                 'Eagle',
                                 'Elisp',
                                 'Elixir',
                                 'Elm',
                                 'Erlang',
                                 'ExpressionEngine',
                                 'ExtJs',
                                 'Fancy',
                                 'Finale',
                                 'FlaxEngine',
                                 'ForceDotCom',
                                 'Fortran',
                                 'FuelPHP',
                                 'GWT',
                                 'Gcov',
                                 'GitBook',
                                 'Go',
                                 'Godot',
                                 'Gradle',
                                 'Grails',
                                 'Haskell',
                                 'IGORPro',
                                 'Idris',
                                 'JBoss',
                                 'JENKINS_HOME',
                                 'Java',
                                 'Jekyll',
                                 'Joomla',
                                 'Julia',
                                 'KiCad',
                                 'Kohana',
                                 'Kotlin',
                                 'LICENSE',
                                 'LabVIEW',
                                 'Laravel',
                                 'Leiningen',
                                 'LemonStand',
                                 'Lilypond',
                                 'Lithium',
                                 'Lua',
                                 'Magento',
                                 'Maven',
                                 'Mercury',
                                 'MetaProgrammingSystem',
                                 'Nanoc',
                                 'Nim',
                                 'Node',
                                 'OCaml',
                                 'Objective-C',
                                 'Opa',
                                 'OpenCart',
                                 'OracleForms',
                                 'Packer',
                                 'Perl',
                                 'Phalcon',
                                 'PlayFramework',
                                 'Plone',
                                 'Prestashop',
                                 'Processing',
                                 'PureScript',
                                 'Python',
                                 'Qooxdoo',
                                 'Qt',
                                 'R',
                                 'README.md',
                                 'ROS',
                                 'Rails',
                                 'Raku',
                                 'RhodesRhomobile',
                                 'Ruby',
                                 'Rust',
                                 'SCons',
                                 'Sass',
                                 'Scala',
                                 'Scheme',
                                 'Scrivener',
                                 'Sdcc',
                                 'SeamGen',
                                 'SketchUp',
                                 'Smalltalk',
                                 'Stella',
                                 'SugarCRM',
                                 'Swift',
                                 'Symfony',
                                 'SymphonyCMS',
                                 'TeX',
                                 "Terraform",
                                 'Textpattern',
                                 'TurboGears2',
                                 'TwinCAT3',
                                 'Typo3',
                                 'Unity',
                                 'UnrealEngine',
                                 'VVVV',
                                 'VisualStudio',
                                 'Waf',
                                 'WordPress',
                                 'Xojo',
                                 'Yeoman',
                                 'Yii',
                                 'ZendFramework',
                                 'Zephir']

    valid_licenses = ["afl-3.0",
                      "apache-2.0",
                      "artistic-2.0",
                      "bsl-1.0",
                      "bsd-2-clause",
                      "bsd-3-clause",
                      "bsd-3-clause-clear",
                      "cc",
                      "cc0-1.0",
                      "cc-by-4.0",
                      "cc-by-sa-4.0",
                      "wtfpl",
                      "ecl-2.0",
                      "epl-1.0",
                      "epl-2.0",
                      "eupl-1.1",
                      "agpl-3.0",
                      "gpl",
                      "gpl-2.0",
                      "gpl-3.0",
                      "lgpl",
                      "lgpl-2.1",
                      "lgpl-3.0",
                      "isc",
                      "lppl-1.3c",
                      "ms-pl",
                      "mit",
                      "mpl-2.0",
                      "osl-3.0",
                      "postgresql",
                      "ofl-1.1",
                      "ncsa",
                      "unlicense",
                      "zlib"]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.params['state'] not in valid_states:
        error_message = 'Invalid state: ' + module.params['state']
        return error_message, False

    if module.params['enterprise_url'] == '':
        g = module.params['token']
    else:
        g = module.params['token'] + module.params['enterprise_url']

    try:
        repo = module.params['repo_name']
        initial = {
            "name": module.params['repo_name'],
            "full_name": module.params['organization_name'] + '/' + module.params['repo_name'],
            "owner": 'test_login',
            "description": '',
            "private": False,
            "archived": False,
            "language": 'null',
            "url": 'test_url',
            "default_branch": 'master',
            "hooks_url": 'test_hook_url',
            "clone_url": 'test_clone_url',
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ''
        }
    except Exception as e:
        initial = {}

    test_output = initial.copy()
    if module.params['state'] == 'present':
        try:
            if module.params['license_template'] and module.params['license_template'] not in valid_licenses:
                error_message = 'Invalid license: ' + \
                    module.params['license_template']
                return error_message, False

            if module.params['gitignore_template'] and module.params['gitignore_template'] not in valid_gitignore_templates:
                error_message = 'Invalid gitignore template: ' + \
                    module.params['gitignore_template']
                return error_message, False

            if repo == 'test_present_repo':
                test_output['name'] = module.params['repo_name']
                test_output['description'] = module.params['description']
                test_output['homepage'] = module.params['homepage']
                test_output['private'] = module.params['private']
                test_output['has_issues'] = module.params['has_issues']
                test_output['has_projects'] = module.params['has_projects']
                test_output['has_wiki'] = module.params['has_wiki']
                test_output['has_downloads'] = module.params['has_downloads']
                test_output['allow_squash_merge'] = module.params['allow_squash_merge']
                test_output['allow_merge_commit'] = module.params['allow_merge_commit']
                test_output['allow_rebase_merge'] = module.params['allow_rebase_merge']
                test_output['delete_branch_on_merge'] = module.params['delete_branch_on_merge']

        except Exception as e:
            repo = 'created new repo'
            # g.get_organization(module.params['organization_name']).create_repo(
            #     module.params['repo_name'],
            #     module.params['description'],
            #     module.params['homepage'],
            #     module.params['private'],
            #     module.params['has_issues'],
            #     module.params['has_wiki'],
            #     module.params['has_downloads'],
            #     module.params['has_projects'],
            #     module.params['team_id'],
            #     module.params['auto_init'],
            #     module.params['license_template'],
            #     module.params['gitignore_template'],
            #     module.params['allow_squash_merge'],
            #     module.params['allow_merge_commit'],
            #     module.params['allow_rebase_merge'],
            #     module.params['delete_branch_on_merge']
            # )

    else:
        try:
            test_output = {}
        
        except Exception as e:
            ...

    try:
        output = test_output
    except Exception as e:
        output = {}

    return output, initial!=output

class TestGeneralRepositoryModule(unittest.TestCase):
    def test_return_initial_repo(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            "name": 'test_present_repo',
            "full_name": 'test_org_name/test_present_repo',
            "owner": 'test_login',
            "description": '',
            "private": False,
            "archived": False,
            "language": 'null',
            "url": 'test_url',
            "default_branch": 'master',
            "hooks_url": 'test_hook_url',
            "clone_url": 'test_clone_url',
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ''
        }
        assert result == test
        assert changed == False

    def test_changing_one_variable(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'present',
            'description' : 'new description'
        })
        result, changed = run_module()
        test = {
            "name": 'test_present_repo',
            "full_name": 'test_org_name/test_present_repo',
            "owner": 'test_login',
            "description": 'new description',
            "private": False,
            "archived": False,
            "language": 'null',
            "url": 'test_url',
            "default_branch": 'master',
            "hooks_url": 'test_hook_url',
            "clone_url": 'test_clone_url',
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ''
        }
        assert result == test
        assert changed == True

    def test_changing_multiple_variables(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'present',
            'description' : 'new description',
            'has_downloads' : True
        })
        result, changed = run_module()
        test = {
            "name": 'test_present_repo',
            "full_name": 'test_org_name/test_present_repo',
            "owner": 'test_login',
            "description": 'new description',
            "private": False,
            "archived": False,
            "language": 'null',
            "url": 'test_url',
            "default_branch": 'master',
            "hooks_url": 'test_hook_url',
            "clone_url": 'test_clone_url',
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": True,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ''
        }
        assert result == test
        assert changed == True

    def test_deleting_repository(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'absent',
            'description' : 'new description',
            'has_downloads' : True
        })
        result, changed = run_module()
        test = {}
        assert result == test
        assert changed == True

    def test_deleting_repository_that_does_not_exit(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_not_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'absent',
            'description' : 'new description',
            'has_downloads' : True
        })
        result, changed = run_module()
        test = {}
        assert result == test
        assert changed == True

    def test_error_message_state_choices(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_not_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'maybe',
        })
        result, changed = run_module()
        test = 'Invalid state: maybe'
        assert result == test
        assert changed == False

    def test_error_message_license_choices(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_not_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'present',
            'license_template' : 'not a real template'
        })
        result, changed = run_module()
        test = 'Invalid license: not a real template'
        assert result == test
        assert changed == False

    def test_error_message_license_choices(self):
        set_module_args({
            'token' : 'test_token',
            'repo_name' : 'test_not_present_repo',
            'organization_name' : 'test_org_name',
            'state' : 'present',
            'gitignore_template' : 'not a real template'
        })
        result, changed = run_module()
        test = 'Invalid gitignore template: not a real template'
        assert result == test
        assert changed == False