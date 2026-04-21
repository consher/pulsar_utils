import requests
import json
from bs4 import BeautifulSoup
import os

psrs = ['J0030+0451','J0218+4232','J0437−4715','J0613−0200','J0621+1002','J0711−6830','J0751+1807','J0900−3144','J1012+5307','J1022+1001','J1024−0719','J1045−4509','J1455−3330','J1600−3053','J1603−7202','J1640+2224','J1643−1224','J1713+0747','J1730−2304','J1732−5049']

class psrcat:
    def __init__(self, cache, version="2.7.0"):
        self.version = version
        self.cache = cache + f"{version}/"

    # get ephemeris either from ATNF or cache
    def get(self, psr, force_rewrite = False):
        # check cache
        if os.path.exists(self.cache + psr + "_ephem.json") and force_rewrite == False:
            with open(self.cache + psr + "_ephem.json", 'r') as fp:
                ephem = json.load(fp)
            return ephem
        
        # otherwise pull from the ANTF
        else:
            if "+" in psr:
                psr = psr.split("+")
                url = f"https://www.atnf.csiro.au/research/pulsar/psrcat/proc_form.php?version={self.version}&startUserDefined=true&sort_attr=jname&sort_order=asc&condition=&coords_unit=raj%2Fdecj&radius=&coords_1=&coords_2=&pulsar_names={psr[0]}%2B{psr[1]}&ephemeris=long&ephemeris_submit=&style=long+with+errors&no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&y_scale=linear&state=query"

            else:
                psr = psr.split("\u2212")
                url = f"https://www.atnf.csiro.au/research/pulsar/psrcat/proc_form.php?version={self.version}&startUserDefined=true&sort_attr=jname&sort_order=asc&condition=&coords_unit=raj%2Fdecj&radius=&coords_1=&coords_2=&pulsar_names={psr[0]}%2D{psr[1]}&ephemeris=long&ephemeris_submit=&style=long+with+errors&no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&y_scale=linear&state=query"

            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')

            content = soup.find('pre').string.split("\n")
            
            return {i.split()[0]:i.split()[1] for i in content[1:-1]}
    
    def update_cache():
        # to be written
        pass

    def write(self, ephem, dir=None):
        output = ephem["PSRJ"] + "_ephem.json"

        # write output to cache
        with open(self.cache+output, 'w+') as fp:
            json.dump(ephem, fp)

        # if desired copy output to given directory
        if dir != None:
            with open(dir+output, 'w+') as fp:
                json.dump(ephem, fp)


    def read(self, dir, psr):
        ephemfile = dir + psr + "_ephem.json"

        if os.path.exists(ephemfile):
            with open(ephemfile, 'r') as fp:
                ephem = json.load(fp)
            return ephem
        
        else:
            raise(f"Ephemeris at {dir}{psr} does not exist, use psrcat.get() instead!")