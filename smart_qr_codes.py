from MyQR import myqr


import requests as r


def smart_qr_code_by_name(name, suffix=".png", save_name=None):
    if save_name is None:
        save_name = name + suffix

    if 'icon' not in name:
        name = name + ' icon'


    s = r.get("https://api.cognitive.microsoft.com/bing/v7.0/images/search/?q={}".format(name),
              headers={"Ocp-Apim-Subscription-Key": "63b3ee16a46847e0be92920dd1409024"})

    from pprint import pprint
    import json

    url = json.loads(s.content).get('value')[0].get('contentUrl')

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=suffix) as fp:
        fp.write(r.get(url).content)
        path = fp.name
        print(path)
        ver, ecl, qr_name = myqr.run("http://natribu.org", picture=path, save_name=save_name)


smart_qr_code_by_name('cross', suffix=".png", save_name='medicine.png')