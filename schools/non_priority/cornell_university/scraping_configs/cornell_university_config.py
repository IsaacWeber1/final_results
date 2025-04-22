from scraper_module.config import *

config = SpiderConfig(
    name="cornell",
    start_url="https://courses.cornell.edu/content.php?catoid=60&navoid=26201",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="https://courses.cornell.edu/ajax/preview_course.php",
            catoid=60,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)