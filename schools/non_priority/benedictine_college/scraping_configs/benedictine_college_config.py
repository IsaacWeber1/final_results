from scraper_module.config import *

config = SpiderConfig(
    name="benedictine",
    start_url="https://coursecatalog.benedictine.edu/course-descriptions/",
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
            search_space='xpath://div[@class="sc_sccoursedescs"]',
            repeating_selector="div",
            fields={
                "title": 'xpath:div[@class="cols noindent"]/span//text()join',
                "description": 'xpath:div[@class="noindent"]/p[@class="courseblockextra noindent"]//text()join'
            },
            num_required=1
        )
    ]
)