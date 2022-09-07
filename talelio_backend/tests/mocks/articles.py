from talelio_backend.tests.mocks.example_markdown import (ART_TO_ENGINEERING_ARTICLE_BODY,
                                                          BACKUP_POSTGRES_ARTICLE_BODY,
                                                          BACKUP_STRATEGY_ARTICLE_BODY,
                                                          FIXED_OR_ROTARY_WING_ARTICLE_BODY,
                                                          HIKING_GEAR_ARTICLE_BODY,
                                                          PRIVATE_BLOCKCHAIN_ARTICLE_BODY)

art_to_engineering_article = {
    'title': 'From Art to Engineering',
    'body': ART_TO_ENGINEERING_ARTICLE_BODY,
    'meta_description': 'Changing the studio and oil paints for an office and a code editor.'
}

private_blockchain_article = {
    'title': 'Dockerize a Private Blockchain',
    'body': PRIVATE_BLOCKCHAIN_ARTICLE_BODY,
    'meta_description': 'Setup a test environment with a dockerized blockchain.'
}

backup_postgres_article = {
    'title': 'Backing up Dockerized PostgreSQL Db from EC2 to S3',
    'body': BACKUP_POSTGRES_ARTICLE_BODY,
    'meta_description': 'Setup Cron Job for automatic database dumps to S3 bucket.'
}

backup_strategy_article = {
    'title': 'The Backup Strategy',
    'body': BACKUP_STRATEGY_ARTICLE_BODY,
    'meta_description': 'Designing a backup routine.'
}

fixed_or_rotary_wing_article = {
    'title': "Fixed or Rotary Wing Pilot's License",
    'body': FIXED_OR_ROTARY_WING_ARTICLE_BODY,
    'meta_description': 'Deciding factors for whether to pursuit a PPL(A) or PPL(H).'
}

hiking_gear_article = {
    'title': 'Packing Lists for Hiking Trips',
    'body': HIKING_GEAR_ARTICLE_BODY,
    'meta_description': 'Items for the outdoors.'
}

articles = [
    art_to_engineering_article, private_blockchain_article, backup_postgres_article,
    backup_strategy_article, fixed_or_rotary_wing_article, hiking_gear_article
]
