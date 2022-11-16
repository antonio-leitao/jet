import sys 
sys.path.append("/Users/antonio/Documents/Projects/JET_JetTesting/jet")

from jet.runner import Runner
from jet.doctor import doctor



if __name__ == "__main__":
    doctor(default_directory="/")