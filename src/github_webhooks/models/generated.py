"""The generated payload models, and the dispatch table that selects one.

Generated -- do not edit. Rebuild with ``scripts/rebuild_models.sh``.

Source:  https://raw.githubusercontent.com/octokit/openapi-webhooks/d9af91f9ddbad97e5b5765d4b5931c75063c7e22/packages/openapi-webhooks/generated/api.github.com.json
Digest:  sha256:375906eeeace26486c6aecf5869a5e5ad4bba72c6571481ef54fa8c1cada3aae
Scope:   pull-request-closed -> pull_request.closed (WebhookPullRequestClosed), pull-request-opened -> pull_request.opened (WebhookPullRequestOpened), pull-request-review-submitted -> pull_request_review.submitted (WebhookPullRequestReviewSubmitted), push -> push (WebhookPush)

The models describe what GitHub sends, not what it promises (ADR 0001):
every field is optional and unknown fields are kept.
"""

from __future__ import annotations

from typing import Any, Literal

from github_webhooks.models.events import Event
from pydantic import AwareDatetime, ConfigDict, Field, RootModel


class AuthorAssociation(RootModel[str | None]):
    root: str | None = Field(
        None,
        description='How the author is associated with the repository.',
        examples=['OWNER'],
        title='author_association',
    )


class EnterpriseWebhooks(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    description: str | None = Field(
        None, description='A short description of the enterprise.'
    )
    html_url: str | None = Field(
        None, examples=['https://github.com/enterprises/octo-business']
    )
    website_url: str | None = Field(None, description="The enterprise's website URL.")
    id: int | None = Field(
        None, description='Unique identifier of the enterprise', examples=[42]
    )
    node_id: str | None = Field(None, examples=['MDEwOlJlcG9zaXRvcnkxMjk2MjY5'])
    name: str | None = Field(
        None, description='The name of the enterprise.', examples=['Octo Business']
    )
    slug: str | None = Field(
        None,
        description='The slug url identifier for the enterprise.',
        examples=['octo-business'],
    )
    created_at: AwareDatetime | None = Field(None, examples=['2019-01-26T19:01:12Z'])
    updated_at: AwareDatetime | None = Field(None, examples=['2019-01-26T19:14:43Z'])
    avatar_url: str | None = None


class LicenseSimple(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    key: str | None = Field(None, examples=['mit'])
    name: str | None = Field(None, examples=['MIT License'])
    url: str | None = Field(None, examples=['https://api.github.com/licenses/mit'])
    spdx_id: str | None = Field(None, examples=['MIT'])
    node_id: str | None = Field(None, examples=['MDc6TGljZW5zZW1pdA=='])
    html_url: str | None = None


class Link(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class OrganizationSimpleWebhooks(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    login: str | None = Field(None, examples=['github'])
    id: int | None = Field(None, examples=[1])
    node_id: str | None = Field(None, examples=['MDEyOk9yZ2FuaXphdGlvbjE='])
    url: str | None = Field(None, examples=['https://api.github.com/orgs/github'])
    repos_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/repos']
    )
    events_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/events']
    )
    hooks_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/hooks']
    )
    issues_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/issues']
    )
    members_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/members{/member}']
    )
    public_members_url: str | None = Field(
        None, examples=['https://api.github.com/orgs/github/public_members{/member}']
    )
    avatar_url: str | None = Field(
        None, examples=['https://github.com/images/error/octocat_happy.gif']
    )
    description: str | None = Field(None, examples=['A great organization'])


