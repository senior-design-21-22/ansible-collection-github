.. _general_repository:


********************
general_repository
********************

**A module that manages a repository in an organization.**


Version added: 0.0.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- A module that creates, modifies, or deletes a repository in an organization.


Requirements
------------
There are no further requirements needed to run this module.


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
  <!-- TOP OF TABLE -->
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th>Choices/<font color="blue">Required</font></th>
            <th width="50%">Comments</th>
        </tr>
  <!-- GITHUB TOKEN -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>

                <td>
                </td>

                <td>
                        <div>True</div>
                </td>
                
                <td>
                        <div>GitHub Token used to authenticate with the Github Rest API.</div>
                </td>
            </tr>

  <!-- ENTERPRISE_URL -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enterprise_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                
                <td>
                        <div>Unecessary in event of user token</div>
                </td>
                
                <td>
                        <div>False</div>
                </td>
                
                <td>
                        <div>An enterprise URL is necessary when a module is recieving an enterprise token. In the structure of the URL, it is vital that it includes the subdirectory path to the GitHub API as well as the correct version type. An template of this is:</div>
                        <code>https://github.&ltENTERPRISE DOMAIN&gt/api/v3</code>
                </td>
            </tr>
  <!-- ORGANIZATION NAME-->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>organization_name</b>                                                                            <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>                                             <!-- TYPE -->
                    </div>
                </td>
                
                <td>
                        <div></div>                                                                         <!-- CHOICES/DEFAULTS -->
                </td>
                
                <td>
                        <div>True</div>
                </td>
                
                <td>
                        <div>The organization containing the repository being managed.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- REPO -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>repo</b>                                                    <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>                                             <!-- TYPE -->
                    </div>
                </td>
                
                <td>
                        <div></div><!-- CHOICES/DEFAULTS -->
                </td>
                
                <td>
                        <div>True</div>
                </td>
                <td>
                        <div>The name of the repository being managed.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- STATE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div><code>present</code> <code>absent</code></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>True</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Whether <code>present</code> or <code>absent</code>, this determines whether the creation/managing of a repo or the deletion of a repo is required.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- DESCRIPTION -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">str</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Description of the repository. Will show up in the README.md and 'About'</div>  <!-- COMMENTS -->
                </td>
            </tr> 

            
    <!-- HOMEPAGE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>homepage</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">str</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div> </div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Link or name of the homepage to the repository.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- HAS_ISSUES -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>has_issues</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Whether or not the repository will have the ability to create issues.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- HAS_WIKI -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>has_wiki</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Whether or not the repository will have a wiki tab.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- HAS_DOWNLOADS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>has_downloads</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Whether or not the repository will have a downloads tab.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- HAS_PROJECTS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>has_projects</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Whether or not the repository will have a projects tab.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- TEAM_ID -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>team_id</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">int</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>A team can be added through their ID number in the organization.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- AUTO INIT -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auto_init</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>This will initalize a README.md file when true.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- LICENSE TEMPLATE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>license_template</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">str</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div><code>gpl-3.0</code></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>License restrictions put on the repository</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- GITIGNORE TEMPLATE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gitignore_template</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">str</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Template for gitignore to use. These can be found at <code>https://github.com/github/gitignore</code>.</div>  <!-- COMMENTS -->
                </td>
            </tr>
      <!-- ALLOW SQUASH MERGE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow_squash_merge</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Status of whether or not squash merges are allowable.</div>  <!-- COMMENTS -->
                </td>
            </tr>
      <!-- ALLOW MERGE COMMIT -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow_merge_commit</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Status of whether or not merge commits are allowable.</div>  <!-- COMMENTS -->
                </td>
            </tr>
        <!-- ALLOW REBASE MERGE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow_rebase_merge</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Status of whether or not rebase merges are allowable.</div>  <!-- COMMENTS -->
                </td>
            </tr>
        <!-- DELTE BRANCH ON MERGE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delete_branch_on_merge</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Status of whether or to delete the branch upon a merge.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- END OF TABLE-->      
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: "Create repository within enterprise organization"
        ohioit.github.general_repository:
          token: "12345"
          organization_name: SSEP
          enterprise_url: https://github.<ENTERPRISE DOMAIN>/api/v3
          repo_name: brad-repo
          private: true
          description: "this is a test"
          homepage: "test homepage"
          has_issues: true
          has_wiki: false
          has_downloads: false
          has_projects: false
          team_id: 46
          auto_init: true
          license_template: gpl-3.0
          gitignore_template: "Haskell"
          allow_squash_merge: true
          allow_merge_commit: false
          allow_rebase_merge: true
          delete_branch_on_merge: true
          state: present
        register: result
        
    - name: "Delete repository within enterprise organization"
        ohioit.github.general_repository:
          token: "12345"
          organization_name: SSEP
          enterprise_url: https://github.<ENTERPRISE DOMAIN>/api/v3
          repo_name: brad-repo
          state: absent


Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2" width="35%">Key</th>
            <th width="15%">Returned</th>                                                                           
            <th width="50%">Description</th>
        </tr>
  <!-- REPO -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dict</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Dictionary of components of current repository</div>
                </td>
            </tr>
  <!-- REPO.ALLOW_MERGE_COMMIT -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.allow_merge_commit</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Status of whether or not merge commits are allowable.</div>
                </td>
            </tr>
  <!-- REPO.ALLOW_REBASE_MERGE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.allow_rebase_merge</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Status of whether or not rebase merges are allowable.</div>
                </td>
            </tr>
  <!-- REPO.ALLOW_SQUASH_MERGE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.allow_squash_merge</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Status of whether or not squash merges are allowable.</div>
                </td>
            </tr>
  <!-- REPO.ARCHIVED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.archived</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The status of whether or not the repository is archived.</div>
                </td>
            </tr>
  <!-- REPO.CLONE_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.clone_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The URL in which one can locally clone a repository.</div>
                </td>
            </tr>
  <!-- REPO.DEFAULT_BRANCH -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.default_branch</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Name of the branch that the repository will show on startup</div>
                </td>
            </tr>
  <!-- REPO.DELETE_BRANCH_ON_MERGE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.delete_branch_on_merge</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Status of whether or to delete the branch upon a merge.</div>
                </td>
            </tr>
  <!-- REPO.DESCRIPTION-->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.description</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Description of the repository. Will show up in the <code>README.md</code> and <code>About</code> </div>
                </td>
            </tr>
  <!-- REPO.HAS_DOWNLOADS-->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.has_downloads</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Whether or not the repository will have a downloads tab.</div>
                </td>
            </tr>
  <!-- REPO.HAS_ISSUES-->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.has_issues</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Whether or not the repository will have a issues tab.</div>
                </td>
            </tr>
  <!-- REPO.HAS_PROJECTS-->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.has_projects</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Whether or not the repository will have a projects tab.</div>
                </td>
            </tr>
  <!-- REPO.HAS_WIKI -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.has_wiki</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Whether or not the repository will have a wiki tab.</div>
                </td>
            </tr>
  <!-- REPO.HOMEPAGE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.homepage</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Link or name of the homepage to the repository.</div>
                </td>
            </tr>
  <!-- REPO.HOOKS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.hooks_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The API URL of where to access the repository's hooks.</div>
                </td>
            </tr>
  <!-- REPO.LANGUAGE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.language</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The primary language of the repository.</div>
                </td>
            </tr>
  <!-- REPO.NAME -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.name</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The name of the repository.</div>
                </td>
            </tr>
  <!-- REPO.OWNER -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.owner</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The organization to which the repository belongs.</div>
                </td>
            </tr>
  <!-- REPO.PRIVATE -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.private</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>The status of whether or not the repository will be private.</div>
                </td>
            </tr>
  <!-- REPO.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>repo.url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If Repo provided is valid within the organization</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>API URL of where the repository is accessible</div>
                </td>
            </tr>
    <!-- END OF TABLE -->
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Brad Golski (@bgolski)
- Jacob Eicher (@jacobeicher)
- Nolan Khounborin (@khounborinn)
- Tyler Zwolenik (@TylerZwolenik)
