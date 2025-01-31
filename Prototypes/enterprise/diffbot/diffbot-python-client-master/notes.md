## Diffbot

- Reference : https://docs.diffbot.com/reference/extract-introduction

- Credits : https://docs.diffbot.com/docs/how-credits-work

- Web UI testdrive : https://www.diffbot.com/products/extract/testdrive/

- Referenced Gitrepo : https://github.com/diffbot/diffbot-python-client.git


Diffbot Extract API is a webpages data scraping product with pre-set categories of specific APIs that categorize using computer vision to "read" a web page, categorize it into a standard page type, and extract its contents based on a standard schema.

They provide a standard Analyze API, which categorizes the page into an appropriate type. The classification are article, image, video, discussion, event, or list - using these specific classes further detailed datasets can be configured to extract. They also offer custom API where user can create entirely new custom extractions by defining rules, all provided in their documentaion : https://docs.diffbot.com/reference/extract-introduction.

They also provide bulk extraction using Extract API which can be scheduled or automated. Each url that needs to be scaped needs to be provided in a job. Thus, if the use case requirement specifies scraping data from thousands of websites rather than creating a thousand API call for varied HTML structures a bulk job can be configured to collect data.


# Pricing analysis :

| Product Type\\Plan                                                     | Free                   | Startup            | Plus                            |
| ---------------------------------------------------------------------- | ---------------------- | ------------------ | ------------------------------- |
| All APIs                                                               | 5 Calls Per Minute     | 5 Calls Per Second | 25 Calls Per Second             |
| [Extract API](https://docs.diffbot.com/reference/extract-introduction) | 10,000 Calls Per Month | None               | None                            |
| Crawl / Bulk Extract API                                               | n/a                    | n/a                | 25 Active Jobs, 1000 Total Jobs |

With the free tier account for a new user is provided with 10,000 credits per month at no cost.
A small scale requirement can easily handled by the same.

Additionaly previewing the provided costing plans gives more leverage for bulk extarction which is access able in the paid plans only with increased credits and rate limits.

Thus for reference if we wanna take 10000 webpages (1 credit per webpage) which is also the limit for a free account one  would :

For a free account - 
10000 webpages / 5 calls per min = 2000 minutes which is around 33.33 hours at 0$ 

For a Startup Plan -
10000 webpages / (5 * 60) calls per min = 33.33 minutes costing around $299
Additional with no limitations on further calls but the same also doesn't include bulk extarction feature.

For a Plus Plan -
10000 webpages / (25 * 60) calls per min = 6.67 mins at $899 costing plan,
With no limitations on further calls and bulk bulk extarction feature jobs to configure larger jobs.


[Reference](https://blog.diffbot.com/announcing-the-diffbot-free-plan/)