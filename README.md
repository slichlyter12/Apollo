# Pull
A project to help automate the TA grading of Oregon State University's CS 362 course.

## Requirements:
- Python 3.6
- gitpython

## Installation:
1. Make sure you have the above requirements (I use [Anaconda]('https://www.anaconda.com/download/') to help maintain my Python installations)
2. Change shebang to your Python installation

## Usage:
- Maintain a `.csv` file (I named mine `usernames.csv`) that has the following headers:
	- `firstname`
	- `lastname`
	- `gid`: GitHub ID
	- `osuid`: OSU username (`osuid@oregonstate.edu`)
	- `url`: The URL of their repository on GitHub
	
- `./pull.py`: pulls (or clones if necessary the assignment branch of their repo)
	- Optional command line arguments:
		- `-a`: assignment number (defaults to `1`)
		- `-i`: input file (defaults to `usernames.csv`)
- `./build.py`: builds the dominion in both `projects/` and main `dominion/` directories

## Feedback:
Please provide feedback by creating an issue above. If you would like to implement a fix then don't hesitate to make a pull request! Happy coding!