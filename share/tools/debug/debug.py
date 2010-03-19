import sys
import os.path

sys.argv.pop()
sys.path.append(os.path.abspath(os.path.join('..', '..', '..')))

a = __import__('main').Application()
