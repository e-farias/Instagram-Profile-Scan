def validates_range_integers(ask, init, end):
    while True:
        try:
            value = int(input(ask))
            if init <= value <= end:
                return(value)
        except ValueError:
            print("Invalid value, please enter between {} and {}".format(init, end))

def features():
    print("""
        ==========    Instagram Profile Scan    ==========

        (1) Scan my profile
        (2) Scan another profile
        (0) Exit

        =============          v1.0          =============
    """)
    return validates_range_integers("Choose an option: ", 0, 2)
