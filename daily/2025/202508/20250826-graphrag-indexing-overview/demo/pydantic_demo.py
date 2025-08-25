import yaml
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class StorageType(str, Enum):
    """存储类型枚举"""
    FILE = "file"
    AZURE_BLOB = "azure_blob"
    S3 = "s3"

class DatabaseConfig(BaseModel):
    """数据库配置模型"""
    host: str = Field(default="localhost", description="数据库主机")
    port: int = Field(default=5432, description="数据库端口")
    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    
    @field_validator("port")
    @classmethod
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("端口必须在 1-65535 范围内")
        return v

class AppConfig(BaseModel):
    """主配置模型"""
    app_name: str = Field(default="MyApp", description="应用名称")
    debug: bool = Field(default=False, description="调试模式")
    storage_type: StorageType = Field(default=StorageType.FILE, description="存储类型")
    database: DatabaseConfig = Field(description="数据库配置")
    
    # 自定义验证器
    @field_validator("app_name")
    @classmethod
    def validate_app_name(cls, v):
        if not v.strip():
            raise ValueError("应用名称不能为空")
        return v.strip()

def load_config_from_yaml(yaml_path: Path) -> AppConfig:
    """从 YAML 文件加载配置"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # Pydantic 自动验证和转换
    return AppConfig(**config_data)

# 使用示例
config_file = Path("config.yaml")
config = load_config_from_yaml(config_file)
print(f"应用名称: {config.app_name}")
print(f"数据库配置: {config.database.host}:{config.database.port}")