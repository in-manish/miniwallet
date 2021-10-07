
def get_fail_msg(error_msg):
    error_msg_data = {'status': 'fail', 'data': {'error': error_msg}}
    return error_msg_data


def get_success_data(data: dict):
    return {
        'status': 'success',
        'data': data
    }
