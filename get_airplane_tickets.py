import json
import pprint
import requests

def getTickets(airplane_destination):
    pp = pprint.PrettyPrinter(indent=4)
    newSession = requests.session()
    destinationResponse = newSession.get("http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/" +
                               "RU/USD/en-GB?query=" + airplane_destination + "&apiKey=ha129292138013702875479911846997",
                               headers = {'Accept': 'application/json'})
    jsonDestinationResponse = json.loads(destinationResponse.text)
    destinations = []
    for place in jsonDestinationResponse['Places']:
        destinations += [place['PlaceId']]
    quotes = []
    for destination in destinations:
        # pp.pprint("DESTINATION: " + destination)
        ticketResponse = newSession.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/" +
                                   "ES/USD/en-GB/BCN-sky/" + destination +
                                   "/anytime/?apiKey=ha129292138013702875479911846997")
        jsonTicketResponse = json.loads(ticketResponse.text)
        # pp.pprint(jsonTicketResponse)
        url = "http://partners.api.skyscanner.net/apiservices/referral/v1.0/ES/USD/en-GB/BCN-sky/" + \
              destination + "/anytime/?apiKey=ha12929213801370"
        for quote in jsonTicketResponse['Quotes']:
            quote['Url'] = url
            quotes += [quote]
    quoteBest = sorted(quotes, key=lambda quote: quote['MinPrice'])[0]
    pp.pprint(quoteBest)

    return quoteBest

if __name__ == "__main__":
    quoteBest = getTickets("Moscow")