class FieldLinks(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    comments: Link | None = None
    commits: Link | None = None
    statuses: Link | None = None
    html: Link | None = None
    issue: Link | None = None
    review_comments: Link | None = None
    review_comment: Link | None = None
    self: Link | None = None


class Base1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    ref: str | None = Field(
        None, description='The base ref of the stack this pull request belongs to.'
    )
    sha: str | None = Field(
        None, description='The base SHA of the stack this pull request belongs to.'
    )


class PullRequestStack(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    base: Base1 | None = None
    size: int | None = Field(
        None, description='The total number of pull requests in the stack.'
    )
    position: int | None = Field(
        None,
        description='The one-based position of this pull request within the stack, where 1 is the bottom of the stack.',
    )
    id: int | None = Field(
        None, description='The ID of the stack that this pull request belongs to.'
    )
    number: int | None = Field(
        None, description='The number of the stack that this pull request belongs to.'
    )


class Permissions(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    admin: bool | None = None
    pull: bool | None = None
    triage: bool | None = None
    push: bool | None = None
    maintain: bool | None = None


class CodeSearchIndexStatus(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    lexical_search_ok: bool | None = None
    lexical_commit_sha: str | None = None


class Owner(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    login: str | None = None
    id: int | None = None
    node_id: str | None = None
    avatar_url: str | None = None
    gravatar_id: str | None = None
    url: str | None = None
    html_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    organizations_url: str | None = None
    repos_url: str | None = None
    events_url: str | None = None
    received_events_url: str | None = None
    type: str | None = None
    site_admin: bool | None = None


class Permissions2(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    admin: bool | None = None
    maintain: bool | None = None
    push: bool | None = None
    triage: bool | None = None
    pull: bool | None = None


class TemplateRepository(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = None
    node_id: str | None = None
    name: str | None = None
    full_name: str | None = None
    owner: Owner | None = None
    private: bool | None = None
    html_url: str | None = None
    description: str | None = None
    fork: bool | None = None
    url: str | None = None
    archive_url: str | None = None
    assignees_url: str | None = None
    blobs_url: str | None = None
    branches_url: str | None = None
    collaborators_url: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    compare_url: str | None = None
    contents_url: str | None = None
    contributors_url: str | None = None
    deployments_url: str | None = None
    downloads_url: str | None = None
    events_url: str | None = None
    forks_url: str | None = None
    git_commits_url: str | None = None
    git_refs_url: str | None = None
    git_tags_url: str | None = None
    git_url: str | None = None
    issue_comment_url: str | None = None
    issue_events_url: str | None = None
    issues_url: str | None = None
    keys_url: str | None = None
    labels_url: str | None = None
    languages_url: str | None = None
    merges_url: str | None = None
    milestones_url: str | None = None
    notifications_url: str | None = None
    pulls_url: str | None = None
    releases_url: str | None = None
    ssh_url: str | None = None
    stargazers_url: str | None = None
    statuses_url: str | None = None
    subscribers_url: str | None = None
    subscription_url: str | None = None
    tags_url: str | None = None
    teams_url: str | None = None
    trees_url: str | None = None
    clone_url: str | None = None
    mirror_url: str | None = None
    hooks_url: str | None = None
    svn_url: str | None = None
    homepage: str | None = None
    language: str | None = None
    forks_count: int | None = None
    stargazers_count: int | None = None
    watchers_count: int | None = None
    size: int | None = None
    default_branch: str | None = None
    open_issues_count: int | None = None
    is_template: bool | None = None
    topics: list[str] | None = None
    has_issues: bool | None = None
    has_projects: bool | None = None
    has_wiki: bool | None = None
    has_pages: bool | None = None
    has_downloads: bool | None = None
    archived: bool | None = None
    disabled: bool | None = None
    visibility: str | None = None
    pushed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    permissions: Permissions2 | None = None
    allow_rebase_merge: bool | None = None
    temp_clone_token: str | None = None
    allow_squash_merge: bool | None = None
    allow_auto_merge: bool | None = None
    delete_branch_on_merge: bool | None = None
    allow_update_branch: bool | None = None
    use_squash_pr_title_as_default: bool | None = None
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    merge_commit_title: str | None = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    allow_merge_commit: bool | None = None
    subscribers_count: int | None = None
    network_count: int | None = None


class SimpleInstallation(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = Field(
        None, description='The ID of the installation.', examples=[1]
    )
    node_id: str | None = Field(
        None,
        description='The global node ID of the installation.',
        examples=['MDQ6VXNlcjU4MzIzMQ=='],
    )


class SimpleUser(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    name: str | None = None
    email: str | None = None
    login: str | None = Field(None, examples=['octocat'])
    id: int | None = Field(None, examples=[1])
    node_id: str | None = Field(None, examples=['MDQ6VXNlcjE='])
    avatar_url: str | None = Field(
        None, examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: str | None = Field(None, examples=['41d064eb2195891e12d0413f63227ea7'])
    url: str | None = Field(None, examples=['https://api.github.com/users/octocat'])
    html_url: str | None = Field(None, examples=['https://github.com/octocat'])
    followers_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: str | None = Field(
        None, examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str | None = Field(None, examples=['User'])
    site_admin: bool | None = None
    starred_at: str | None = Field(None, examples=['"2020-07-09T00:17:55Z"'])
    user_view_type: str | None = Field(None, examples=['public'])


class TeamSimple(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = Field(
        None, description='Unique identifier of the team', examples=[1]
    )
    node_id: str | None = Field(None, examples=['MDQ6VGVhbTE='])
    url: str | None = Field(
        None,
        description='URL for the team',
        examples=['https://api.github.com/organizations/1/team/1'],
    )
    members_url: str | None = Field(
        None,
        examples=['https://api.github.com/organizations/1/team/1/members{/member}'],
    )
    name: str | None = Field(
        None, description='Name of the team', examples=['Justice League']
    )
    description: str | None = Field(
        None, description='Description of the team', examples=['A great team.']
    )
    permission: str | None = Field(
        None,
        description='Permission that the team will have for its repositories',
        examples=['admin'],
    )
    privacy: str | None = Field(
        None,
        description='The level of privacy this team should have',
        examples=['closed'],
    )
    notification_setting: str | None = Field(
        None,
        description='The notification setting the team has set',
        examples=['notifications_enabled'],
    )
    html_url: str | None = Field(
        None, examples=['https://github.com/orgs/rails/teams/core']
    )
    repositories_url: str | None = Field(
        None, examples=['https://api.github.com/organizations/1/team/1/repos']
    )
    slug: str | None = Field(None, examples=['justice-league'])
    ldap_dn: str | None = Field(
        None,
        description='Distinguished Name (DN) that team maps to within LDAP environment',
        examples=['uid=example,ou=users,dc=github,dc=com'],
    )
    type: str | None = Field(None, description='The ownership type of the team')
    organization_id: int | None = Field(
        None,
        description='Unique identifier of the organization to which this team belongs',
        examples=[37],
    )
    enterprise_id: int | None = Field(
        None,
        description='Unique identifier of the enterprise to which this team belongs',
        examples=[42],
    )


class Comments(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class Commits(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class Html(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class Issue(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class ReviewComment(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class ReviewComments(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class Self(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class Statuses(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class FieldLinks1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    comments: Comments | None = Field(None, title='Link')
    commits: Commits | None = Field(None, title='Link')
    html: Html | None = Field(None, title='Link')
    issue: Issue | None = Field(None, title='Link')
    review_comment: ReviewComment | None = Field(None, title='Link')
    review_comments: ReviewComments | None = Field(None, title='Link')
    self: Self | None = Field(None, title='Link')
    statuses: Statuses | None = Field(None, title='Link')


class Assignee(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class Assignee1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None


class EnabledBy(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class AutoMerge1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    commit_message: str | None = Field(
        None, description='Commit message for the merge commit.'
    )
    commit_title: str | None = Field(
        None, description='Title for the merge commit message.'
    )
    enabled_by: EnabledBy | None = Field(None, title='User')
    merge_method: str | None = Field(None, description='The merge method to use.')


class License(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    key: str | None = None
    name: str | None = None
    node_id: str | None = None
    spdx_id: str | None = None
    url: str | None = None


class Owner1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class Permissions3(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    admin: bool | None = None
    maintain: bool | None = None
    pull: bool | None = None
    push: bool | None = None
    triage: bool | None = None


class Repo(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    allow_auto_merge: bool | None = Field(
        False, description='Whether to allow auto-merge for pull requests.'
    )
    allow_forking: bool | None = Field(
        None, description='Whether to allow private forks'
    )
    allow_merge_commit: bool | None = Field(
        True, description='Whether to allow merge commits for pull requests.'
    )
    allow_rebase_merge: bool | None = Field(
        True, description='Whether to allow rebase merges for pull requests.'
    )
    allow_squash_merge: bool | None = Field(
        True, description='Whether to allow squash merges for pull requests.'
    )
    allow_update_branch: bool | None = None
    archive_url: str | None = None
    archived: bool | None = Field(
        False, description='Whether the repository is archived.'
    )
    assignees_url: str | None = None
    blobs_url: str | None = None
    branches_url: str | None = None
    clone_url: str | None = None
    collaborators_url: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    compare_url: str | None = None
    contents_url: str | None = None
    contributors_url: str | None = None
    created_at: int | AwareDatetime | None = None
    default_branch: str | None = Field(
        None, description='The default branch of the repository.'
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
    )
    deployments_url: str | None = None
    description: str | None = None
    disabled: bool | None = Field(
        None, description='Returns whether or not this repository is disabled.'
    )
    downloads_url: str | None = None
    events_url: str | None = None
    fork: bool | None = None
    forks: int | None = None
    forks_count: int | None = None
    forks_url: str | None = None
    full_name: str | None = None
    git_commits_url: str | None = None
    git_refs_url: str | None = None
    git_tags_url: str | None = None
    git_url: str | None = None
    has_downloads: bool | None = Field(
        True, description='Whether downloads are enabled.'
    )
    has_issues: bool | None = Field(True, description='Whether issues are enabled.')
    has_pages: bool | None = None
    has_projects: bool | None = Field(True, description='Whether projects are enabled.')
    has_wiki: bool | None = Field(True, description='Whether the wiki is enabled.')
    has_discussions: bool | None = Field(
        False, description='Whether discussions are enabled.'
    )
    has_pull_requests: bool | None = Field(
        True, description='Whether pull requests are enabled.'
    )
    pull_request_creation_policy: (
        str | None
    ) = (
        Field(None, description='The policy controlling who can create pull requests: all or collaborators_only.')
    )
    homepage: str | None = None
    hooks_url: str | None = None
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the repository')
    is_template: bool | None = None
    issue_comment_url: str | None = None
    issue_events_url: str | None = None
    issues_url: str | None = None
    keys_url: str | None = None
    labels_url: str | None = None
    language: str | None = None
    languages_url: str | None = None
    license: License | None = Field(None, title='License')
    master_branch: str | None = None
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    merge_commit_title: str | None = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merges_url: str | None = None
    milestones_url: str | None = None
    mirror_url: str | None = None
    name: str | None = Field(None, description='The name of the repository.')
    node_id: str | None = None
    notifications_url: str | None = None
    open_issues: int | None = None
    open_issues_count: int | None = None
    organization: str | None = None
    owner: Owner1 | None = Field(None, title='User')
    permissions: Permissions3 | None = None
    private: bool | None = Field(
        None, description='Whether the repository is private or public.'
    )
    public: bool | None = None
    pulls_url: str | None = None
    pushed_at: int | AwareDatetime | None = None
    releases_url: str | None = None
    role_name: str | None = None
    size: int | None = None
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    ssh_url: str | None = None
    stargazers: int | None = None
    stargazers_count: int | None = None
    stargazers_url: str | None = None
    statuses_url: str | None = None
    subscribers_url: str | None = None
    subscription_url: str | None = None
    svn_url: str | None = None
    tags_url: str | None = None
    teams_url: str | None = None
    topics: list[str] | None = None
    trees_url: str | None = None
    updated_at: AwareDatetime | None = None
    url: str | None = None
    use_squash_pr_title_as_default: (
        bool | None
    ) = (
        Field(False, description='Whether a squash merge commit can use the pull request title as default. **This property is closing down. Please use `squash_merge_commit_title` instead.')
    )
    visibility: str | None = None
    watchers: int | None = None
    watchers_count: int | None = None
    web_commit_signoff_required: (
        bool | None
    ) = (
        Field(None, description='Whether to require contributors to sign off on web-based commits')
    )


class User(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class Base2(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    label: str | None = None
    ref: str | None = None
    repo: Repo | None = Field(None, description='A git repository', title='Repository')
    sha: str | None = None
    user: User | None = Field(None, title='User')


class Repo1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    allow_auto_merge: bool | None = Field(
        False, description='Whether to allow auto-merge for pull requests.'
    )
    allow_forking: bool | None = Field(
        None, description='Whether to allow private forks'
    )
    allow_merge_commit: bool | None = Field(
        True, description='Whether to allow merge commits for pull requests.'
    )
    allow_rebase_merge: bool | None = Field(
        True, description='Whether to allow rebase merges for pull requests.'
    )
    allow_squash_merge: bool | None = Field(
        True, description='Whether to allow squash merges for pull requests.'
    )
    allow_update_branch: bool | None = None
    archive_url: str | None = None
    archived: bool | None = Field(
        False, description='Whether the repository is archived.'
    )
    assignees_url: str | None = None
    blobs_url: str | None = None
    branches_url: str | None = None
    clone_url: str | None = None
    collaborators_url: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    compare_url: str | None = None
    contents_url: str | None = None
    contributors_url: str | None = None
    created_at: int | AwareDatetime | None = None
    default_branch: str | None = Field(
        None, description='The default branch of the repository.'
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
    )
    deployments_url: str | None = None
    description: str | None = None
    disabled: bool | None = Field(
        None, description='Returns whether or not this repository is disabled.'
    )
    downloads_url: str | None = None
    events_url: str | None = None
    fork: bool | None = None
    forks: int | None = None
    forks_count: int | None = None
    forks_url: str | None = None
    full_name: str | None = None
    git_commits_url: str | None = None
    git_refs_url: str | None = None
    git_tags_url: str | None = None
    git_url: str | None = None
    has_downloads: bool | None = Field(
        True, description='Whether downloads are enabled.'
    )
    has_issues: bool | None = Field(True, description='Whether issues are enabled.')
    has_pages: bool | None = None
    has_projects: bool | None = Field(True, description='Whether projects are enabled.')
    has_wiki: bool | None = Field(True, description='Whether the wiki is enabled.')
    has_discussions: bool | None = Field(
        False, description='Whether discussions are enabled.'
    )
    has_pull_requests: bool | None = Field(
        True, description='Whether pull requests are enabled.'
    )
    pull_request_creation_policy: (
        str | None
    ) = (
        Field(None, description='The policy controlling who can create pull requests: all or collaborators_only.')
    )
    homepage: str | None = None
    hooks_url: str | None = None
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the repository')
    is_template: bool | None = None
    issue_comment_url: str | None = None
    issue_events_url: str | None = None
    issues_url: str | None = None
    keys_url: str | None = None
    labels_url: str | None = None
    language: str | None = None
    languages_url: str | None = None
    license: License | None = Field(None, title='License')
    master_branch: str | None = None
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    merge_commit_title: str | None = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merges_url: str | None = None
    milestones_url: str | None = None
    mirror_url: str | None = None
    name: str | None = Field(None, description='The name of the repository.')
    node_id: str | None = None
    notifications_url: str | None = None
    open_issues: int | None = None
    open_issues_count: int | None = None
    organization: str | None = None
    owner: Owner1 | None = Field(None, title='User')
    permissions: Permissions3 | None = None
    private: bool | None = Field(
        None, description='Whether the repository is private or public.'
    )
    public: bool | None = None
    pulls_url: str | None = None
    pushed_at: int | AwareDatetime | None = None
    releases_url: str | None = None
    role_name: str | None = None
    size: int | None = None
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    ssh_url: str | None = None
    stargazers: int | None = None
    stargazers_count: int | None = None
    stargazers_url: str | None = None
    statuses_url: str | None = None
    subscribers_url: str | None = None
    subscription_url: str | None = None
    svn_url: str | None = None
    tags_url: str | None = None
    teams_url: str | None = None
    topics: list[str] | None = None
    trees_url: str | None = None
    updated_at: AwareDatetime | None = None
    url: str | None = None
    use_squash_pr_title_as_default: (
        bool | None
    ) = (
        Field(False, description='Whether a squash merge commit can use the pull request title as default. **This property is closing down. Please use `squash_merge_commit_title` instead.')
    )
    visibility: str | None = None
    watchers: int | None = None
    watchers_count: int | None = None
    web_commit_signoff_required: (
        bool | None
    ) = (
        Field(None, description='Whether to require contributors to sign off on web-based commits')
    )


class Head1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    label: str | None = None
    ref: str | None = None
    repo: Repo1 | None = Field(None, description='A git repository', title='Repository')
    sha: str | None = None
    user: User | None = Field(None, title='User')


class Label1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    color: str | None = Field(
        None,
        description='6-character hex code, without the leading #, identifying the color',
    )
    default: bool | None = None
    description: str | None = None
    id: int | None = None
    name: str | None = Field(None, description='The name of the label.')
    node_id: str | None = None
    url: str | None = Field(None, description='URL for the label')


class Creator(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class Milestone1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    closed_at: AwareDatetime | None = None
    closed_issues: int | None = None
    created_at: AwareDatetime | None = None
    creator: Creator | None = Field(None, title='User')
    description: str | None = None
    due_on: AwareDatetime | None = None
    html_url: str | None = None
    id: int | None = None
    labels_url: str | None = None
    node_id: str | None = None
    number: int | None = Field(None, description='The number of the milestone.')
    open_issues: int | None = None
    state: str | None = Field(None, description='The state of the milestone.')
    title: str | None = Field(None, description='The title of the milestone.')
    updated_at: AwareDatetime | None = None
    url: str | None = None


class RequestedReviewers(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    avatar_url: str | None = None
    deleted: bool | None = None
    email: str | None = None
    events_url: str | None = None
    followers_url: str | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    html_url: str | None = None
    id: int | None = None
    login: str | None = None
    name: str | None = None
    node_id: str | None = None
    organizations_url: str | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    type: str | None = None
    url: str | None = None
    user_view_type: str | None = None


class Parent(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    description: str | None = Field(None, description='Description of the team')
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the team')
    members_url: str | None = None
    name: str | None = Field(None, description='Name of the team')
    node_id: str | None = None
    permission: str | None = Field(
        None, description='Permission that the team will have for its repositories'
    )
    privacy: str | None = None
    repositories_url: str | None = None
    slug: str | None = None
    url: str | None = Field(None, description='URL for the team')


class RequestedReviewers1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    deleted: bool | None = None
    description: str | None = Field(None, description='Description of the team')
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the team')
    members_url: str | None = None
    name: str | None = Field(None, description='Name of the team')
    node_id: str | None = None
    parent: Parent | None = None
    permission: str | None = Field(
        None, description='Permission that the team will have for its repositories'
    )
    privacy: str | None = None
    repositories_url: str | None = None
    slug: str | None = None
    url: str | None = Field(None, description='URL for the team')


class RequestedTeam(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    deleted: bool | None = None
    description: str | None = Field(None, description='Description of the team')
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the team')
    members_url: str | None = None
    name: str | None = Field(None, description='Name of the team')
    node_id: str | None = None
    parent: Parent | None = None
    permission: str | None = Field(
        None, description='Permission that the team will have for its repositories'
    )
    privacy: str | None = None
    repositories_url: str | None = None
    slug: str | None = None
    url: str | None = Field(None, description='URL for the team')


class PullRequest1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    field_links: FieldLinks1 | None = Field(None, alias='_links')
    active_lock_reason: str | None = None
    assignee: Assignee | None = Field(None, title='User')
    assignees: list[Assignee1 | None] | None = None
    author_association: str | None = Field(
        None,
        description='How the author is associated with the repository.',
        title='AuthorAssociation',
    )
    auto_merge: AutoMerge1 | None = Field(
        None,
        description='The status of auto merging a pull request.',
        title='PullRequestAutoMerge',
    )
    base: Base2 | None = None
    body: str | None = None
    closed_at: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    created_at: str | None = None
    diff_url: str | None = None
    draft: bool | None = None
    head: Head1 | None = None
    html_url: str | None = None
    id: int | None = None
    issue_url: str | None = None
    labels: list[Label1] | None = None
    locked: bool | None = None
    merge_commit_sha: str | None = None
    merged_at: str | None = None
    milestone: Milestone1 | None = Field(
        None,
        description='A collection of related issues and pull requests.',
        title='Milestone',
    )
    node_id: str | None = None
    number: int | None = None
    patch_url: str | None = None
    requested_reviewers: list[RequestedReviewers | RequestedReviewers1 | None] | None = (
        None
    )
    requested_teams: list[RequestedTeam] | None = None
    review_comment_url: str | None = None
    review_comments_url: str | None = None
    stack: PullRequestStack | None = None
    state: str | None = None
    statuses_url: str | None = None
    title: str | None = None
    updated_at: str | None = None
    url: str | None = None
    user: User | None = Field(None, title='User')


class Author(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    date: AwareDatetime | None = None
    email: str | None = None
    name: str | None = Field(None, description="The git author's name.")
    username: str | None = None


class Committer(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    date: AwareDatetime | None = None
    email: str | None = None
    name: str | None = Field(None, description="The git author's name.")
    username: str | None = None


class Commit(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    added: list[str] | None = Field(
        None,
        description='An array of files added in the commit. A maximum of 3000 changed files will be reported per commit.',
    )
    author: Author | None = Field(
        None,
        description='Metaproperties for Git author/committer information.',
        title='Committer',
    )
    committer: Committer | None = Field(
        None,
        description='Metaproperties for Git author/committer information.',
        title='Committer',
    )
    distinct: bool | None = Field(
        None,
        description='Whether this commit is distinct from any that have been pushed before.',
    )
    id: str | None = None
    message: str | None = Field(None, description='The commit message.')
    modified: list[str] | None = Field(
        None,
        description='An array of files modified by the commit. A maximum of 3000 changed files will be reported per commit.',
    )
    removed: list[str] | None = Field(
        None,
        description='An array of files removed in the commit. A maximum of 3000 changed files will be reported per commit.',
    )
    timestamp: AwareDatetime | None = Field(
        None, description='The ISO 8601 timestamp of the commit.'
    )
    tree_id: str | None = None
    url: str | None = Field(
        None, description='URL that points to the commit API resource.'
    )


class HeadCommit(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    added: list[str] | None = Field(
        None, description='An array of files added in the commit.'
    )
    author: Author | None = Field(
        None,
        description='Metaproperties for Git author/committer information.',
        title='Committer',
    )
    committer: Committer | None = Field(
        None,
        description='Metaproperties for Git author/committer information.',
        title='Committer',
    )
    distinct: bool | None = Field(
        None,
        description='Whether this commit is distinct from any that have been pushed before.',
    )
    id: str | None = None
    message: str | None = Field(None, description='The commit message.')
    modified: list[str] | None = Field(
        None, description='An array of files modified by the commit.'
    )
    removed: list[str] | None = Field(
        None, description='An array of files removed in the commit.'
    )
    timestamp: AwareDatetime | None = Field(
        None, description='The ISO 8601 timestamp of the commit.'
    )
    tree_id: str | None = None
    url: str | None = Field(
        None, description='URL that points to the commit API resource.'
    )


class Pusher(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    date: AwareDatetime | None = None
    email: str | None = None
    name: str | None = Field(None, description="The git author's name.")
    username: str | None = None


class Repository1(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    allow_auto_merge: bool | None = Field(
        False, description='Whether to allow auto-merge for pull requests.'
    )
    allow_forking: bool | None = Field(
        None, description='Whether to allow private forks'
    )
    allow_merge_commit: bool | None = Field(
        True, description='Whether to allow merge commits for pull requests.'
    )
    allow_rebase_merge: bool | None = Field(
        True, description='Whether to allow rebase merges for pull requests.'
    )
    allow_squash_merge: bool | None = Field(
        True, description='Whether to allow squash merges for pull requests.'
    )
    allow_update_branch: bool | None = None
    archive_url: str | None = None
    archived: bool | None = Field(
        False, description='Whether the repository is archived.'
    )
    assignees_url: str | None = None
    blobs_url: str | None = None
    branches_url: str | None = None
    clone_url: str | None = None
    collaborators_url: str | None = None
    comments_url: str | None = None
    commits_url: str | None = None
    compare_url: str | None = None
    contents_url: str | None = None
    contributors_url: str | None = None
    created_at: int | AwareDatetime | None = None
    custom_properties: dict[str, Any] | None = Field(
        None,
        description='The custom properties that were defined for the repository. The keys are the custom property names, and the values are the corresponding custom property values.',
    )
    default_branch: str | None = Field(
        None, description='The default branch of the repository.'
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
    )
    deployments_url: str | None = None
    description: str | None = None
    disabled: bool | None = Field(
        None, description='Returns whether or not this repository is disabled.'
    )
    downloads_url: str | None = None
    events_url: str | None = None
    fork: bool | None = None
    forks: int | None = None
    forks_count: int | None = None
    forks_url: str | None = None
    full_name: str | None = None
    git_commits_url: str | None = None
    git_refs_url: str | None = None
    git_tags_url: str | None = None
    git_url: str | None = None
    has_downloads: bool | None = Field(
        True, description='Whether downloads are enabled.'
    )
    has_issues: bool | None = Field(True, description='Whether issues are enabled.')
    has_pages: bool | None = None
    has_projects: bool | None = Field(True, description='Whether projects are enabled.')
    has_wiki: bool | None = Field(True, description='Whether the wiki is enabled.')
    has_discussions: bool | None = Field(
        False, description='Whether discussions are enabled.'
    )
    has_pull_requests: bool | None = Field(
        True, description='Whether pull requests are enabled.'
    )
    pull_request_creation_policy: (
        str | None
    ) = (
        Field(None, description='The policy controlling who can create pull requests: all or collaborators_only.')
    )
    homepage: str | None = None
    hooks_url: str | None = None
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the repository')
    is_template: bool | None = None
    issue_comment_url: str | None = None
    issue_events_url: str | None = None
    issues_url: str | None = None
    keys_url: str | None = None
    labels_url: str | None = None
    language: str | None = None
    languages_url: str | None = None
    license: License | None = Field(None, title='License')
    master_branch: str | None = None
    merges_url: str | None = None
    milestones_url: str | None = None
    mirror_url: str | None = None
    name: str | None = Field(None, description='The name of the repository.')
    node_id: str | None = None
    notifications_url: str | None = None
    open_issues: int | None = None
    open_issues_count: int | None = None
    organization: str | None = None
    owner: Owner1 | None = Field(None, title='User')
    permissions: Permissions3 | None = None
    private: bool | None = Field(
        None, description='Whether the repository is private or public.'
    )
    public: bool | None = None
    pulls_url: str | None = None
    pushed_at: int | AwareDatetime | None = None
    releases_url: str | None = None
    role_name: str | None = None
    size: int | None = None
    ssh_url: str | None = None
    stargazers: int | None = None
    stargazers_count: int | None = None
    stargazers_url: str | None = None
    statuses_url: str | None = None
    subscribers_url: str | None = None
    subscription_url: str | None = None
    svn_url: str | None = None
    tags_url: str | None = None
    teams_url: str | None = None
    topics: list[str] | None = None
    trees_url: str | None = None
    updated_at: AwareDatetime | None = None
    url: str | None = None
    visibility: str | None = None
    watchers: int | None = None
    watchers_count: int | None = None
    web_commit_signoff_required: (
        bool | None
    ) = (
        Field(None, description='Whether to require contributors to sign off on web-based commits')
    )


class WebhooksNullableString(RootModel[str | None]):
    root: str | None = None


class WebhooksNumber(RootModel[int | None]):
    root: int | None = Field(None, description='The pull request number.')


class PullRequest2(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    href: str | None = None


class FieldLinks2(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    html: Html | None = Field(None, title='Link')
    pull_request: PullRequest2 | None = Field(None, title='Link')


class WebhooksReview(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    field_links: FieldLinks2 | None = Field(None, alias='_links')
    author_association: str | None = Field(
        None,
        description='How the author is associated with the repository.',
        title='AuthorAssociation',
    )
    body: str | None = Field(None, description='The text of the review.')
    commit_id: str | None = Field(None, description='A commit SHA for the review.')
    html_url: str | None = None
    id: int | None = Field(None, description='Unique identifier of the review')
    node_id: str | None = None
    pull_request_url: str | None = None
    state: str | None = None
    submitted_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None
    user: User | None = Field(None, title='User')


class AutoMerge(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    enabled_by: SimpleUser | None = None
    merge_method: str | None = Field(None, description='The merge method to use.')
    commit_title: str | None = Field(
        None, description='Title for the merge commit message.'
    )
    commit_message: str | None = Field(
        None, description='Commit message for the merge commit.'
    )


class Milestone(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    url: str | None = Field(
        None, examples=['https://api.github.com/repos/octocat/Hello-World/milestones/1']
    )
    html_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World/milestones/v1.0']
    )
    labels_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/milestones/1/labels'],
    )
    id: int | None = Field(None, examples=[1002604])
    node_id: str | None = Field(None, examples=['MDk6TWlsZXN0b25lMTAwMjYwNA=='])
    number: int | None = Field(
        None, description='The number of the milestone.', examples=[42]
    )
    state: str | None = Field(
        'open', description='The state of the milestone.', examples=['open']
    )
    title: str | None = Field(
        None, description='The title of the milestone.', examples=['v1.0']
    )
    description: str | None = Field(
        None, examples=['Tracking milestone for version 1.0']
    )
    creator: SimpleUser | None = None
    open_issues: int | None = Field(None, examples=[4])
    closed_issues: int | None = Field(None, examples=[8])
    created_at: AwareDatetime | None = Field(None, examples=['2011-04-10T20:09:31Z'])
    updated_at: AwareDatetime | None = Field(None, examples=['2014-03-03T18:58:10Z'])
    closed_at: AwareDatetime | None = Field(None, examples=['2013-02-12T13:22:01Z'])
    due_on: AwareDatetime | None = Field(None, examples=['2012-10-09T23:39:01Z'])


class Label(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = None
    node_id: str | None = None
    url: str | None = None
    name: str | None = None
    description: str | None = None
    color: str | None = None
    default: bool | None = None
    archived_by: SimpleUser | None = Field(
        None,
        description='The user who archived the label, or `null` if it has not been archived.',
    )


class Repository(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = Field(
        None, description='Unique identifier of the repository', examples=[42]
    )
    node_id: str | None = Field(None, examples=['MDEwOlJlcG9zaXRvcnkxMjk2MjY5'])
    name: str | None = Field(
        None, description='The name of the repository.', examples=['Team Environment']
    )
    full_name: str | None = Field(None, examples=['octocat/Hello-World'])
    license: LicenseSimple | None = None
    forks: int | None = None
    permissions: Permissions | None = None
    owner: SimpleUser | None = None
    private: bool | None = Field(
        False, description='Whether the repository is private or public.'
    )
    html_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World']
    )
    description: str | None = Field(None, examples=['This your first repo!'])
    fork: bool | None = None
    url: str | None = Field(
        None, examples=['https://api.github.com/repos/octocat/Hello-World']
    )
    archive_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}'],
    )
    assignees_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/assignees{/user}'],
    )
    blobs_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}'],
    )
    branches_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/branches{/branch}'],
    )
    collaborators_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}'],
    )
    comments_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/comments{/number}'],
    )
    commits_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/commits{/sha}']
    )
    compare_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}'],
    )
    contents_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/contents/{+path}'],
    )
    contributors_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/contributors']
    )
    deployments_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/deployments']
    )
    downloads_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/downloads']
    )
    events_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/events']
    )
    forks_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/forks']
    )
    git_commits_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}'],
    )
    git_refs_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}'],
    )
    git_tags_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}'],
    )
    git_url: str | None = Field(
        None, examples=['git:github.com/octocat/Hello-World.git']
    )
    issue_comment_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}'],
    )
    issue_events_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues/events{/number}'],
    )
    issues_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues{/number}'],
    )
    keys_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/keys{/key_id}']
    )
    labels_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/labels{/name}']
    )
    languages_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/languages']
    )
    merges_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/merges']
    )
    milestones_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/milestones{/number}'],
    )
    notifications_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}'],
    )
    pulls_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/pulls{/number}'],
    )
    releases_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/releases{/id}']
    )
    ssh_url: str | None = Field(
        None, examples=['git@github.com:octocat/Hello-World.git']
    )
    stargazers_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/stargazers']
    )
    statuses_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/statuses/{sha}'],
    )
    subscribers_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/subscribers']
    )
    subscription_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/subscription']
    )
    tags_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/tags']
    )
    teams_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/teams']
    )
    trees_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}'],
    )
    clone_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World.git']
    )
    mirror_url: str | None = Field(
        None, examples=['git:git.example.com/octocat/Hello-World']
    )
    hooks_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/hooks']
    )
    svn_url: str | None = Field(
        None, examples=['https://svn.github.com/octocat/Hello-World']
    )
    homepage: str | None = Field(None, examples=['https://github.com'])
    language: str | None = None
    forks_count: int | None = Field(None, examples=[9])
    stargazers_count: int | None = Field(None, examples=[80])
    watchers_count: int | None = Field(None, examples=[80])
    size: int | None = Field(
        None,
        description='The size of the repository, in kilobytes. Size is calculated hourly. When a repository is initially created, the size is 0.',
        examples=[108],
    )
    default_branch: str | None = Field(
        None, description='The default branch of the repository.', examples=['master']
    )
    open_issues_count: int | None = Field(None, examples=[0])
    is_template: bool | None = Field(
        False,
        description='Whether this repository acts as a template that can be used to generate new repositories.',
        examples=[True],
    )
    topics: list[str] | None = None
    has_issues: bool | None = Field(
        True, description='Whether issues are enabled.', examples=[True]
    )
    has_projects: bool | None = Field(
        True, description='Whether projects are enabled.', examples=[True]
    )
    has_wiki: bool | None = Field(
        True, description='Whether the wiki is enabled.', examples=[True]
    )
    has_pages: bool | None = None
    has_downloads: bool | None = Field(
        True,
        deprecated=True,
        description='Whether downloads are enabled.',
        examples=[True],
    )
    has_discussions: bool | None = Field(
        False, description='Whether discussions are enabled.', examples=[True]
    )
    has_pull_requests: bool | None = Field(
        True, description='Whether pull requests are enabled.', examples=[True]
    )
    pull_request_creation_policy: (
        str | None
    ) = (
        Field(None, description='The policy controlling who can create pull requests: all or collaborators_only.', examples=['all'])
    )
    archived: bool | None = Field(
        False, description='Whether the repository is archived.'
    )
    disabled: bool | None = Field(
        None, description='Returns whether or not this repository disabled.'
    )
    visibility: str | None = Field(
        'public', description='The repository visibility: public, private, or internal.'
    )
    pushed_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:06:43Z'])
    created_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    updated_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:14:43Z'])
    allow_rebase_merge: bool | None = Field(
        True,
        description='Whether to allow rebase merges for pull requests.',
        examples=[True],
    )
    temp_clone_token: str | None = None
    allow_squash_merge: bool | None = Field(
        True,
        description='Whether to allow squash merges for pull requests.',
        examples=[True],
    )
    allow_auto_merge: bool | None = Field(
        False,
        description='Whether to allow Auto-merge to be used on pull requests.',
        examples=[False],
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
        examples=[False],
    )
    allow_update_branch: bool | None = Field(
        False,
        description='Whether or not a pull request head branch that is behind its base branch can always be updated even if it is not required to be up to date before merging.',
        examples=[False],
    )
    use_squash_pr_title_as_default: (
        bool | None
    ) = (
        Field(False, deprecated=True, description='Whether a squash merge commit can use the pull request title as default. **This property is closing down. Please use `squash_merge_commit_title` instead.')
    )
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    merge_commit_title: str | None = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    allow_merge_commit: bool | None = Field(
        True,
        description='Whether to allow merge commits for pull requests.',
        examples=[True],
    )
    allow_forking: bool | None = Field(
        None, description='Whether to allow forking this repo'
    )
    web_commit_signoff_required: (
        bool | None
    ) = (
        Field(False, description='Whether to require contributors to sign off on web-based commits')
    )
    open_issues: int | None = None
    watchers: int | None = None
    master_branch: str | None = None
    starred_at: str | None = Field(None, examples=['"2020-07-09T00:17:42Z"'])
    anonymous_access_enabled: bool | None = Field(
        None, description='Whether anonymous git access is enabled for this repository'
    )
    code_search_index_status: CodeSearchIndexStatus | None = Field(
        None, description='The status of the code search index for this repository'
    )


