import sys
import os.path

sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', '..')))

a = __import__('main').Application()
