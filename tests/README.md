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
behave tests/features/
```
The results are visible on stdout but also an output file is created
```shell
plain.output
```