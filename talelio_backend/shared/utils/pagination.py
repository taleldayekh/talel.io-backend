from math import ceil


class Pagination:

    @staticmethod
    def calculate_offset(page: int, limit: int) -> int:
        return ((abs(page) - 1) * abs(limit) + 1) - 1

    @staticmethod
    def total_pages(entries: int, limit: int) -> int:
        return ceil(entries / limit)
