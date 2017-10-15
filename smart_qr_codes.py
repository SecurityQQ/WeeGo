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

    url = json.loads(s.content.decode('utf8')).get('value')[0].get('contentUrl')

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=suffix) as fp:
        fp.write(r.get(url).content)
        path = fp.name
        print(path)
        ver, ecl, qr_name = myqr.run("https://www.facebook.com/Cia-El-ladr%C3%B3n-de-patinetes-Teatro-167506496609941/", picture=path, save_name=save_name)


smart_qr_code_by_name('theatre', suffix=".png", save_name='theatre.png')
# smart_qr_code_by_name('cinema', suffix=".png", save_name='cinema.png')