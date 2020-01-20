Welcome to the CodeCrafters Redis Challenge!

In this challenge, you'll build a toy Redis clone that's capable of handling
basic commands like `PING`, `SET` and `GET`. Along the way we'll learn about
event loops, the Redis protocol and more. 

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to start the challenge.

# Usage

1. Ensure you have `python` (3.8) installed locally.
2. Run `make install`, which'll install the required Python dependencies.
3. Run `make test` to run local tests, which are located in `tests/test_main.py`
4. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.

# Passing the first stage

1. We've built a basic local testing setup for you at `tests/test_main.py`. To
   run these tests, run `make test`.
   
   You should see a failure message that looks like this: 
   
```sh
============== FAILURES =============
______ test_can_connect_to_6379 _____

    def test_can_connect_to_6379():
        with spawn_server():
            # Shouldn't throw an error
>           socket.create_connection(("localhost", 6379))

    ...
    ...
    ...

>               sock.connect(sa)
E               ConnectionRefusedError: [Errno 111] Connection refused

/usr/lib64/python3.8/socket.py:796: ConnectionRefusedError
```
   
2. Now, implement a socket in `app/main.py`
 
```diff
--- app/old.py	2020-01-20 10:29:06.254902363 +0530
+++ app/main.py	2020-01-20 10:23:36.160486553 +0530
@@ -1,3 +1,4 @@
+import socket
 import time
 
 
@@ -5,6 +6,9 @@
     # Implement your server here
     print("hey")
 
+    s = socket.create_server(("localhost", 6379))
+    s.accept()  # Wait for a new connection
+
 
 if __name__ == "__main__":
     main()
```

3. Run `make test` again, and the tests should now pass!
   
```
$ make test
pipenv run pytest tests
============================= test session starts ====================
platform linux -- Python 3.8.1, pytest-5.3.3, py-1.8.1, pluggy-0.13.1
rootdir: /redis-solution-starter-py
collected 1 item                                                                                                                                                                                                                              

tests/test_main.py .                                                                                                                                                                                                                    [100%]

============================== 1 passed in 0.13s =====================
```

4. Now it's time to submit your result to CodeCrafters! Commit your changes and
   run `git push origin master`.

# Troubleshooting

**`make install` says it can't find Python 3.8, although I have it installed**

When running `make install`, you might be prompted with something like this: 

```
Warning: Python 3.8 was not found on your system…
You can specify specific versions of Python with:
  $ pipenv --python path/to/python
```

This is because `pipenv` expects your default `python` executable's version to
be 3.8. If you've installed 3.8 elsewhere, use `pipenv --python
<path/to/your/python38> install`. For example, if you have Python 3.8
installed at `/usr/bin/python38`, then run the following: 

``` sh
pipenv --python /usr/bin/python38 install
```
