from talelio_backend.app_article.domain.article_model import Article
from talelio_backend.tests.mocks.articles import art_to_engineering_article


def test_can_generate_article_url() -> None:
    article = Article(art_to_engineering_article['title'], art_to_engineering_article['body'],
                      art_to_engineering_article['meta_description'])

    assert article.url == 'https://www.talel.io/articles/from-art-to-engineering'
