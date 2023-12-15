# <img src="https://upload.wikimedia.org/wikipedia/commons/f/f5/Capx-logo-redux.svg" alt="logo of the Capacity Exchange" width="50" title="Capacity Exchange" style="transform:translateY(5px)"> The Capacity Exchange

The Capacity Exchange (CapX) is a project focusing on [Global Approaches to Local Skills Development](https://meta.wikimedia.org/wiki/Movement_Strategy/Initiatives/Global_Approach_for_Local_Skill_Development) within and for the Wikimedia Movement. It establishes a sociotechnical platform for peer-to-peer connection and knowledge sharing to sustainably enable community-based capacity-building.

The aim is to create a methodology and service, which will serve as the structure for initiating mutual skills development globally, regionally, and locally. An interactive, online platform, backed by a database, will enable wikimedians to publish information about themselves, their affiliates, and informal groups. They will also be able to conduct searches, access information and to connect with each other in a way that reflects the Wiki's spirit and the Wikimedia Movement Strategy.

The Capacity Exchange (CapX) is available in Toolforge at https://capacity-exchange.toolforge.org

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3
- Django 4.2.5
- MySQL

### Installation

1. Clone the repository:

   ```bash
   https://github.com/WikiMovimentoBrasil/capx-dev.git

2. Navigate to the project directory:

   ```bash
   cd capx-dev

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv

4. Activate the virtual environment:
    * On Windows:
   ```bash
   venv\Scripts\activate
   ```
    * On macOS and Linux:
   ```bash
   source venv/bin/activate

5. Install project dependencies:
   ```bash
   pip install -r requirements.txt

6. Create the database and apply migrations:
   ```bash
   python manage.py migrate
   
7. Create a superuser to have full control over the database:
   ``` bash
   python manage.py createsuperuser

8. Install initial data:
   ``` bash
   python manage.py loaddata fixtures/initial_data.json
   python manage.py loaddata users/fixtures/region.json
   python manage.py loaddata users/fixtures/language.json
   python manage.py loaddata users/fixtures/organizationType.json
      python manage.py loaddata users/fixtures/organization.json
   

9. Start the development server:
   ```bash
    python manage.py runserver

You should now be able to access the project at http://localhost:8000/ in your web browser.

## Contributing
Contributions are welcome! To contribute to the Capacity Exchange, follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes and commit them: git commit -m 'Add some feature'
4. Push to the branch: git push origin feature/your-feature
5. Create a pull request on GitHub

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit) - see the LICENSE file for details.