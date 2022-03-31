.. _branch_protection:


********************
branch_protection
********************

**A module that allows the modification of branch protections.**


Version added: 0.0.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- A module that allows the addition, deletion and modification of existing branch protections.


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
                        <div>The organization in which branch protections will be modified.</div>  <!-- COMMENTS -->
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
                        <div>The repository in which branch protections will be modified.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- BRANCH -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>branch</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>True</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>The branch whose protections will be modified.</div>  <!-- COMMENTS -->
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
                        <div><code>present</code> or <code>absent</code></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>True</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>When provided <code>present</code>, the branch protection will either be created of modified. When provided <code>absent</code>, the branch protection will be deleted.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
            
    <!-- BRANCH PROTECTIONS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>branch_protections</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dict</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div> <code>strict</code> <code>contexts</code> <code>enforce_admins</code> <code>dismissal_users</code> <code>dismissal_teams</code> <code>dismiss_stale_reviews</code> <code>require_code_owner_reviews</code> <code>required_approving_review_count</code> <code>user_push_restrictions</code> <code>team_push_restrictions</code> </div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>The following elements will be modified or created upon the state being 'present'.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- strict -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>strict</b>                                                             <!-- PARAMETER -->
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
                        <div>The branch must be up to date with the base branch before merging.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- CONTEXTS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>contexts</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>The list of status checks to require in order to merge into this branch. This will set the contexts to exactly what is in the list.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- ENFORCE ADMINS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enforce_admins</b>                                                             <!-- PARAMETER -->
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
                        <div>Set to <code>true</code> to enforce required status checks for repository administrators.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- DISMISSAL_USERS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dismissal_users</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Specify which users can dismiss pull request reviews.  This will set the users to exactly who is in the list.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- DISMISSAL TEAMS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dismissal_teams</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Specify which teams can dismiss pull request reviews. This will set the users to exactly who is in the list.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- DISMISS STALE REVIEWS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dismiss_stale_reviews</b>                                                             <!-- PARAMETER -->
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
                        <div>Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- REQUIRE CODE OWNER REVIEWS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>require_code_owner_reviews</b>                                                             <!-- PARAMETER -->
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
                        <div>Blocks merging pull requests until code owners have reviewed.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- REQUIRED APPROVING REVIEW COUNT -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>required_approving_review_count</b>                                                             <!-- PARAMETER -->
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
                        <div>Specifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- USER PUSH RESTRICTIONS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user_push_restrictions</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Restrict who can push to the protected branch. User restrictions are only available for organization-owned repositories. This will set the users to exactly who is in the list.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- TEAM PUSH RESTRICTIONS -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>team_push_restrictions</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>Restrict who can push to the protected branch. Team restrictions are only available for organization-owned repositories. This will set the users to exactly who is in the list.</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- END OF TABLE-->      
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: "MODIFY/CREATE BRANCH PROTECTIONS IN BRANCH"
        ohioit.github.branch_protection:
          token: "12345"
          organization_name: "SSEP"
          enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
          repo: "testing-repo-public"
          branch: "tyler-branch"
          state: present
          branch_protections:
            strict: false
            contexts: ["default", "ci-test"]
            enforce_admins: false
            dismissal_users: ["nk479217", "bg881717"]
            dismissal_teams: ["tyler-team"]
            dismiss_stale_reviews: false
            require_code_owner_reviews: true
            required_approving_review_count: 5
            user_push_restrictions: ["nk479217"]
            team_push_restrictions: ["tyler-team"]
        register: result
        
    - name: "REMOVE ALL BRANCH PROTECTIONS FROM BRANCH"
      ohioit.github.branch_protection:
        token: "12345"
        organization_name: "SSEP"
        enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
        repo: "testing-repo-public"
        branch: "tyler-branch"
        state: absent
        register: result


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
  <!-- BRANCH PROTECTIONS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dict</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch provided is valid.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Dictionary describing branch protections of a single branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.ALLOW_DELETIONS.ENABLED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.allow_deletions.enabled</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Allows deletions within the branch.</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.ALLOW_FORCE_PUSHES.ENABLED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.allow_force_pushes.enabled</b>                                                        <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Allows force pushes within the branch.</div>
                </td>
            </tr>
      
            
  <!-- BRANCH_PROTECTIONS.ENFORCE_ADMINS.ENABLED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.enforce_admins.enabled</b>                                                        <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Enforce all configured restrictions for administrators. Set to true to enforce required status checks for repository administrators.</div>
                </td>
            </tr>
                        
  <!-- BRANCH_PROTECTIONS.ENFORCE_ADMINS.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.enforce_admins.url</b>                                                       <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>API URL where to find the enforce_admins status</div>
                </td>
            </tr>
               
  <!-- BRANCH_PROTECTIONS.REQUIRED_CONVERSATION_RESOLUTION.ENABLED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_conversation_resolution.enabled</b>                                             <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Requires all conversations on code to be resolved before a pull request can be merged into a branch that matches this rule. Set to false to disable.</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.DISMISS_STALE_REVIEWS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.dismiss_stale_reviews</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Set to <code>true</code> if you want to automatically dismiss approving reviews when someone pushes a new commit.</div>
                </td>
            </tr>
            
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.DISMISSAL_RESTRICTIONS.TEAMS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.dismissal_restrictions.teams</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Specifies which teams can dismiss pull request reviews.</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.DISMISSAL_RESTRICTIONS.TEAMS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.dismissal_restrictions.teams_url</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>API URL to access the dismissal restriction teams.</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.DISMISSAL_RESTRICTIONS.USERS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.dismissal_restrictions.users</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>List of user dictionaries and their information</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.DISMISSAL_RESTRICTIONS.USERS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.dismissal_restrictions.users_url</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>API URL access to the users with dismissal restrictions</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.REQUIRE_CODE_OWNER_REVIEWS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.require_code_owner_reviews</b>                                         <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                    <!-- WHEN IS IT RETURNED -->
                <td>
                                                                                                                        <!--DESCRIPTION-->
                            <div>Blocks merging pull requests until code owners have reviewed.</div>
                </td>
            </tr>
            
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.REQUIRED_APPROVING_REVIEW_COUNT -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.required_approving_review_count</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">int</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>Specifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.REQUIRED_PULL_REQUEST_REVIEWS.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_pull_request_reviews.url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL to access required pull request reviews.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.REQUIRED_SIGNATURES.ENABLED -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_signatures.enabled</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>Status of whether signatures are required.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.REQUIRED_SIGNATURES.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_signatures.url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL to access status of whether signatures are required.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.REQUIRED_STATUS_CHECKS.CONTEXTS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_status_checks.contexts</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>The list of status checks to require in order to merge into this branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.REQUIRED_STATUS_CHECKS.CONTEXTS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.required_status_checks.contexts_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>The URL where to find the list of status checks to require in order to merge into this branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.APPS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.apps</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>list of apps that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.APPS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.apps_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL where to find the list of apps that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.TEAMS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.teams</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>list of teams that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.TEAMS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.teams_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL where to find the list of teams that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.USERS -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.users</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>list of users that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.USERS_URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.users_url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL where to find the list of users that restrict who can push to the protected branch.</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.RESTRICTIONS.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.restrictions.url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL where to find branch protection restrictions</div>
                </td>
            </tr>
  <!-- BRANCH_PROTECTIONS.URL -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>branch_protections.url</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">str</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>If branch protections are present.</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>URL where to find branch protections</div>
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
