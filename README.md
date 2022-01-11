# Chess tournament manager

***
This project is part of the python developer course on [Openclassrooms](http:/openclassrooms.com).

The goal is to create a python script that allows for the creation and management of a chess tournament.

Code should follow the MVC architecture.

## **Setup**

***
</br>

### **Setting up the code for execution**

</br>
A Python installation is required.
> The code was written using python 3.9.7. User discretion is advised when using an earlier version.

Assuming a git installation, clone the repository using:

    $git clone git clone https://github.com/Chfrlt/P4_chess_tournament

Creating a virtual environment is recommended.

> Following instructions are the ones recommanded for python 3.6 or greater. If your python installation is an earlier version, please consult the associated documentation.

To create a virtual environnement use:

    $python -m venv <env_name>

To activate it:

* On Windows:

        $env_name/Script/activate

* On Linux/Mac:

        $source env_name/bin/activate

To install the required packages:

    $pip install -r requirements.txt

### **Generating a flake8 report**

</br>

The root folder by default contains a flake8 report.\
The report result can be found in it under *index.html*

To generate a new report, use:
> flake8 chess_tournament --format=html --htmldir=<new_report_name>
>> Note: chess_tournament is the default name of the folder containing the code. If changed, please update the command fittingly.

</br>

## **Usage**

***

Execute the script using:

    $python app.py

If it doesn't exist yet, the execution will create a database.
Tournaments and players datas will be stored inside.

Executing the script will lead to the menus. Navigation is made by input into the console.

### **Menus options & navigation**

***
</br>

* [Main menu](#Main-Menu)
  * Tournament creation & selection.
* [Player Menu](#Player-Menu)
  * Create, delete, update & manage player(s) in database.
* [Tournament Menu](#Tournament-Menu)
  * Manage a tournament. Start & end rounds, edit game(s) in current round.
* [Player Management Menu](Player-Management-Menu)
  * Manage player(s) in tournament. Add & remove players from tournament, see rankings, create new player(s).

#### **Main menu**

1) Create tournament
    * Allows for tournament creation.\
        The script does support multiple tournaments existing at once.
2) Select tournament
    * Allows the user to select the tournament they wish to manage.
3) Tournament menu
    * Access to the [Tournament Menu](#Tournament-Menu).
4) Player menu
    * Access to the [Player Menu](#Player-Menu).
5) Delete tournament(s)
    * Allows the user to delete **all** or a single tournament in the database.
6) Exit
    * Exit from python.
</br></br>

#### **Player Menu**

1) Show all players
    * Display the stored players in database.
2) Show all players by name
    * Display the stored players in database sorted by lastname.
3) Show all players by elo
    * Display the stored players in database sorted by elo (From higher to lower).
4) Create player(s)
    * Allows user to create one or multiple players and stores them in database.
        > Note: If the user has selected a tournament to manage prior to using this option, the user will have the option to add the created players to it.
5) Update a player
    * Allow user to select a player and update one of its value.
        > Note: If the player is registered in any tournament, the value will also update there.
    Therefore, updating a player prior to a tournament completion should be done with care.
6) Delete player(s) in database
    * Allows the user to delete **all** or a single player in the database.
        > Note: When deleting players, if the player to delete is registered in any tournament that has already started (a round is in progress), the player will not be deleted from it.
7) Main menu
    * Go back to the [Main menu](#Main-Menu).
8) Exit
    * Exit from python.
</br></br>

#### **Tournament Menu**

1) Show games in round
   * Display games for the current round.
2) Edit a game in round
   * Allow the user to edit a game result from the current round:\
    Set it back to non-played, draw it, or set a player to be the winner.
3) Start next round
    * Allow the user to start the next round.
        > Note: By selecting this option, the result of the round are set to stone and won't be availaible for update.
4) End round
    * Allow the user to end the current round.
        > Note: Selecting this option will lead to the update of any non-completed game.
5) Tournament's games history
    * Display the games in past and current round(s) and the associated result.
6) Player management
    * Access to the [Player Management Menu](Player-Management-Menu).
7) Main menu
    * Go back to the [Main menu](#Main-Menu).
8) Exit
    * Exit from python.
</br></br>

#### **Player Management Menu**

1) Create player(s)
    * Allows user to create one or multiple players and stores them in database with the option to add the created players to the current tournament.
        > Note: This option is a duplicate to the identicality nammed one in the [Player Menu](#Player-Menu). </br>
        > However, since access to this menu requires a tournament to be selected, the option to add the created player to the tournament will always be available.
2) Add Player to tournament
    * Allows the user to add a player from the database to the tournament.
3) Show players in tournament
    * Display players registered in the current tournament.
4) Show players in tournament by score
    * Display players registered in the current tournament by score(from higher to lower)
5) Delete a player in tournament
    * Allows the user to delete a player from the current tournament.
6) Tournament menu
    * Go back to the [Tournament Menu](#Tournament-Menu)..
7) Main menu
    * Go back to the [Main menu](#Main-Menu).
8) Exit
    * Exit from python.
