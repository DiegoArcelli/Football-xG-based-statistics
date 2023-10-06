# Football xG based statistics
An easy to use Python program which allows to compute various statistics about football games based on xG and xGoT.

## How the program works
The program receives as input the URL of a FBref match report and it extracts from the page the information about expected goals (xG) and expected goals on target (xGoT) of every shot taken by the two teams during the game. 

After that the program will simulate the game many times based on xG or xGoT and it will use the results of the simulations to determine:
- The expected points (xPts) of the two teams for that game
- The probability of the two teams to win, lose or draw the game
- The probability distribution of the results of the game 
- The probability distribution of the goals difference between the two teams

The program will also compute the xG or xGoT timeline of the two teams.

## How to install the program
To install the program using a Python virtual environment first clone the repository using the command:
```
git clone https://github.com/DiegoArcelli/Football-xG-based-statistics.git
```

Then create a virtual environment using the command:
```
python -m venv .env
```

and activate the environment with the command
```
source .env/bin/activate
```
After that install the requirements using the command:
```
pip install -r requirements.txt
```

## How to run the program
Once the program is installed you can run it using the `main.py` file, by passing the following command line arguments:
- `--url`: the URL of the FBref match report of the desidred game 
- `--reference_stat`: the game statistic to use in order to compute the simulations of the game. The two admissible values are 'xg' and 'xgot'
- `--iterations`: the number of simulations of the game to perform using the reference statistic
- `--plots`: flag argument which can be used to enable the visualization of the plots

For instance to compute the statistic based on xG and the plots of the Inter vs Milan derby of the 16/19/2023, you can run the following command:

```
python main.py --reference_stat xg --iterations 1000 --plots
 --url https://fbref.com/it/partite/10a39d69/Derby-della-Madonnina-Internazionale-Milan-16-Settembre-2023-Serie-A 
```


## Warning 
The program works by scraping the FBref website, so if in the future the structure of the website gets updated the program might not work anymore.
