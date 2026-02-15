Assignment Problem Solver (Hungarian Method)

A Python application that solves the Assignment Problem using the König Algorithm, also known as the Hungarian Method.

The program computes the optimal assignment that minimizes the total cost and provides a graphical interface for matrix input.

Project Overview

The Assignment Problem is a classical optimization problem in operations research.
This application:

Accepts an n × n cost matrix

Applies the Hungarian Method

Finds the optimal assignment

Computes the minimum total cost

Displays the result in a graphical interface

Technologies Used

Python 3

NumPy

CustomTkinter

Project Structure
assignment-problem-solver/
│
├── affectation-konig.py
├── requirements.txt
└── README.md


affectation-konig.py: contains the Hungarian algorithm implementation, graphical user interface, and application logic.

requirements.txt: lists required Python dependencies.

README.md: project documentation.

Installation

Clone the repository:

git clone https://github.com/your-username/assignment-problem-solver.git
cd assignment-problem-solver


Create a virtual environment (recommended):

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

Run the Application
python affectation-konig.py


Make sure Python 3 is installed on your system.

Academic Context

This project was developed as part of engineering studies in optimization and algorithm design. It demonstrates practical implementation of combinatorial optimization techniques.
