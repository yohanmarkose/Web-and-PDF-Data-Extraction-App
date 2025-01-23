from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "datascraper"

    def start_requests(self):
        # urls = ["https://en.wikipedia.org/wiki/Large_language_model"]
        urls = ["https://en.wikipedia.org/wiki/Transformers"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        main_title = response.css("main.mw-body h1 ::text").get()
        # body_content = response.css("div .mw-body-content".get())
        body_content = response.css("div.mw-body-content")
        elements = body_content.css('p, table, img, a, chart')  # To get all the tags under the body_content in order

        sub_titles = response.xpath("//div[@class='mw-body-content']//h2")
        
        for title in sub_titles:
            images, text_content = [], []
            title_text = title.css("::text").get()
            div_tag = title.xpath("..")[0]
            following_tags = div_tag.xpath('following-sibling::*')
            for tag_element in following_tags:
                # if tag_element.root.tag in ['figure', 'p', 'table', 'img', 'a', 'chart']:
                #     pass
                if tag_element.root.tag == 'figure':
                    images.append(tag_element.css("a img::attr(src)").get())
                if tag_element.root.tag == 'p':
                    text_content.append(tag_element.css("::text").getall())
                # if tag_element.root.tag == 'p':
                #     text_content.append = tag_element.css("a::attr(href)").get()
                # if tag_element.root.tag == 'p':
                #     text_content.append = tag_element.css("a::attr(href)").get()
                
            yield {
            "title": title_text,
            "text_content": self.process_text_content(text_content),
            "images": images,
            }

    def process_text_content(self, data):
        flattened_sentence = "".join([item for sublist in data for item in (sublist if isinstance(sublist, list) else [sublist])])
        flattened_sentence = " ".join(flattened_sentence.split())
        return flattened_sentence
                


        
        
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")