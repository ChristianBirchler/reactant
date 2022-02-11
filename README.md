# reactant
This application is meant to collect all words in function and method names of `Python` and `Java` repositories on
GitHub. For this reason I came up with the name *reactant*:

> popula**R** m**E**thod **A**nd fun**CT**ion n**A**mes o**N** gi**T**hub

![](resources/screenshot.png)

## Run *reactant* with Docker Compose
First, simply clone the repository:
```
git clone https://github.com/ChristianBirchler/reactant.git
cd reactant
```
If you use docker on a Mac, then docker compose is already installed and you can run the application with the following
command:
```
docker compose build
docker compose up -d
```
In case you do not use a Mac, then you can install docker-compose with `pip`. The command looks slightly different:
```
docker-compose build
docker-compose up -d
```
The `-d` is optional but it will deamonize the containers but if you want to have the output of the containers in your
terminal then you can leave this option flag out.

Go to your web browser on `localhost:8050` to see *reactant* visualizing in a parameterized bar chart the top words.

## Run *reactant* locally
In case you want to run the application locally it is worth to use a virtual environment. For managing virtual
environments and dependencies in `Python` I use [Poetry](https://python-poetry.org/). You should go to the website and
install it.

### Install Dependendcies
```
git clone https://github.com/ChristianBirchler/reactant.git

cd reactant/miner
poetry install

cd ../visualizer
poetry install
```

### Run *reactant*
```
cd visualizer
poetry run python src/visualizer/main.py
```

```
cd miner
poetry run python src/miner/main.py
```

Go to your web browser on `localhost:8050` to see *reactant* visualizing in a parameterized bar chart the top words.

