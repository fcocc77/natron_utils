
def testing_log(message, fact, hoped=None, error=None):
    error = 0
    if hoped:
        if fact == hoped:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( testing: ' + str(fact) + ' y deberia ser: ' + str(hoped) + ' )'
            error = 1
    else:
        if fact:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( ' + error + ' )'
            error = 1

    return error


def slide_testing_log(message, error):
    return testing_log(message, False if error else True,
                       error='Nodos con error: ' + error)
