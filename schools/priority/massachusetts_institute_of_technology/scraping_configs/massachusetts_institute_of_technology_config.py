from scraper_module.config import *

config = SpiderConfig(
    name="mit",
    start_url="https://catalog.mit.edu/subjects/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://ul[contains(@id, "/subjects/")]',
        link_selector="xpath:li/a/@href",
        target_page_selector='html'
    ),
     tasks=[
        Find(
            task_name="courses",
            # Corrected the attribute selector: use = instead of a comma
            search_space='xpath://div[@class="page_content"]',
            # Added a dot to make the repeating selector relative to the search_space element
            repeating_selector='xpath://div[@id="content"]',
            fields={
                "category":'xpath:.//h1[contains(@class, "page-title")]/text()',
               "title": 'xpath:.//h4[contains(@class, "courseblocktitle")]/span/strong/text()',
                "description": 'xpath:.//p[contains(@class, "courseblockdesc")]/text()join'
            },
            num_required=1
        )
    ]
)