class RepositoryWebhooks(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    id: int | None = Field(
        None, description='Unique identifier of the repository', examples=[42]
    )
    node_id: str | None = Field(None, examples=['MDEwOlJlcG9zaXRvcnkxMjk2MjY5'])
    name: str | None = Field(
        None, description='The name of the repository.', examples=['Team Environment']
    )
    full_name: str | None = Field(None, examples=['octocat/Hello-World'])
    license: LicenseSimple | None = None
    organization: SimpleUser | None = None
    forks: int | None = None
    permissions: Permissions | None = None
    owner: SimpleUser | None = None
    private: bool | None = Field(
        False, description='Whether the repository is private or public.'
    )
    html_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World']
    )
    description: str | None = Field(None, examples=['This your first repo!'])
    fork: bool | None = None
    url: str | None = Field(
        None, examples=['https://api.github.com/repos/octocat/Hello-World']
    )
    archive_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}'],
    )
    assignees_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/assignees{/user}'],
    )
    blobs_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}'],
    )
    branches_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/branches{/branch}'],
    )
    collaborators_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}'],
    )
    comments_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/comments{/number}'],
    )
    commits_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/commits{/sha}']
    )
    compare_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}'],
    )
    contents_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/contents/{+path}'],
    )
    contributors_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/contributors']
    )
    deployments_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/deployments']
    )
    downloads_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/downloads']
    )
    events_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/events']
    )
    forks_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/forks']
    )
    git_commits_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}'],
    )
    git_refs_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}'],
    )
    git_tags_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}'],
    )
    git_url: str | None = Field(
        None, examples=['git:github.com/octocat/Hello-World.git']
    )
    issue_comment_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}'],
    )
    issue_events_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues/events{/number}'],
    )
    issues_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues{/number}'],
    )
    keys_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/keys{/key_id}']
    )
    labels_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/labels{/name}']
    )
    languages_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/languages']
    )
    merges_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/merges']
    )
    milestones_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/milestones{/number}'],
    )
    notifications_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}'],
    )
    pulls_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/pulls{/number}'],
    )
    releases_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/releases{/id}']
    )
    ssh_url: str | None = Field(
        None, examples=['git@github.com:octocat/Hello-World.git']
    )
    stargazers_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/stargazers']
    )
    statuses_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/statuses/{sha}'],
    )
    subscribers_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/subscribers']
    )
    subscription_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/subscription']
    )
    tags_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/tags']
    )
    teams_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/teams']
    )
    trees_url: str | None = Field(
        None,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}'],
    )
    clone_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World.git']
    )
    mirror_url: str | None = Field(
        None, examples=['git:git.example.com/octocat/Hello-World']
    )
    hooks_url: str | None = Field(
        None, examples=['http://api.github.com/repos/octocat/Hello-World/hooks']
    )
    svn_url: str | None = Field(
        None, examples=['https://svn.github.com/octocat/Hello-World']
    )
    homepage: str | None = Field(None, examples=['https://github.com'])
    language: str | None = None
    forks_count: int | None = Field(None, examples=[9])
    stargazers_count: int | None = Field(None, examples=[80])
    watchers_count: int | None = Field(None, examples=[80])
    size: int | None = Field(
        None,
        description='The size of the repository, in kilobytes. Size is calculated hourly. When a repository is initially created, the size is 0.',
        examples=[108],
    )
    default_branch: str | None = Field(
        None, description='The default branch of the repository.', examples=['master']
    )
    open_issues_count: int | None = Field(None, examples=[0])
    is_template: bool | None = Field(
        False,
        description='Whether this repository acts as a template that can be used to generate new repositories.',
        examples=[True],
    )
    topics: list[str] | None = None
    custom_properties: dict[str, Any] | None = Field(
        None,
        description='The custom properties that were defined for the repository. The keys are the custom property names, and the values are the corresponding custom property values.',
    )
    has_issues: bool | None = Field(
        True, description='Whether issues are enabled.', examples=[True]
    )
    has_projects: bool | None = Field(
        True, description='Whether projects are enabled.', examples=[True]
    )
    has_wiki: bool | None = Field(
        True, description='Whether the wiki is enabled.', examples=[True]
    )
    has_pages: bool | None = None
    has_downloads: bool | None = Field(
        True, description='Whether downloads are enabled.', examples=[True]
    )
    has_discussions: bool | None = Field(
        False, description='Whether discussions are enabled.', examples=[True]
    )
    has_pull_requests: bool | None = Field(
        True, description='Whether pull requests are enabled.', examples=[True]
    )
    pull_request_creation_policy: (
        str | None
    ) = (
        Field(None, description='The policy controlling who can create pull requests: all or collaborators_only.')
    )
    archived: bool | None = Field(
        False, description='Whether the repository is archived.'
    )
    disabled: bool | None = Field(
        None, description='Returns whether or not this repository disabled.'
    )
    visibility: str | None = Field(
        'public', description='The repository visibility: public, private, or internal.'
    )
    pushed_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:06:43Z'])
    created_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    updated_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:14:43Z'])
    allow_rebase_merge: bool | None = Field(
        True,
        description='Whether to allow rebase merges for pull requests.',
        examples=[True],
    )
    template_repository: TemplateRepository | None = None
    temp_clone_token: str | None = None
    allow_squash_merge: bool | None = Field(
        True,
        description='Whether to allow squash merges for pull requests.',
        examples=[True],
    )
    allow_auto_merge: bool | None = Field(
        False,
        description='Whether to allow Auto-merge to be used on pull requests.',
        examples=[False],
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
        examples=[False],
    )
    allow_update_branch: bool | None = Field(
        False,
        description='Whether or not a pull request head branch that is behind its base branch can always be updated even if it is not required to be up to date before merging.',
        examples=[False],
    )
    use_squash_pr_title_as_default: (
        bool | None
    ) = (
        Field(False, deprecated=True, description='Whether a squash merge commit can use the pull request title as default. **This property is closing down. Please use `squash_merge_commit_title` instead.')
    )
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    merge_commit_title: str | None = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    allow_merge_commit: bool | None = Field(
        True,
        description='Whether to allow merge commits for pull requests.',
        examples=[True],
    )
    allow_forking: bool | None = Field(
        None, description='Whether to allow forking this repo'
    )
    web_commit_signoff_required: (
        bool | None
    ) = (
        Field(False, description='Whether to require contributors to sign off on web-based commits')
    )
    subscribers_count: int | None = None
    network_count: int | None = None
    open_issues: int | None = None
    watchers: int | None = None
    master_branch: str | None = None
    starred_at: str | None = Field(None, examples=['"2020-07-09T00:17:42Z"'])
    anonymous_access_enabled: bool | None = Field(
        None, description='Whether anonymous git access is enabled for this repository'
    )


