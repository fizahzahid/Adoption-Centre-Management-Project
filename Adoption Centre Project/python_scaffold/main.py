import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from python_scaffold.model.AdoptionCentre import AdoptionCentre
from python_scaffold.LoginView import LoginView

def main():
    adoption_centre = AdoptionCentre()
    LoginView(adoption_centre)

if __name__ == "__main__":
    main()



