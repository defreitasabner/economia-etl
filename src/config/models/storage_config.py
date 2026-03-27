from typing import Literal, Union

from pydantic import BaseModel


StorageTier = Literal['bronze', 'silver', 'gold']

class BronzeStorageConfig(BaseModel):
	output_path: str
	output_format: str

class SilverStorageConfig(BaseModel):
	input_path: str
	input_format: str
	output_path: str
	output_format: str

class StorageConfig(BaseModel):
	bronze: BronzeStorageConfig
	silver: SilverStorageConfig

	def get_tier(self, tier: StorageTier) -> Union[BronzeStorageConfig, SilverStorageConfig]:
		return getattr(self, tier)

