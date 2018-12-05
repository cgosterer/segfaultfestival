def tryAction(func):
    def try_wrapper(*args):
        try:
            return func(args)
        except:
            print("Connection Error")
            return False
    return try_wrapper
