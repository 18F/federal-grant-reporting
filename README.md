# The 10x Federal Grant Reporting project

## Project description

### The [10x Federal Grant Reporting project](#project-description) is enabling simpler, faster, easier, better resolution of single audit findings by agencies and grantees alike.

To that end, we're building prospective shared solutions for the single audit finding resolution process.

### Distiller
Distiller, provides easier access to data, reducing a multi-day process to less than five minutes. This stands to help auditors, grant managers, and agency CFOs as well as grantees.

### PDF Audit Data Extractor 
This prototype will locate all findings in any audit pdf and extracts specific information about each audit findings. Namely Audit finding texts and Grantee responses to start. Ultimately the goal is to improve entering data into the Federal Audit Clearinghouse. When uploading a single audit pdf, the PDF Audit Data Extractor will extract and pre-populate finding information into the data collection form so that auditors or grantees can  review and confirm the data rather than requiring them to copy and paste or retype critical data. When you consider that for each finding, multiple fields are required to be filled out, and the number of audit findings each year, the time savings is considerable. One outside auditor for a state audit said he typically sees 100 findings in each years audit and that this could save 1.5 hours to his work and another 1.5 hours to the grantees staff time considering the additional fields added to the data collection form.

### Earlier prototypes explored 
_SAFR: Single audit finding resolution,_ focuses on single audit finding resolution, which is a high-priority element of post-award financial grant reporting. By facilitating direct communication and increasing visibility into the state of work, the prototype dramatically 1) streamlines the finding resolution process and 2) gives agencies unprecedented visibility into single audit findings relevant to their shared grantees, thereby reducing costly duplication of effort for agencies and grantees alike.



## How can you help?

### Federal granting agency
If you're someone who works with single audits at a federal agency, we're interested in speaking with you. 

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).

### Independent auditors
If you're someone who's created single audits, we're interested in talking with you and better understanding your current process and any pain points around creating audits and adding them to the Federal Audit Clearinghouse.

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).

### Grantees
If you've developed corrective action plans or been involved in single audit finding resolution, we'd love to talk.

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).

## What we've done so far

For background and context, see [this project's history](/project-history.md).


## Local development

1. Install [Docker][]. If you're on OS X, install Docker for Mac. If you're on Windows, install Docker for Windows.

2. Open terminal (Mac) or command line (PC) and “enter” to move into the `single-audit` directory at the repository root:

  ```
  cd single-audit
  ```

3. Run the three following commands:

  ```shell
  docker-compose build 
  docker-compose run app python manage.py migrate
  docker-compose run app python manage.py createsuperuser
  ```

`docker-compose build` builds the containers by pulling down a number of libraries which take a few minutes to download and install but you only do this once. 

`docker-compose run app python manage.py migrate` runs a Django command to create the database and the tables and columns. 

`docker-compose run app python manage.py createsuperuser` creates an account to access admin panel.

4. Once the above commands are successful, run:

  ```
  docker-compose up
  ```

  This will start up all required servers in containers and output their
  log information to stdout.

5. Visit [http://localhost:8000/][] directly to access the site.

You can access the admin panel at `/admin` by logging in with the super user credentials you created in the step above.

### Create sample finding data

Once you can access the admin interface for the project (at `/admin`), you'll be able to create sample finding data locally.

Start by adding and saving a new finding: http://127.0.0.1:8000/admin/resolve_findings/finding/add/.

### See the project locally

Once your new finding record is saved, visit http://127.0.0.1:8000/findings/1/ to see the Finding Resolution Page.

Here is what that page looks like as of June 2019:

![screenshot of Finding Resolution page](https://user-images.githubusercontent.com/3209501/60221160-737c7f80-982d-11e9-9092-be88541e5141.png)

... and here is what the comments section looks like as of June 2019:

![another screenshot of Finding Resolution page](https://user-images.githubusercontent.com/3209501/60221179-8b540380-982d-11e9-8bbb-38f6faeefe3c.png)


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

[Docker]: https://www.docker.com/
[http://localhost:8000/]: http://localhost:8000/
