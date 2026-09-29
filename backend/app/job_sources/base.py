from abc import ABC, abstractmethod


class JobSourceAdapter(ABC):
    source_name = "BASE"

    @abstractmethod
    def search_jobs(self, query: str, location: str | None = None, page: int = 1):
        raise NotImplementedError

    @abstractmethod
    def get_job_details(self, job_id: str):
        raise NotImplementedError

    @abstractmethod
    def normalize_job(self, raw_job: dict):
        raise NotImplementedError

    @abstractmethod
    def supports_application(self, job: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def start_application(self, job: dict):
        raise NotImplementedError

    @abstractmethod
    def fill_application(self, job: dict, user_profile: dict):
        raise NotImplementedError

    @abstractmethod
    def submit_application(self, job: dict):
        raise NotImplementedError
