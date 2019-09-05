# The 10x Federal Grant Reporting project

## Project description

### The [10x Federal Grant Reporting project](#project-description) is enabling simpler, faster, easier, better resolution of single audit findings by agencies and grantees alike.

To that end, we're building two prospective shared solutions for the single audit finding resolution process.

### SAFR: Single audit finding resolution
The first element of the prototype, "SAFR," focuses on single audit finding resolution, which is a high-priority element of post-award financial grant reporting. By facilitating direct communication and increasing visibility into the state of work, the prototype dramatically 1) streamlines the finding resolution process and 2) gives agencies unprecedented visibility into single audit findings relevant to their shared grantees, thereby reducing costly duplication of effort for agencies and grantees alike.

### Distiller
A second element of the prototype, "Distiller," provides easier access to data, reducing a multi-day process to less than five minutes. This stands to help auditors, grant managers, and agency CFOs as well as grantees.

## How can you help?

**Federal granting agency**
If you're someone who works with single audits at a federal agency, we're interested in speaking with you.

[File an issue](https://github.com/18F/federal-grant-reporting/issues) or email us at federal-grant-reporting@gsa.gov

**Independent auditors**
If you're someone who's worked on single audits, we're interested in talking with you and better understanding your current process and any pain points around creating audits and adding them to the Federal Audit Clearinghouse.

[File an issue](https://github.com/18F/federal-grant-reporting/issues) or email us at federal-grant-reporting@gsa.gov

## What we've done so far

For background and context, see [this project's history](/project-history.md).


## Local installation

This is a Django app designed to run on Python 3.7.3.
[pipenv](https://pipenv.readthedocs.io) is recommended for creating a virtual
environment and managing dependencies. If you don't already have `pipenv`
installed:

1. Run `pip --version` and confirm that your `pip` uses Python 3, not Python 2, then
2. Install pipenv by running `pip install pipenv`.

Now you can prepare your development environment by running:

```
git clone git@github.com:18F/federal-grant-reporting.git
cd federal-grant-reporting
cd single-audit
pipenv shell
pipenv install
```

You will also need to set up a local [PostgreSQL](https://www.postgresql.org) database that matches the configuration in `single-audit/single_audit/settings/development.py`. (Alternately, you can create a local database and user and update the app's configuration to match.)

First, create a new Postgres database from the command line:

```bash
createdb FGR_LOCAL_DB
```

Then, once you are logged into the FGR_LOCAL_DB Postgres database:

```SQL
CREATE USER fgr_local_user;
\password fgr_local_user;
{enter the password defined in development.py}
```

At this point, if you try running the project locally, you may see a message like: "You have 17 unapplied migration(s)..."

Apply these migrations to your local database:

```bash
python manage.py migrate --settings=single_audit.settings.development
```

Now you can start the project locally:

```bash
./manage.py runserver --settings=single_audit.settings.development
```

The app should now be running at http://localhost:8000 or http://127.0.0.1:8000.

### Creating a superuser

The Django project contains an admin interface at `/admin`.

To access the admin interface, you'll need to create a superuser first. Run the following on your command line to create a superuser on your local machine:

```
./manage.py createsuperuser --settings=single_audit.settings.development
```

You will be prompted to supply a username, email, and password.

Having completed that process, you will be able to access the admin interface at `/admin` using your new superuser account.

### Create sample finding data

Once you can access the admin interface for the project (at `/admin`), you'll be able to create sample finding data locally.

Start by adding and saving a new finding: http://127.0.0.1:8000/admin/resolve_findings/finding/add/.

### See the project locally

Once your new finding record is saved, visit http://127.0.0.1:8000/finding/1/ to see the Finding Resolution Page.

Here is what that page looks like as of June 2019:

![screenshot of Finding Resolution page](https://user-images.githubusercontent.com/3209501/60221160-737c7f80-982d-11e9-9092-be88541e5141.png)

... and here is what the comments section looks like as of June 2019:

![another screenshot of Finding Resolution page](https://user-images.githubusercontent.com/3209501/60221179-8b540380-982d-11e9-8bbb-38f6faeefe3c.png)

## Background

The Federal Grant Reporting (FGR) Project is sponsored by the GSA [Technology Transformation Service](https://www.gsa.gov/about-us/organization/federal-acquisition-service/technology-transformation-services)'s [10x team](https://10x.gsa.gov). 10x helps turn ideas from federal employees into real projects that improve the experience people have with our government through technology. [The 10x process](https://10x.gsa.gov/the-10x-process/) incubates these ideas through a series of stages: Investigation, Discovery, Development, and Scale. The FGR project has reached the third stage.

## Phase I: Investigation

The first phase of this project consisted of in-depth user research, including direct observation of a grant report submission process and the receipt and analysis of submitted reports.

* Link to Phase I [final presentation](https://docs.google.com/presentation/d/1ZSIbFb3CR3aUyJWLBVIQj0qMj_VfVVaBEj1tXkWvdLQ/edit?ts=59569845#slide=id.p) (:lock:)

## Phase II: Discovery

During the second phase, the team broadened its focus to an analysis of the grant reporting actions shared by the majority of federal grantees, the data standards development work happening across the federal government, and the opportunities to improve related systems and processes for agencies and auditors. During this phase, the team also prototyped several proofs of concept for reducing the reporting burden for federal grant recipients.

* Link to Phase II [final presentation](https://docs.google.com/presentation/d/1w1N7bTz0fQ8e8MePlY3t6T450eYBlBVweEdZIQQ3rkI/edit#slide=id.g3770e36ff6_0_0) (:lock:)

## Phase III: Development

The team is building out a minimum viable product (MVP) focused on improving the single audit finding resolution experience for federal grant managers and grantees. This work is informed by and in conversation with several agencies as well as the ongoing data standards work taking place across the federal government.


## Important resources

* Phase 3 [area of focus](https://docs.google.com/document/d/1qMXaHjQhaT4crKhMoXSnzQgBsjItdM94kILYJoSf-9Y/edit) (:lock:)
* Phase 3 [timeline](https://docs.google.com/document/d/138eE7wCwZCrDpuHr4ufulan6bRByTlcZCnPOkpilgvA/edit#) (:lock:)


## Project structure

```
federal-grant-reporting/
├── sam-to-ffr/
├── single-audit/
│   ├── distiller/
│   ├── fac/
│   ├── resolve_findings/
│   └── single_audit/
└── tools/
```

* `tools`: A home for one-off scripts written in service of the project.
* `sam-to-ffr`: Flask prototype application from Phase II; a proof-of-concept app which fills out fields of the Federal Financial Report form based on data from SAM.gov.
* `single-audit`: Main application being developed during Phase III; a Django project with several sub-apps.
  * `single-audit/single_audit`: Home for project-wide resources and settings, such as shared CSS, URL structure, and shared settings for development/production.
  * `single-audit/distiller`: Prototype app — exploring the idea of parsing data from the Federal Audit Clearinghouse and distilling it down into the most relevant information.
  * `single-audit/fac`: Prototype app — exploring the idea of a front-end interface for the Federal Audit Clearinghouse which could let findings be entered in a templatized way. This is currently a stub (i.e., very much an early work in progress).
  * `single-audit/resolve_findings`: Prototype app for Single Audit Finding Resolution. Actively under development.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
