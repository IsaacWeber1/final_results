from scraper_module.config import *

config = SpiderConfig(
    name="uchicago",
    start_url="http://collegecatalog.uchicago.edu/thecollege/programsofstudy/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://li[@class="active self"]',
        link_selector='xpath:/ul/li/a/@href',
        target_page_selector='html', # Target page to scrape
        max_depth = 1
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://div[@class="sc_sccoursedescs"]',
            repeating_selector="div",
            fields={
                "title": 'xpath:p[@class="courseblocktitle"]/strong//text()join',
                "description": 'xpath:p[@class="courseblockdesc"]//text()join'
            },
            num_required=1
        )
    ]
)