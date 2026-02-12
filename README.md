# MapleStory-Server-079（Python 3.12 重构与容器化）

一个将 MapleStory 079 版 Java 代码结构化转换为 Python 的模板工程：
- 目录结构保持与原 Java 工程一致（迁移到 src/ 下的 Python 包）
- 提供 main.py 作为启动入口（Python 3.12）
- 提供 Dockerfile + docker-compose.yml（app + MySQL）
- 提供 JPype JAR 桥接（可调用 bin/maple.jar，或回退为 `java -jar`）
- 统一源码与文件名编码为 UTF-8，命名风格 English + snake_case（不使用中文或不可读的变量名）

---

## 基本运行环境
- Python 3.12+
- Docker 24+ / docker-compose v2+
- MySQL 8.0（compose 内置服务 `db`）
- 可选：本地 JRE（容器内已包含 headless JRE 以支持 JPype）
- 操作系统：Linux / macOS / Windows（建议 WSL2）

```sh
python3 -V
pip -V
```

## 安装依赖（非容器）
```sh
pip install -r requirements.txt
```

## 启动

- 直接运行（非容器）：
```sh
python main.py
```
> 默认从环境变量或 `./config/db.properties` 读取数据库配置。

- 使用 Docker Compose：
```sh
# 首次或变更后建议先 build
docker compose up --build

# 常规启动
docker compose up

# 查看日志
docker compose logs -f app

# 进入容器
docker compose exec app bash
```
> 预期：`db` 服务（MySQL）常驻；`app` 输出 Python 版本与 DB 配置后退出（当前为结构化占位实现）。

### 环境变量（app）
- `DB_HOST`（默认：db）
- `DB_PORT`（默认：3306）
- `DB_NAME`（默认：maple）
- `DB_USER`（默认：maple）
- `DB_PASSWORD`（默认：maple）
- `JAR_PATH`（可选，默认：`./bin/maple.jar`）

## 目录结构（节选）
```
MapleStory-Server-079
├─ main.py                       # Python 启动入口
├─ requirements.txt              # Python 依赖
├─ Dockerfile                    # Python 3.12 + headless JRE
├─ docker-compose.yml            # app + MySQL 服务
├─ bin/
│  └─ maple.jar                  # 可选的外部 JAR（JPype 桥接）
├─ config/
│  └─ db.properties              # 数据库连接配置（可用环境变量覆盖）
└─ src/
   ├─ bridge/
   │  └─ jar_bridge.py           # JPype 桥接（或 java -jar 回退）
   ├─ server/ ...                # 结构化转换后的模块（占位 + 注释）
   ├─ tools/ ...                 # 工具模块（含 wztosql）
   │  └─ wztosql/
   │     ├─ WzStringDumper.py
   │     ├─ WzStringDumper_pet_data.py
   │     ├─ WzStringDumper_equipment_data.py
   │     ├─ WzStringDumper_unknown1.py
   │     └─ WzStringDumper_unknown2.py
   └─ ...
```

## 维护规范
- 编码统一为 UTF-8（源码与文件名）
- 命名规范：英文 + snake_case；不使用中文或不可读（如 a1、b2、lIlI）变量名
- 模块/类/函数注释：尽量简要说明用途与参数
- 数据库配置：优先环境变量，其次 `config/db.properties`
- 依赖管理：`requirements.txt`
- 推荐工具：
  - 代码格式化：black（可选）
  - 代码校验：ruff 或 flake8（可选）

## JPype 桥接用法（可选）
```python
from src.bridge.jar_bridge import start_jvm, call_main_with_subprocess

# 优先尝试 JPype 启动 JVM（classpath 包含 bin/maple.jar）
ok = start_jvm()
if not ok:
    # 回退为外部进程
    rc = call_main_with_subprocess(["--help"])  # 例子
```

## 常用 Docker 命令
```sh
# 启动/停止/重启
docker start|stop|restart <container_id|container_name>

# 查看容器列表
docker ps

# 查看日志
docker logs --tail 50 -f <container_id|container_name>

# 移除容器
docker rm [-f] <container_id|container_name>
```

## 开发路线（后续）
- 将网络栈（Apache MINA）逐步迁移到 asyncio
- 将数据库访问替换为 PyMySQL 并梳理连接池/事务
- 逐步将占位实现替换为可运行逻辑
- 配置文件可按需迁移到 JSON/YAML（当前兼容 .properties）

---

如需对变量命名和文件重命名提出偏好（英文描述 / 拼音 / 统一英文），请在 PR 中评论说明。

