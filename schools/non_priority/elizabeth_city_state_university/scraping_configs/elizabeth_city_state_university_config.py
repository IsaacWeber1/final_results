from scraper_module.config import *

config = SpiderConfig(
    name="ecsu",
    start_url="https://catalog.ecsu.edu/content.php?catoid=5&navoid=180",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="https://catalog.ecsu.edu/ajax/preview_course.php",
            catoid=5,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)