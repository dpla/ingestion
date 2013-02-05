from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json


def split_name(name):
    return name.split(".")


def find_element(data, name):
    el = data
    for n in split_name(name):
        el = el[n]
    return el


def convert_data(value, dict_name):
    """
    Converts given data using provided dict name.
    """
    d = globals()[dict_name]
    result = None

    if isinstance(value, basestring):
        logger.debug("Changing value of ['{0}':'{1}'] to {2}".
                format(input_field, value, d[value]))
        result = d[value]

    if isinstance(value, list):
        msg = "Changing each value of array ['{0}':'{1}'] to array of values."
        logger.debug(msg.format(input_field, value))
        result = []
        for v in value:
            if v in d:
                logger.debug("Changing value of '{0}' to {1}".format(v, d[v]))
                result.append(d[v])
            else:
                logger.debug("Not changing value of '{0}', didn't find in {1}".
                        format(v, substitution))
                result.append(v)

    return result


@simple_service('POST', 'http://purl.org/la/dp/lookup',
    'lookup', 'application/json')
def lookup(body, ctype, input_field, output_field, substitution):
    """
    Performs simple lookup.
    """


    logger.debug("BODY  : [%s]" % body)
    logger.debug("INPUT : [%s]" % input_field)
    logger.debug("OUTPUT: [%s]" % output_field)

    LOG_JSON_ON_ERROR = True

    def log_json():
        if LOG_JSON_ON_ERROR:
            logger.debug(body)

    data = {}
    try:
        data = json.loads(body)
    except Exception as e:
        msg = "Bad JSON: " + e.args[0]
        logger.error(msg)
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return msg

    x = find_element(data, input_field)
    logger.debug(x)

    if not output_field:
        msg = "There is not provided output field name."
        logger.error(msg)
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return msg

    key = substitution.upper()
    if not key in globals():
        msg = "Missing substitution dictionary"
        logger.error(msg)
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return msg

    if not input_field in data:
        logger.error("Missing input key in provided JSON.")
        return json.dumps(data)

    d = globals()[key]
    value = data[input_field]

    if isinstance(value, basestring):
        logger.debug("Changing value of ['{0}':'{1}'] to {2}".
                format(input_field, value, d[value]))
        data[output_field] = d[value]

    if isinstance(value, list):
        msg = "Changing each value of array ['{0}':'{1}'] to array of values."
        logger.debug(msg.format(input_field, value))
        outlist = []
        for v in value:
            if v in d:
                logger.debug("Changing value of '{0}' to {1}".format(v, d[v]))
                outlist.append(d[v])
            else:
                logger.debug("Not changing value of '{0}', didn't find in {1}".
                        format(v, substitution))
                outlist.append(v)

        data[output_field] = outlist

    return json.dumps(data)


TEST_SUBSTITUTE = {
    "aaa": "AAA",
    "bbb": "BBB",
    "ccc": "CCC",
    "ddd": "DDD",
}
