# Requestbin-acceptance-test

### Table of contents

- [Requestbin-acceptance-test](#requestbin-acceptance-test)
    - [Table of contents](#table-of-contents)
  - [Description](#description)
    - [File organization](#file-organization)
  - [Prerequisites](#prerequisites)
  - [How to use](#how-to-use)
    - [Instalation](#instalation)
    - [Run test cases](#run-test-cases)
  - [References](#references)
  
---
## Description

Acceptance testing with Behave and following the screenplay pattern. The base of framework is built with Python programming language and Gherkin

### File organization

 | Path | Description |
| :--- | :---: |
|features | Features is the place where we will keep all our user stories written in Gherkins |
|steps | The step definitions is where we will put all our steps that are written in the Features section |
| data | It is where we will put all the data that we will need to execute the test cases such as payload, headers, etc. |
| models | It is where we model the request bodies |
| facts| It is where we will put all the classes that we will need to initialize the execute of the test cases, we can say that it is associated with Given step. Facts will consist of a series of interactions|
| task | It is where we will put all the classes related with the business goal, i mean, with the action that i will do in the execute of the test case, we can say that it is associated with When step. Tasks will consist of a series of interactions|
| questions | It is where we will put all the classes to check that the task was successful, we can say that it is associated with the Then step. Questions will consist of a series of interactions|
|interactions | It is where we will put all the classes related with the interactions with the SUT, such as navigating to websites, clicking buttons, entering values in form fields, or submitting HTTP requests to a REST API. This series of actions are composite a results in a facts, task or questions |


## Prerequisites

You’ll need Python installed

--- 

## How to use 

### Instalation
To install the framework, you must follow the following steps:   

1. ``` 
    git clone https://github.com/squella/Requestbin.git
2. ```
    python3 -m venv env
3. ``` 
    source env/bin/activate
4. ```
    pip install -r requirements.txt
5. ``` 
    behave
    
### Run test cases 

Now, time to run your tests!, to do so, just run:

``` 
    behave
```

--- 


## References

[Behave](https://behave.readthedocs.io/en/stable/)