class WebhookPullRequestReviewSubmitted(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    action: Literal["submitted"] | None = None
    enterprise: EnterpriseWebhooks | None = None
    installation: SimpleInstallation | None = None
    organization: OrganizationSimpleWebhooks | None = None
    pull_request: PullRequest1 | None = Field(None, title='Simple Pull Request')
    repository: RepositoryWebhooks | None = None
    review: WebhooksReview | None = None
    sender: SimpleUser | None = None


class WebhookPush(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    after: str | None = Field(
        None, description='The SHA of the most recent commit on `ref` after the push.'
    )
    base_ref: WebhooksNullableString | None = None
    before: str | None = Field(
        None, description='The SHA of the most recent commit on `ref` before the push.'
    )
    commits: list[Commit] | None = Field(
        None,
        description='An array of commit objects describing the pushed commits. (Pushed commits are all commits that are included in the `compare` between the `before` commit and the `after` commit.) The array includes a maximum of 2048 commits. If necessary, you can use the [Commits API](https://docs.github.com/rest/commits) to fetch additional commits.',
    )
    compare: str | None = Field(
        None,
        description='URL that shows the changes in this `ref` update, from the `before` commit to the `after` commit. For a newly created `ref` that is directly based on the default branch, this is the comparison between the head of the default branch and the `after` commit. Otherwise, this shows all commits until the `after` commit.',
    )
    created: bool | None = Field(
        None, description='Whether this push created the `ref`.'
    )
    deleted: bool | None = Field(
        None, description='Whether this push deleted the `ref`.'
    )
    enterprise: EnterpriseWebhooks | None = None
    forced: bool | None = Field(
        None, description='Whether this push was a force push of the `ref`.'
    )
    head_commit: HeadCommit | None = Field(None, title='Commit')
    installation: SimpleInstallation | None = None
    organization: OrganizationSimpleWebhooks | None = None
    pusher: Pusher | None = Field(
        None,
        description='Metaproperties for Git author/committer information.',
        title='Committer',
    )
    ref: str | None = Field(
        None,
        description='The full git ref that was pushed. Example: `refs/heads/main` or `refs/tags/v3.14.1`.',
    )
    repository: Repository1 | None = Field(
        None, description='A git repository', title='Repository'
    )
    sender: SimpleUser | None = None


class Head(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    label: str | None = None
    ref: str | None = None
    repo: Repository | None = None
    sha: str | None = None
    user: SimpleUser | None = None


class Base(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    label: str | None = None
    ref: str | None = None
    repo: Repository | None = None
    sha: str | None = None
    user: SimpleUser | None = None


class PullRequest(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    url: str | None = Field(
        None, examples=['https://api.github.com/repos/octocat/Hello-World/pulls/1347']
    )
    id: int | None = Field(None, examples=[1])
    node_id: str | None = Field(None, examples=['MDExOlB1bGxSZXF1ZXN0MQ=='])
    html_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World/pull/1347']
    )
    diff_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World/pull/1347.diff']
    )
    patch_url: str | None = Field(
        None, examples=['https://github.com/octocat/Hello-World/pull/1347.patch']
    )
    issue_url: str | None = Field(
        None, examples=['https://api.github.com/repos/octocat/Hello-World/issues/1347']
    )
    commits_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits'],
    )
    review_comments_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments'],
    )
    review_comment_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}'],
    )
    comments_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/issues/1347/comments'],
    )
    statuses_url: str | None = Field(
        None,
        examples=['https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e'],
    )
    number: int | None = Field(
        None,
        description='Number uniquely identifying the pull request within its repository.',
        examples=[42],
    )
    state: str | None = Field(
        None,
        description='State of this Pull Request. Either `open` or `closed`.',
        examples=['open'],
    )
    locked: bool | None = Field(None, examples=[True])
    title: str | None = Field(
        None,
        description='The title of the pull request.',
        examples=['Amazing new feature'],
    )
    user: SimpleUser | None = None
    body: str | None = Field(None, examples=['Please pull these awesome changes'])
    labels: list[Label] | None = None
    milestone: Milestone | None = None
    active_lock_reason: str | None = Field(None, examples=['too heated'])
    created_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    updated_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    closed_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    merged_at: AwareDatetime | None = Field(None, examples=['2011-01-26T19:01:12Z'])
    merge_commit_sha: str | None = Field(
        None, examples=['e5bd3914e2e596debea16f433f57875b5b90bcd6']
    )
    assignee: SimpleUser | None = None
    assignees: list[SimpleUser] | None = None
    requested_reviewers: list[SimpleUser] | None = None
    requested_teams: list[TeamSimple] | None = None
    head: Head | None = None
    base: Base | None = None
    field_links: FieldLinks | None = Field(None, alias='_links')
    author_association: AuthorAssociation | None = None
    auto_merge: AutoMerge | None = None
    stack: PullRequestStack | None = None
    draft: bool | None = Field(
        None,
        description='Indicates whether or not the pull request is a draft.',
        examples=[False],
    )
    merged: bool | None = None
    mergeable: bool | None = Field(None, examples=[True])
    rebaseable: bool | None = Field(None, examples=[True])
    mergeable_state: str | None = Field(None, examples=['clean'])
    merged_by: SimpleUser | None = None
    comments: int | None = Field(None, examples=[10])
    review_comments: int | None = Field(None, examples=[0])
    maintainer_can_modify: bool | None = Field(
        None,
        description='Indicates whether maintainers can modify the pull request.',
        examples=[True],
    )
    commits: int | None = Field(None, examples=[3])
    additions: int | None = Field(None, examples=[100])
    deletions: int | None = Field(None, examples=[3])
    changed_files: int | None = Field(None, examples=[5])


