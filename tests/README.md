# E2E tests

## How to run the tests
### Setup
Create a python virtual env
```shell
virtualenv venv
```
Activate it
```shell
source venv/bin/activate
```
Install prerequisites
```shell
pip install -r tests/requirments.txt
```
## Run the tests
```shell
behave tests/features/ -D endpoint="endpoint to test"
```
The results are visible on stdout but also an output file is created
```shell
plain.output
```

## Lint
```shell
 pycodestyle tests/ --max-line-length=120
```

## Pipeline

![pipeline](pipeline.png)

I propose 4 stages for the pipeline
- Build
- Test
- Deploy
- Test-prod
#### Build
This stage is triggered and every push and consists in 2 jobs, 
build the docker image and checking the codestytle for the testing project

#### Test
In this stage the e2e tests run, it is building and running the docker container and
firing the e2e tests, this stage is triggered on a merge request event.
The results of the tests are available on the artifacts of the job, visible and downloadable on gitlab

#### Deploy
This stage is a manual step to deploy on production.
It is available after the code is merged on master.
I decided to have this step manual for several reasons like:
- not every code change should be deployed immediately in production
- I imagined a release team responsible to deploy on production, that will also create a release note,
  maybe also perform some manual check
- not all the engineer have the "power" to deploy on production

Side note, I did not implemented the deploy scripts

#### Test-prod
This stage is composed by 2 job.
- The first `e2e-test-prod` is triggered as soon as `deploy-prod` is finished.
It is running the e2e-tests but against the real endpoint that is specified on the job.
It is running only the scenarios that are tagged with `@prod`
- The second `non-functional-test` it is instead a scheduled job, so can be scheduled to run nightly/weekly/etc.
It runs non-functional test (performance) that I did not implemented in this homework but they should be taken in consideration
