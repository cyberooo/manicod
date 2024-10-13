#!/usr/bin/env python

from serpapi.google_search import GoogleSearch

class GoogleAPIModel:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.serp_apikey = "REPLACE WITH YOUR OWN KEY!"
        print("SerpApi apikey: ****{}".format(self.serp_apikey[-4:]))

    def serpapi_google_search(self, query: str, lang="en", num_responses=3, google_domain="google.com", gl_country="us", tbs=None):

        search_results = []
        query = query.replace('"', '')
        if lang.lower() == "cn":
            lang = "zh-cn"

        # Set parameters
        params = {
            "api_key": self.serp_apikey,
            "engine": "google",
            "q": query,
            "google_domain": google_domain,
            "gl": gl_country,
            "hl": lang.lower(),
        }
        if tbs:
            params['tbs'] = tbs
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
        # Fail to make API request- to check
        except Exception as e:
            if self.verbose:
                print("[ERR] Serpapi Google Search failed. Exception caught: {}".format(e))
            results = None
        if results:
            if "error" in results:
                if self.verbose:
                    print("[ERR] Error returned: {}".format(results.get("error")))
            else:
                # Get search information stats (if any)
                search_info = results.get("search_information")
                if search_info:
                    if self.verbose:
                        print("[INFO] Total number of results returned: {}. Time taken: {}s.".format(search_info.get("total_results"),
                                                                                          search_info.get("time_taken_displayed")))
                # Get main results
                if results.get("organic_results"):
                    search_results = results.get("organic_results")
                    if self.verbose:
                        print("[INFO] Number of organic results returned: {}.".format(len(search_results)))
                else:
                    if self.verbose:
                        print("[INFO] No <organic_results> in dict. To check. Returned dict: {}".format(results))
        else:
            if self.verbose:
                print("[INFO] No results returned from SerpAPI Google Search. See previous logs...")
        if self.verbose:
            if num_responses > len(search_results):
                print("[INFO] The number of response has been changed from {} to {} due to insufficient number of responses received.".format(num_responses, len(search_results)))
                num_responses = len(search_results)
            # print("--- END SerpAPI Google Search ---")
            print("[INFO] ", end="")
            print([item['title'] for item in search_results][:num_responses])
        
        search_titles = []
        search_links = []
        search_snippets = []
        search_dates = []
        for item in search_results[:num_responses]:
            search_titles.append(item['title'])
            search_links.append(item['link'])

            if 'snippet' in item.keys():
                search_snippets.append(item['snippet'])
            else:
                search_snippets.append("")
            
            if 'date' in item.keys():
                search_dates.append(item['date'])
            else:
                search_dates.append("")
       
        return search_links, search_titles, search_snippets, search_dates 
    

if __name__ == '__main__':

    API = GoogleAPIModel(verbose=True)
    query = "Taiwan wakes up to aftermath of worst earthquake in 25 years."
    ans = API.serpapi_google_search(query)
    print(ans)