class PullRequestWebhook(PullRequest):
    model_config = ConfigDict(
        extra='allow',
    )
    allow_auto_merge: bool | None = Field(
        False, description='Whether to allow auto-merge for pull requests.'
    )
    allow_update_branch: bool | None = Field(
        None, description="Whether to allow updating the pull request's branch."
    )
    delete_branch_on_merge: bool | None = Field(
        False,
        description='Whether to delete head branches when pull requests are merged.',
    )
    merge_commit_message: str | None = Field(
        None,
        description="The default value for a merge commit message.\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    merge_commit_title: str | None = Field(
        None,
        description='The default value for a merge commit title.\n- `PR_TITLE` - default to the pull request\'s title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., "Merge pull request #123 from branch-name").',
    )
    squash_merge_commit_message: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit message:\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.")
    )
    squash_merge_commit_title: (
        str | None
    ) = (
        Field(None, description="The default value for a squash merge commit title:\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).")
    )
    use_squash_pr_title_as_default: (
        bool | None
    ) = (
        Field(False, description='Whether a squash merge commit can use the pull request title as default. **This property is closing down. Please use `squash_merge_commit_title` instead.**')
    )


class WebhookPullRequestClosed(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    action: Literal["closed"] | None = None
    enterprise: EnterpriseWebhooks | None = None
    installation: SimpleInstallation | None = None
    number: WebhooksNumber | None = None
    organization: OrganizationSimpleWebhooks | None = None
    pull_request: PullRequestWebhook | None = None
    repository: RepositoryWebhooks | None = None
    sender: SimpleUser | None = None


class WebhookPullRequestOpened(Event):
    model_config = ConfigDict(
        extra='allow',
    )
    action: Literal["opened"] | None = None
    enterprise: EnterpriseWebhooks | None = None
    installation: SimpleInstallation | None = None
    number: WebhooksNumber | None = None
    organization: OrganizationSimpleWebhooks | None = None
    pull_request: PullRequestWebhook | None = None
    repository: RepositoryWebhooks | None = None
    sender: SimpleUser | None = None


DISPATCH: dict[str, type[Event]] = {
    "pull_request.closed": WebhookPullRequestClosed,
    "pull_request.opened": WebhookPullRequestOpened,
    "pull_request_review.submitted": WebhookPullRequestReviewSubmitted,
    "push": WebhookPush,
}
