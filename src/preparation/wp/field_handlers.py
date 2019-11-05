def text(field):
    return field.text


def text_to_int(field):
    return int(field.text)


def attrib_dict_plus_text(field):
    response = {'text': field.text}
    for k, v in field.attrib.iteritems():
        response[k] = v
    return response


def postmeta_pair(field):
    key, value = field.getchildren()
    return (key.text, value.text)
