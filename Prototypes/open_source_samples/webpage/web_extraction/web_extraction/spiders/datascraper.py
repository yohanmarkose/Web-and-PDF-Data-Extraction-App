from pathlib import Path

import scrapy


class WikiSpider(scrapy.Spider):
    name = "datascraper"

    def start_requests(self):
        urls = ["https://en.wikipedia.org/wiki/Automotive_industry_in_China", "https://en.wikipedia.org/wiki/Large_language_model"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        main_title = response.css("main.mw-body h1 ::text").get()
        # body_content = response.css("div .mw-body-content".get())
        yield {"main_title": main_title}

        sub_titles = response.xpath("//div[@class='mw-body-content']//h2")
        
        for title in sub_titles:
            flag = False
            images, text_content, tables, links = [], [], [], []

            title_text = title.css("::text").get()  # Text if sub title
            div_tag = title.xpath("..")[0]  # Parent div tag
            following_tags = div_tag.xpath('following-sibling::*')
            for tag_element in following_tags: # Iterating through all the following tags to get the contents related to the heading
                if tag_element.root.tag == 'div' and tag_element.css('::attr(class)').get() == 'mw-heading mw-heading2':  # Condition to break the loop when the next heading is reached
                    flag = True
                    break
                elif tag_element.root.tag == 'figure':
                    images.append(tag_element.css("a img::attr(src)").get())
                elif tag_element.root.tag == 'p':
                    text_content.append(tag_element.css("::text").getall())
                elif tag_element.root.tag == 'table' and tag_element.css('::attr(class)').get() == "wikitable":
                    tables.append(self.extract_table_data(tag_element))
                
            yield {
            "title": title_text,
            "text_content": self.process_text_content(text_content),
            "images": images,
            "table": tables
            }
            if flag == True:
                continue


    def extract_table_data(self, table_tag):
        tbody = table_tag.css("tbody")
        table_dict = {}
        header = []
        for val in tbody.xpath("tr")[0].xpath("th"): # Getting the headers
            text = val.css("::text").get().strip()
            header.append(text)
            table_dict[text] = []  # Initializing the header as key to dict and value as a list

        for col in range(len(header)-1): # Getting header data
            for row in range(1, len(tbody.xpath("tr"))):
                table_dict[header[col+1]].append(tbody.xpath("tr")[row].xpath("td")[col].css("::text").get().strip())

        for row in range(1, len(tbody.xpath("tr"))):  # Getting index data
            table_dict[header[0]].append(tbody.xpath("tr")[row].xpath("th")[0].css("::text").get().strip())

        return table_dict
        


    def process_text_content(self, data):
        flattened_sentence = "".join([item for sublist in data for item in (sublist if isinstance(sublist, list) else [sublist])])
        flattened_sentence = " ".join(flattened_sentence.split())
        return flattened_sentence
                


        
        
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")