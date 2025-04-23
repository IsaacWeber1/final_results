from scraper_module.config import *

config = SpiderConfig(
    name="mellon_university",
    start_url="http://coursecatalog.web.cmu.edu/coursedescriptions/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://div[@id="textcontainer"]',
        link_selector='xpath://li/a/@href',
        target_page_selector='html',
        max_depth=1,
        # base_url = "http://coursecatalog.web.cmu.edu/"
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://div[@class="courses"]',
            repeating_selector="dl",
            fields={
                "title": 'xpath:dt//text()',
                "description": 'xpath:dd//text()join'
            },
            num_required=1
        )
    ]
)