# How to Contribute
I am glad that you are reading this as I need help to make this project successful and widely used. You will find on this page all the necessary information to become contributor in my [project](https://github.com/mdabrowski1990/uds).
I have provided list of most important chapters for all contributors depending on a role so you do not have to read everything:
- Developers:
  - [Before you start](#before-you-start)
  - [Coding Convention](#coding-convention)
  - [Software Development Process Lifecycle](#sdpl) - especially:
    - [Design](#design)
    - [Implementation](#implementation)
    - [Testing](#testing)
- Testers:
  - [Before you start](#before-you-start)
  - [Software Development Process Lifecycle](#sdpl)  - especially:
    - [Testing](*#testing)
- Sponsors:
  - [Before you start](#before-you-start)
  - [Sponsoring](#sponsoring)
- Other:
  - [Before you start](#before-you-start)
  - [Software Development Process Lifecycle](#sdpl)


## Before you start
I recommend you to [join our mailing list](https://groups.google.com/g/uds-package-development/about) first as we discuss hot topics there. It is also a place to simply say 'hi', tell a few words about yourself, what are you good at, what can you or would like to do in the project. We welcome anyone who wants to help while providing open and supportive environment.
If you are willing to help, but you have no python skills or no money to share, you can still be an influential member of this project. Please write an email to uds-package-development@googlegroups.com and let us know about your motivation and skill. We will find you a role matching your ambitions!


## Coding Convention
Following standards/guidelines are applied in the code:
- [pep8](https://www.python.org/dev/peps/pep-0008/)
- [pep257](https://www.python.org/dev/peps/pep-0257/)
- reStructuredText for all docstrings

Compliance with these standards/guidelines is checked during [static test analysis](#static-code-analysis).


## <a name="sdpl">Software Development Process Lifecycle</a>
Due to limited resources that we have available for the project, I want to focus on using them efficiently. My plan is to maximize work undone and pay big attention to quality and automation.

![SDLC](https://www.tutorialspoint.com/sdlc/images/sdlc_stages.jpg)
1. [Planning](#planning)
3. [Defining](#defining)
4. [Design](#design)
5. [Implementation](#implementation)
6. [Testing](#testing)
7. [Deployment](#deployment)

### Planning
This phase is all about analysing the needs of sponsors and user

Input:
- UDS Standards (e.g. ISO 14229)
- Communication bus related standards (e.g. ISO 11898, ISO 17458, ISO 13400, ISO 14230, ISO 17987)
- [Bugs and feature requests](https://github.com/mdabrowski1990/uds/issues/new/choose) created by the package users (with tag `[INVESTIGATE]` in their title)\
- Special sponsors requests

<a name="planning-output">Output</a>:
- Piorities and roadmap defined in [group forum](https://groups.google.com/g/uds-package-development)
- [Milestones](https://github.com/mdabrowski1990/uds/milestones) with general scope and intention defined

### Defining
Once, analysing requirements is finished, we can actually define scope of work to do and create tasks to track it. Each task shall contain following information:
- What features/functionalities does it provide for users?
- What existing functionalities does this change affect (e.g. Server, Client, CAN Transport Interface)?
- How would we test the change?
  - What kind of dynamic tests would we perform to make sure that the change does not introduce critical bugs?
  - How would we check that the feature/functionality is integrated and can be used with already existing software?
  - Are there any new system tests required/desired to test this feature/functionality?
- Acceptance criteria (how do we know that the task is completed)

Input to this phase is [output from planning phase](#planning-output).

<a name="defining-output">Output</a>:
- New story/stories created in [development project](https://github.com/mdabrowski1990/uds/projects/1)

### Design - TODO: refine
It would be great to have [UML](https://pl.wikipedia.org/wiki/Unified_Modeling_Language) models for our software, but to be honest I do not see this happening. Therefore, I decided to accept any form of design files (unless we decide to change this decision). As a lone developer, I have started myself with schemes created in my notebook.

Input to this phase is [output from defining phase](#defining-output).

<a name="design-output">Output</a>:
- Schemes with basic description what and where shall be added/changed in given story

### Implementation

Input to this phase is [output from defining phase](#defining-output).

<a name="implementation-output">Output</a>:

### Testing

Input to this phase is [output from implementation phase](#implementation-output).

<a name="testing-output">Output</a>:

#### Static Testing
##### Static Code Analysis
##### Review
#### Dynamic Testing
##### Unit Tests
##### Integration Tests
##### System Tests

### Deployment

Input to this phase is [output from testing phase](#testing-output).

<a name="deployment-output">Output</a>:

## Sponsoring
### ISO Standards
### Equipment
