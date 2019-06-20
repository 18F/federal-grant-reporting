# Federal Grant Reporting Project
Improving the experience of federal grant reporting.

# Single audit resolution
Enabling simpler, faster, easier, better resolution of single audit findings by
agencies and grantees alike.

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


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
