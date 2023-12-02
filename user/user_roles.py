from enum import Enum


class Rolename(Enum):
    USER = 'user'
    ADMIN = 'admin'


all_roles = [Rolename.USER, Rolename.ADMIN]
