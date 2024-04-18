import re
import time
import secrets
import uuid
from collections import OrderedDict
from multiprocessing import Semaphore
from typing import Optional, List


class TokenGenerator:

    @staticmethod
    def generate_token() -> str:
        return f"{uuid.uuid4().hex}{secrets.token_hex(32)}"


class SessionData:

    def __init__(self, created_timestamp_sec: float, access_token: str, public_key: str):
        self.last_used = created_timestamp_sec
        self.access_token = access_token
        self.public_key = public_key


class SessionCache:
    def __init__(self, ttl_sec: int):
        self._cache = OrderedDict()
        self._ttl_sec = ttl_sec
        self._cache_lock = Semaphore(1)

    def _invalidate_old(self, cutoff: float) -> None:
        keys_to_delete = []
        for key, data in self._cache.items():
            if data.last_used >= cutoff:
                break
            keys_to_delete.append(key)

        for key in keys_to_delete:
            del (self._cache[key])

    def get(self, user_token: str) -> Optional[SessionData]:
        """
        Retrieve session data from cache by token
        @param user_token: user access token
        @return: session data for the token or None
        """
        self._cache_lock.acquire()
        try:
            session_data = self._cache.get(user_token, None)
            if session_data is None:
                return None

            # invalidate old record
            now = time.time()
            cutoff = now - self._ttl_sec
            if session_data.last_used < cutoff:
                del(self._cache[user_token])
                return None

            # update record
            session_data.last_used = now
            self._cache.move_to_end(user_token)
        finally:
            self._cache_lock.release()

        return session_data

    def put(self, public_key: str) -> SessionData:
        """
        Insert a new token into the cache and perform cleanup of old records if there are any
        @param public_key: public key serving as a username
        @return inserted session data
        """
        now = time.time()
        user_token = TokenGenerator.generate_token()
        new_record = SessionData(now, user_token, public_key)
        self._cache[user_token] = new_record
        self._invalidate_old(now - self._ttl_sec)
        return new_record

    def get_all(self) -> OrderedDict:
        """
        Get the entire cache content
        :return: copy of the internal cache dict
        """
        return OrderedDict(self._cache)
