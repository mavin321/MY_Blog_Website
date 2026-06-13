import math
import re
from collections import Counter
from datetime import datetime
from types import SimpleNamespace

import markdown
from django.http import Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import Post

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "toc"]
WORDS_PER_MINUTE = 220

FEATURED_STORY = {
    "title": "My Journey into Software Development: Exploring Back-End Development, Data Science, and Machine Learning with Python",
    "category": "Editorial Note",
    "date": datetime(2025, 2, 23, 22, 46),
    "image_url": "assets/img/blog/featuredblog.png",
    "content": """
Software development has always fascinated me because it turns curiosity into systems, experiments, and useful tools.

Python became the foundation for that journey. Its clarity made it easier to learn programming fundamentals, but its ecosystem made it possible to move far beyond the basics. The same language let me build web applications, explore data, and prototype machine learning ideas without constantly switching mental models.

## Why back-end work clicked for me

Back-end development felt like learning how digital products truly think. Designing APIs, modeling data, and building logic that remains reliable under real usage taught me to value structure over shortcuts.

Working with Django sharpened that instinct. It gave me a framework for building complete applications with authentication, data relationships, administration tools, and clean routing.

> The part I enjoy most is building systems that feel calm under complexity.

## Expanding into data science

After learning how to build applications, I wanted to understand how to learn from the information those systems create. That led me into data analysis, visualization, and experimentation with predictive models.

Data science added a different discipline. Instead of only asking whether software works, I also had to ask whether the evidence is sound, whether patterns are meaningful, and whether the output deserves trust.

## What keeps the work interesting

The overlap between engineering and data is where the work feels most alive:

- building useful products
- measuring what matters
- improving decisions with evidence
- learning continuously across disciplines

That mix is why this blog exists. It is a place for writing about back-end systems, software craftsmanship, experiments with data, and the ideas that connect them.
""",
}


def _render_markdown(content):
    return mark_safe(markdown.markdown(content, extensions=MARKDOWN_EXTENSIONS))


def _plain_text(content):
    html = markdown.markdown(content, extensions=MARKDOWN_EXTENSIONS)
    without_tags = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", without_tags).strip()


def _excerpt(content, words=30):
    text = _plain_text(content).split()
    snippet = " ".join(text[:words])
    if len(text) > words:
        return f"{snippet}..."
    return snippet


def _reading_time(content):
    word_count = len(_plain_text(content).split())
    return max(1, math.ceil(word_count / WORDS_PER_MINUTE))


def _decorate_post(post):
    post.formatted_date = post.date.strftime("%b %d, %Y")
    post.long_date = post.date.strftime("%B %d, %Y")
    post.reading_time = _reading_time(post.content)
    post.excerpt = _excerpt(post.content, words=28)
    post.subtitle = _excerpt(post.content, words=38)
    post.category_slug = slugify(post.category) or "journal"
    post.image_url = f"assets/img/blog/blogitem{post.image}.jpg"
    return post


def _all_posts():
    return [_decorate_post(post) for post in Post.objects.order_by("-date", "-id")]


def _category_data(posts):
    counts = Counter(post.category for post in posts)
    ordered_categories = sorted(counts.items(), key=lambda item: (-item[1], item[0].lower()))
    return [
        {
            "name": name,
            "slug": slugify(name) or "journal",
            "count": count,
        }
        for name, count in ordered_categories
    ]


def _featured_story():
    return SimpleNamespace(
        title=FEATURED_STORY["title"],
        category=FEATURED_STORY["category"],
        category_slug=slugify(FEATURED_STORY["category"]) or "editorial-note",
        date=FEATURED_STORY["date"],
        formatted_date=FEATURED_STORY["date"].strftime("%b %d, %Y"),
        long_date=FEATURED_STORY["date"].strftime("%B %d, %Y"),
        reading_time=_reading_time(FEATURED_STORY["content"]),
        excerpt=_excerpt(FEATURED_STORY["content"], words=26),
        subtitle=_excerpt(FEATURED_STORY["content"], words=40),
        image_url=FEATURED_STORY["image_url"],
        content_html=_render_markdown(FEATURED_STORY["content"]),
        is_featured_story=True,
    )


def index(request):
    posts = _all_posts()
    hero_post = posts[0] if posts else None
    archive_posts = posts[1:] if hero_post else []
    supporting_posts = posts[1:4] if len(posts) > 1 else []

    context = {
        "active_page": "home",
        "posts": posts,
        "hero_post": hero_post,
        "archive_posts": archive_posts,
        "supporting_posts": supporting_posts,
        "categories": _category_data(posts),
        "featured_story": _featured_story(),
        "post_count": len(posts),
        "category_count": len({post.category for post in posts}),
        "page_title": "Mavin's Blog",
        "page_description": "A thoughtful technical journal on back-end systems, data, machine learning, and software craftsmanship.",
    }
    return render(request, "index.html", context)


def author(request):
    return render(
        request,
        "author-profile.html",
        {
            "active_page": "author",
            "page_title": "Author Profile | Mavin's Blog",
            "page_description": "Learn more about Mavin Peter, a back-end developer and data-focused builder writing about systems, software, and ideas.",
        },
    )


def featured(request):
    posts = _all_posts()
    featured_post = _featured_story()
    related_posts = posts[:3]

    return render(
        request,
        "blog-details.html",
        {
            "active_page": "home",
            "post": featured_post,
            "related_posts": related_posts,
            "newer_post": None,
            "older_post": None,
            "page_title": f"{featured_post.title} | Mavin's Blog",
            "page_description": featured_post.subtitle,
        },
    )


def details(request, pk):
    posts = _all_posts()
    current_index = next((index for index, post in enumerate(posts) if str(post.id) == str(pk)), None)
    if current_index is None:
        raise Http404("Post not found")

    post = posts[current_index]
    post.content_html = _render_markdown(post.content)

    same_category_posts = [item for item in posts if item.id != post.id and item.category == post.category]
    fallback_posts = [item for item in posts if item.id != post.id and item.category != post.category]
    related_posts = (same_category_posts + fallback_posts)[:3]

    context = {
        "active_page": "home",
        "post": post,
        "newer_post": posts[current_index - 1] if current_index > 0 else None,
        "older_post": posts[current_index + 1] if current_index + 1 < len(posts) else None,
        "related_posts": related_posts,
        "page_title": f"{post.title} | Mavin's Blog",
        "page_description": post.subtitle,
    }
    return render(request, "blog-details.html", context)


def contacts(request):
    return render(
        request,
        "contact.html",
        {
            "active_page": "contact",
            "page_title": "Contact | Mavin's Blog",
            "page_description": "Reach out to Mavin Peter for collaborations, questions, or conversations around software, data, and product thinking.",
        },
    )


def custom_404(request, exception):
    return render(
        request,
        "404.html",
        {
            "active_page": "",
            "page_title": "Page Not Found | Mavin's Blog",
            "page_description": "The page you requested could not be found.",
        },
        status=404,
    )
