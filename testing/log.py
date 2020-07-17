
def testing_log(message, fact, hoped=None, error_info=None):
    error = 0
    if not hoped == None:
        if fact == hoped:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( testing: ' + str(fact) + ' y deberia ser: ' + str(hoped) + ' )'
            error = 1
    else:
        if fact:
            print '- ' + message + ': OK'
        else:
            print '- ' + message + ': ERROR ( ' + error_info + ' )'
            error = 1

    return error


def slide_testing_log(message, error):
    return testing_log(message, False if error else True,
                       error_info='Nodos con error: ' + error)
