## PAC4 - Programació per a la ciència de dades


### What's PAC4
PAC4 is the final "Prova d'Avaluació Continuada" in the subject "Programació per a la ciència de dades".

This final deliverable is about creating a set of tools for managing technical information regarding soccer players 

### How to install
Optional:

    virtual env
    source venv/bin/activate
 Install:

Unzip file in project folder and install requirements

    pip install -r requirements.txt

### How to run all examples at once

    cd ./PAC4
    python3 main.py

### Modules in PAC4

- [x] **Preprocess**: Provides a set of functions to load data into dataframes and combine dataframes.
- [x] **Statistics**:
  - Basic statistics: Provides a set of functions for basic statistics and data filtering by queries
  - Bmi statistics: Provides a set of functions for bmi related calculations statistics
- [x] **Datamanagement**:
  - dictionaries: Provides a set of functions for specific dictionaries building and data cleaning
  - evolution: Provides a set of functions to follow up the temporal evolution of a given characteristic and find top players for that characteristic
  - rosters: Provides a set of functions for finding candidates for a given position (all, top players) and to generate combinations
- [x] **Other**: Small pieces of code to support main code functionalities

### Examples

- [x] **Example_1**: This example prints the information of belgium players with maximum potential
- [x] **Example_2**: This example prints the information of players goalkeepers, female, older than 28 with overall higher than 85
- [x] **Example_3**: This example creates one bar chart with the maximum BMI by country
- [x] **Example_4**: This example compares players bmi with spain population bmi and creates 2 sets of comparative pie charts.
- [x] **Example_5**: This example creates a dictionary with players info and later cleans the dictionary according to col_query information
- [x] **Example_6**: This example provides the evolution of "movement_sprint_speed" of the four best average players of this characteristic.
- [x] **Example_7**: This example calculates the best defense roster for gender male and young players, gender female and young players & senior players (male & female)

### Running examples one by one

    cd ./PAC4
    python3 example_name.py