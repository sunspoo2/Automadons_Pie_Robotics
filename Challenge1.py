stops = {"SL": "San Leandro", "COL": "Coliseum", "FR":  "Fruitvale", "LM": "Lake Merrit", "OAK": "Oakland", "RICH": "Richmond", "EC": "El Cerrito", "NB": "North Berkeley", "DB": "Downtown Berkeley", "ASH": "Ashby", "WC": "Walnut Creek", "ORI": "Orinda", "LAF": "Lafayette", "PH": "Pleasant Hill", "MAC": "MacArthur", "PIT": "Pittsburg"}
stop1 = [
    ["SL", "COL", "FR", "LM", "OAK"],
    ["RICH", "EC", "NB", "DB", "ASH"],
    ["WC", "ORI", "LAF", "WC", "PH"],
    ["MAC", "ASH", "DB", "NB", "EC"]
    ]
stop2 = [
    ["OAK", "DB", "NB"],
    ["WC", "ORI", "LAF", "WC", "PH"],
    ["MAC", "ASH", "DB", "NB", "EC"],
    ["OAK", "RICH", "ORI", "NB", "PIT"]
    ]

def berkeley_bound(where):
    found=[]
    for section in where:
        n=0
        for bart in section:
            if bart=='NB' or bart=='DB':
                found.append(n)
                break
            else:
                n+=1
        else:
            found.append("lost")       
    return found
print(berkeley_bound(stop1))
print(berkeley_bound(stop2))


