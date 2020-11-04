#!/usr/bin/env python3
import requests
import json

URL = "https://eos.hyperion.eosrio.io/v2/history/get_actions?limit=1&account=associapress&filter=associapress%3Aelection&sort=desc"
SOURCE_URL = "https://everipedia.org/oraqle/ap"
STATE_MAP = "state_map.json"


def fetch_url():
    req = requests.get(URL)
    if req.status_code > 200:
        print("Error fetching {}, status code {}".format(URL, req.status_code))
        exit(1)
    return req.json()


def parse(do_file=False):
    with open(STATE_MAP, "r") as sm:
        state_map = json.load(sm)
    if not do_file:
        results = fetch_url()
    else:
        results = fetch_file()

    if not results:
        print("Error fetching result json")
        exit(1)

    state_results = []
    t = 0
    b = 0
    none = 0
    not_counted = []
    for act in results["actions"]:
        data = act["act"]["data"]["data"]
        state_results.append(json.loads(data))

    for state_res in state_results:
        for k, _ in state_res.items():
            if k == "US":
                continue
            pres = state_res[k]["president"]
            if pres == "Biden":
                b += state_map[k]
            elif pres == "Trump":
                t += state_map[k]
            else:
                none += state_map[k]
                not_counted.append("{}: {}".format(k, state_map[k]))

    print(
        "Current associated press US presidential electoral vote count:\nBiden: {}\nTrump: {}\nElectoral Votes left: {}\nState/Electoral votes uncounted: {}\nsource {}".format(
            b, t, none, ",".join(not_counted), SOURCE_URL
        )
    )


def main():
    parse()


if __name__ == "__main__":
    main()
