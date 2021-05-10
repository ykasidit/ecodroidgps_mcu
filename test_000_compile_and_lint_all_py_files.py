import os

# for pylint error messages ref, see: https://docs.pylint.org/en/1.6.0/features.html

def test():
    files = os.listdir('.')
    for f in files:
        if f.endswith(".py") and not f.startswith(".#"):
            print("TEST compile:", f)
            cmd = '''python3 -c "import ast; ast.parse(open('%s').read())"''' % f
            ret = os.system(cmd)
            assert ret == 0
            
            print("TEST pylint:", f)
            cmd = '''pylint --disable=C,W0611,W0612,W0703,R1705,R0915,R0912,R0914,W0613 '%s' ''' % f
            ret = os.system(cmd)
            assert ret == 0
    
    
if __name__ == '__main__':
    test()
