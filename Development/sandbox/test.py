import subprocess

if __name__ == "__main__":
    a = 10
    b = 30
    c = "{0} ".format(a) + "{0}".format(b)
    print("hi " + c)
    script = subprocess.Popen(["./test.sh"], stdin=subprocess.PIPE)
    d = bytes(c, 'utf-8')
    result = script.communicate(d)

        # subprocess.call(["mkdir", "my_directory"])
    # p1 = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
    # pwd = p1.communicate()

    # print(pwd)

    # time.sleep(10)