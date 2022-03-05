import requests
import json


def getRawData(word: str, lang: str) -> str:
    parameters = {
        "page": word,
        "prop": "wikitext",
    }

    response = requests.get("https://"+lang+".wiktionary.org/w/api.php?action=parse&format=json", params=parameters)
    #status_code = response.status_code # -0
    data = json.loads(json.dumps(response.json()["parse"]["wikitext"]["*"]))

    #print(data) # -0
    return data

def getReadableData(word: str, lang: str) -> str:
    """
    Makes data readable
    example: {{inh|en|enm|somthing}} => Middle English somthing
    """
    data = getRawData(word,lang)
    # TODO: make it

    return data

def tojson(data: str) -> json:
    """
    Convert the string data to json format for easy access
    """
    stop = False
    counter = 2  # counts number of = used, to determine indentation 
    curlyend = 0 # counts number of curly brackets ( } ) to be added at the end

    while(not stop):
        numeq = [(data[data.find("==")+i]) for i in range(counter+1)].count("=") # number of equal signs ( = )
        if (numeq == 0):
            stop = True

        elif (numeq == counter):
            # edit title (add   ," ":   outside the text})
            data = data.replace("="*counter, ",\"", 1)
            if (counter == 2): # if at the begining of the data
                index = data.find(",") # actual beginning index
                data = "{" + data[index+1:]
            sindex = data.find("="*counter)+2 # subdata index (start)
            data = data.replace("="*counter, "\": ", 1) 
            # edit subdata (add   " "   outside the text)
            if (data[sindex+1] != "="):
                data = data[:sindex] + "\"" + data[sindex:]
                sindex = data.find("==") # subdata index (end)
                data = data[:sindex] + "\"" + data[sindex:]

        elif (numeq > counter): 
            if (numeq > curlyend):
                curlyend = numeq
            counter = numeq
            # edit title (add   " ":{   outside the text})
            data = data.replace("="*counter, "\"{", 1)
            sindex = data.find("="*counter)+2 # subdata index (start)
            data = data.replace("="*counter, "\": ", 1) 
            # edit subdata (add   " "   outside the text)
            if (data[sindex+1] != "="):
                data = data[:sindex] + "\"" + data[sindex:]
                sindex = data.find("==") # subdata index (end)
                data = data[:sindex] + "\"" + data[sindex:]
            
        elif (numeq < counter):
            counter = numeq
            # edit title (add   }," ":   outside the text})
            data = data.replace("="*counter, "},\"", 1)
            sindex = data.find("="*counter)+2 # subdata index (start)
            data = data.replace("="*counter, "\": ", 1) 
            # edit subdata (add   " "   outside the text)
            if (data[sindex+1] != "="):
                data = data[:sindex] + "\"" + data[sindex:]
                sindex = data.find("==") # subdata index (end)
                data = data[:sindex] + "\"" + data[sindex:]

    # Add missing curly brackets at the end
    data += "}"*curlyend

    # TODO: fix converison to json (issue at "json.loads(data)") ########
    # there's probably an issue on the formatting above :(

    # text_file = open("sample.txt", "w") # -0
    # text_file.write(data)               # -0
    # text_file.close()                   # -0

    #json.loads(data) # Convert string to dictionary
    data = json.dumps(data)

    with open("test.json", "w") as outfile: # -0
        json.dump(data, outfile)

    #####################################################################
            
    return data

def getData(word: str, lang: str) -> json:
    data = tojson(getReadableData(word,lang))
    print(data) # -0
    return data


getData("something", "en")

