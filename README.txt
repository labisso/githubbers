-------------------------------------------------------------------------------
githubbers
-------------------------------------------------------------------------------

This simple utility queries Github for committer details and formats them
into a template. This is useful for generating static includes for a website.
Since committers don't change very often, the script can be called by
cron occasionally.

Usage:
===============================================================================

githubbers -c path/to/config


Example Configuration File
===============================================================================

user: nimbusproject
repository: nimbus

ignore:
    logins: [jimmy, johnny, nimbusproject]
    names: ["Some Dude", sandwich]

template: |
    <ul>
    {% for user in contributors %}
        <li>
            <img src="{{ user.gravatar_uri() }}"> {{ user.name }}
        </li>
    {% endfor %}
    </ul>


Templates are Jinja2 format. The `committers` variable is provided, a list of
committers sorted by number of commits.
