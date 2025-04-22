from scraper_module.config import *

config = SpiderConfig(
    name="houston",
    start_url="https://publications.uh.edu/content.php?catoid=52&navoid=19813",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="https://publications.uh.edu/ajax/preview_course.php",
            catoid=52,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)