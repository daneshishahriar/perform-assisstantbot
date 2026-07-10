from datetime import date


def user_data_template():

    return {
        "name": None,
        "phone": None,
        "grade": None,
        "field": None,
        "step": None
    }



def today():

    return date.today()