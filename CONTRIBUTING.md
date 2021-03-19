# How to Contribute
I am glad that you are reading this as I need help to make this project successful and widely used. You will find on this page all the necessary information to become valuable contributor in my [UDS project](https://github.com/mdabrowski1990/uds).
Below is the list of most important topics for all contributors depending on a role they are eager to fullfil:
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


## Before You Start
I recommend you to [join our mailing list](https://groups.google.com/g/uds-package-development/about) first as we discuss hot topics there. It is also a place to simply say 'hi', tell a few words about yourself, what are you good at, what can you or would like to do in the project. We welcome anyone who wants to help while providing open and supportive environment and offering great learning experience.
If you are willing to help, but you have no python skills, you can still be an influential member of this project! Let us know what are your skill and we will find you a role matching your ambitions and abilities!


## Coding Convention
List of standards/guidelines that are followed in the code:
- [pep8](https://www.python.org/dev/peps/pep-0008/)
- [pep257](https://www.python.org/dev/peps/pep-0257/)
- reStructuredText for all docstrings

Compliance with these standards/guidelines is checked during [static test analysis](#static-code-analysis) and [review](#review).


## <a name="sdpl">Software Development Process Lifecycle</a>
Due to limited resources that we have available for the project, I want to focus on using them efficiently. My plan is to maximize work undone and pay big attention to quality and automation and this is visible in the shape of the processes that I have proposed.

![SDLC](https://www.tutorialspoint.com/sdlc/images/sdlc_stages.jpg)
1. [Planning](#planning)
3. [Defining](#defining)
4. [Design](#design)
5. [Implementation](#implementation)
6. [Testing](#testing)
7. [Deployment](#deployment)

### Planning
This phase is all about analysing the needs of our sponsors and user. It is meant to optimize and adjust a general long-term plan that we have, so the project provides maximal value to our stakeholders.

Input:
- UDS Standards (e.g. ISO 14229)
- Communication bus related standards (e.g. ISO 11898, ISO 17458, ISO 13400, ISO 14230, ISO 17987)
- [Bugs and feature requests](https://github.com/mdabrowski1990/uds/issues/new/choose) created by the package users (with tag `[INVESTIGATE]` in their title)\
- Special sponsors requests

<a name="planning-output">Output</a>:
- Piorities and roadmap defined in [group forum](https://groups.google.com/g/uds-package-development)
- [Milestones](https://github.com/mdabrowski1990/uds/milestones) with general scope defined/refined

### Defining
Once, analysing requirements is finished, we can actually define scope of work to do and create tasks to track it efficiently. Each task shall contain following information:
- What features/functionalities is it meant to provide for users?
- What existing functionalities does this change affect (e.g. Server, Client, CAN Transport Interface)?
- How would we test the change?
  - What kind of dynamic tests would we perform to make sure that the change does not introduce critical bugs?
  - How would we check that the feature/functionality is integrated and can be used with already existing software?
  - Are there any new system tests required/desired to test this feature/functionality?
- Acceptance criteria (how do we know that the task is completed)

Input to this phase is [output from planning phase](#planning-output).

<a name="defining-output">Output</a>:
- New story/stories created in [development project](https://github.com/mdabrowski1990/uds/projects/1)

### Design
It would be great to have [UML](https://pl.wikipedia.org/wiki/Unified_Modeling_Language) models for our software, but to be honest I do not see this happening. Therefore, I decided to accept any form of design files (unless we decide to change this decision). As a lone developer, I have started with schemes which I have drawn in my notebook. You can use [draw.io](https://app.diagrams.net/) or any other tool that you feel confortable with. The point is, I want us to make designs and plan the code (interfaces, how it interacts with existing code/functionalities, etc.) before we start the actual implementation.

Input to this phase is [output from defining phase](#defining-output).

<a name="design-output">Output</a>:
- Schemes (in any form) which decribes what will be added/changed to the existing code to provide additional functionality. These schemes shall be added to the related user story.

### Implementation
Please follow these simple rule when implementing the code:
- Before you start coding, please assign yourself to approriate issue in [issues tracking project](https://github.com/mdabrowski1990/uds/projects/1).
- You must never commit directly to main branch (it is blocked). Please create separate branch to track your changes.
- I encourage everyone to use TDD, aTDD, pair-programming and ofter walkthroughs/informal reviews (e.g. [rubber duck debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging)), but it is really up to you how you implement your tasks.
- Unit tests are must have and they must be merged together with the code (there is no approval for merging code and unit tests separately).
- Before pull request is created, all acceptance criteria (defined in related tasks) should be met.
- Pull request must be linked with tasks (defined in [issues tracking project](https://github.com/mdabrowski1990/uds/projects/1)) that it implements.
- Before code is merged, it must be [reviewed and approved](#review).

Input to this phase is [output from defining phase](#defining-output).

<a name="implementation-output">Output</a>:
- Updated [main branch](https://github.com/mdabrowski1990/uds/tree/main) with changes that were delivered.

#### Static Code Analysis
Static Code Analysis is performed automatically on each commit according the [policy file](https://github.com/mdabrowski1990/uds/blob/main/tests/prospector_profile.yaml).

#### Review
Review before each pull request is mandatory.
Desired number of reviewers: 2-4 (with one senior member).

### Testing
In this phase, system (e.g. exploratory) tests might be executed. The idea is to confirm that the pacakge has no major problems and it is ready to be released.
We would like to have all system tests executed before the deployment, but I am aware that this will be problematic, therefore the scope of tests will be decided before each release after analysis of changes impact on the delivered product.

Input to this phase is [output from implementation phase](#implementation-output).

<a name="testing-output">Output</a>:
- [Issues](https://github.com/mdabrowski1990/uds/issues/new/choose) (most likely [bugs](https://github.com/mdabrowski1990/uds/issues/new?assignees=&labels=bug&template=00_bug_report.md&title=%5BINVESTIGATE%5D+enter+short+name+here)) related to all findings discovered during testing.

### Deployment
We want to release new versions of our package as often as possible. To make sure the product is ready, please complete this checklist:
- [ ] Is [readme file](https://github.com/mdabrowski1990/uds/blob/main/README.rst) updated?
- [ ] Is [documentation](https://github.com/mdabrowski1990/uds/tree/main/docs) updated with desription for all new features?

Perform following actions to complete release of the new version:
- [ ] Assign new version according to [semantic versioning](https://semver.org/)
- [ ] Upload new version of documentation:
  - [ ] [UDS - ReadTheDocs](https://uds.readthedocs.io/en/latest/)
  - [ ] [UDS - GitHub Pages](https://mdabrowski1990.github.io/uds/)
- [ ] Upload new version to pypi with release notes.

Input to this phase is [output from testing phase](#testing-output).

Output:
- New version of the package.

## Sponsoring
We need sponsors to make sure this project is continued. There are many ways you could help (not neccessarily giving us money, nevertheless it is more than welcome).

### ISO Standards
We need access to newest ISO standards, therefore we would appreciate donation to any of these pools:
- [UDS standards pool](https://www.paypal.com/pools/c/8xzKVUT0ba)
- [CAN related standards pool](https://www.paypal.com/pools/c/8xBlQ11Adr)
- [LIN related standards pool](https://www.paypal.com/pools/c/8xBlUHGPpE)
- [Ethernet related standards pool](https://www.paypal.com/pools/c/8xBm451jNW)

### Equipment
We need equipment for testing reasons. If you could give/share it with us, it would be really appreciated.

### Testing
Performing system tests will probably be the bottleneck of the development, therefore any form of help with tests would albo be very much appreciated.

### $$$
I appreciate any form of gratitute, but 💰 is desired one 🤑. You will be rewarded with additional influence and user support if you decide to make a donation.
