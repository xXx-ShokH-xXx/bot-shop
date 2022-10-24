from dataclasses import dataclass # Mahsus metodlarni avtomatik qo'shish uchun kerak __init__(), __repr__() kabi
from typing import List # typing moduli tiplardagi izohlarni bajarish uchun yordam beradi
from telebot.types import LabeledPrice # LabeledPrice narx bilan ishlaydi
from config import PROVIDER_TOKEN # Pul o'tkazmalari uchun token

@dataclass
class Product:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = PROVIDER_TOKEN

    def generate_invoice(self):
        return self.__dict__ # Product classidagi ma'lumotlarni dict ko'rinishida qaytaradi.

