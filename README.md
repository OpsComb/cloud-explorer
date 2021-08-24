# Cloud Explorer
An API Gateway to multiple Cloud Providers.

The projects has been designed to create a common gateway for interating with multiple
infrastructures(clouds).

### Why Common Gateway?
1) Applications need not maintain/secure access keys to different environments. They can use 1 request format for interacting with different infrastructures
2) A similar response structure for all requests makes it easier for consumers to focus on data without concerning about parse logics in multi-cloud environments
3) Access tokens/keys can be maintained at 1 location for cloud/non-cloud inter cloud applications thus providing greater control over access
4) Features like request throttling help you control the hits any consumer makes to the cloud. (Unbounded requests can lead to request throttling at cloud end as well which can certainly cause production issues)

Some small but significant additions include -
1) Support for adding default tags for resources
2) Instant Audit Log for resource creation or deletion
3) Notification can be given to stakeholder for infra changes (support for filtering events)
4) Restrict creation of certain resources directly via API. Only whitelisted users can create resource without approval

### To run this project
1) Install [pipenv](https://pypi.org/project/pipenv/)

2) Create a virtualenv or let pipenv manage that for you. Install dependencies !!

3) Configure any local settings in `settings/local.py`

4) Ready to launch django's runserver by hitting `python manage.py runserver`

### Run inside a container
The project contains Containerfile. You can use any tool (like docker or buildah) to compile this file and make a container image

The Containerfile contains multiple targets for production and debug builds

## For prod build
> buildah bud --squash --target=prod -t cloud-explorer .

## For debug build
> buildah bud --target=debug -t cloud-explorer-debug .


Run the image using podman (or docker)
> podman run cloud-explorer
