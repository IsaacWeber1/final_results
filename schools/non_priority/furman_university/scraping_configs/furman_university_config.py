from scraper_module.config import *

config = SpiderConfig(
    name="furman",
    start_url="https://catalog.furman.edu/content.php?catoid=27&navoid=1463",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="http://catalog.furman.edu/ajax/preview_course.php",
            catoid=27,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)