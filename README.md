# Object-Oriented Micromouse Controller (oop-micromouse)

[//]: # (Add build status) 

A work-in-progress, object-oriented refactor of micromouse 
code previously written by me for a university project.

## Table of Contents
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)


## Background
Micromouse was one of my favourite university projects and the only 
group project for which I wrote almost the entirety of the code. I 
decided to reflect on the code, see what could have been done 
differently, and adapt the 
controller to a more realistic, less deterministic simulation 
environment. This could involve bayesian filters, continuous 
feedback control, occupancy grid mapping, etc. 
However, to implement these changes I needed code that was 
more modular and less brittle than the 
procedural style of the original program. Conveniently, I was also
interested in improving my Object-Oriented Programming,
software design and architecture skills. 

AI use:
While LLMs are increasingly being used as programming tools, overuse 
would be detrimental to the 
educational purpose of this project. A Gemini chatbot is used 
sparingly to review and critique code, 
clarify uncertainty, and assist with Unittest coverage. 

## Install

* Developed using Python 3.12.
* This project requires an installation of 
[Webots simulator](https://cyberbotics.com/doc/guide/installing-webots)

Download or clone the project:

```bash
git clone https://github.com/Frichy-0/oop-micromouse
```
From the shell navigate to the controller directory:
```bash
cd <path-to-project-directory>/controllers/oop_controller
```
Activate the virtual environment and install dependencies:
* **Linux / MacOS:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

Create a file to point Webots to the correct interpreter:
* **Linux / MacOS:**
  ```bash
  echo -e "[python]\nCOMMAND = $(pwd)/venv/bin/python" > runtime.ini
  ```
* **Windows (PowerShell):**
  ```powershell
  "[python]`nCOMMAND = <path-to-project-directory>\oop-micromouse\controllers\oop_controller\venv\Scripts\python.exe" | Out-File -FilePath runtime.ini -Encoding utf8
  ``` 

## Usage

Open Webots and go to File > Open World.

Navigate to maze_solver_project/Worlds/maze.wbt and select Open.

The 3D window should display a simple maze environment and E-puck 
robot. 

In the [Scene Tree](https://cyberbotics.com/doc/guide/the-scene-tree)
open the E-puck "e-puck" node and select "controller".

Go to Select > oop_controller > OK.

You should now be able to run the simulation. 


## Maintainer

[@Frichy-0](https://github.com/Frichy-0)

## Contributing

No contributions, code is purely for my own enjoyment and 
education.


