from scraper_module.config import *

config = SpiderConfig(
    name="berkeley",
    start_url="https://guide.berkeley.edu/courses/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://*[@id="textcontainer"]/div',
        link_selector='xpath:/ul/li/a/@href',
        target_page_selector='html', # Target page to scrape
        max_depth = 1
    ),
    tasks=[
        Find(
            task_name="courses",
            search_space='xpath://div[@id="sc_sccoursedescs"]',
            repeating_selector="div",
            fields={
                "title": 'xpath:button[@class="btn_toggleCoursebody"]/h3[@class="courseblocktitle"]/span//text()join',
                "description": 'xpath:div[@class="coursebody"]/p[@class="courseblockdesc"]/span//text()join'
            },
            num_required=1
        )
    ]
)