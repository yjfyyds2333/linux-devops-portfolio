# Week1:Docker Compose 多容器编排


## 项目内容
用docker-compose编排4个容器:Nginx反向代理+python爬虫+MySQL数据库

## 技术栈
-Docker Compose 
-Nginx (反向代理)
-MySQL9.6 (数据持久化)
Python （爬取豆瓣TOP250）

## 快速启动
```bash
cp .env.example .env
# 编辑.env填入密码
docker compose up -d 
```

## 截图
<img width="778" height="254" alt="4个容器运行" src="https://github.com/user-attachments/assets/02b4eeeb-7e44-4fab-b506-05c6718dfabe" />

<img width="844" height="483" alt="nginx容器里成功连接mysql" src="https://github.com/user-attachments/assets/b6a31a59-049b-4fff-a95b-353a0d2c401a" />

<img width="832" height="226" alt="scheduler py启动成功" src="https://github.com/user-attachments/assets/cb292a7e-1ccb-474d-97e2-152843b8e266" />

<img width="1138" height="596" alt="成功将爬虫爬到的数据写入mysql中" src="https://github.com/user-attachments/assets/ff9138ad-b46a-4935-a680-d8520499b34e" />

## Week1总结
# 本周学习精炼总结 & 核心避坑手册

---

## 一、核心知识体系（4大模块核心）

### 1. Docker容器化与编排

- 网络：**自定义bridge网络支持服务名互访**，默认bridge不支持；容器互通默认开启（icc=true），关闭后需用`-link`显式关联
- 环境变量：优先级 `Shell > environment指令 > .env文件`；用`os.environ.get(键, 兜底值)`安全读取，避免无配置时报错
- 健康检查：通过`test/interval/retries/start_period`定义检查规则，配合`depends_on: service_healthy`确保依赖服务就绪后启动

### 2. Nginx反向代理

- 配置层级：全局块 → events块 → http块 → server块 → location块，嵌套划分作用域
- 核心配置：单后端直接用`proxy_pass`转发；多后端负载均衡需先定义`upstream`上游组，再通过`proxy_pass`引用
- 配置生成：用`<< 'EOF'`（单引号包裹）的Here Document生成配置，避免Shell解析`$host`等内置变量

### 3. Python爬虫与数据入库

- 爬虫：`requests`库处理请求/headers/响应解析；BeautifulSoup4用内置`html.parser`解析HTML，通过`find()`/`find_all()`/CSS选择器定位节点，class属性需写`class_`规避Python关键字冲突
- 数据库：`pymysql`中`db`连接对象管理事务/网络连接，`cursor`游标对象执行SQL；增删改操作必须`commit()`提交，异常时`rollback()`回滚

### 4. 工程化与定时任务

- 定时任务：`schedule`库定义定时规则，主循环必须加`time.sleep()`降低CPU占用
- 敏感管理：`.env`存密码/密钥，**绝对不推GitHub**，用`.gitignore`排除，仅上传无真实值的`.env.example`模板
- 依赖管理：所有第三方库必须写入`requirements.txt`，确保镜像构建时自动安装

---

## 二、核心避坑手册（高频踩坑速查）

### 1. Docker&MySQL类

| 坑点 | 核心原因 | 解决方案 |
| --- | --- | --- |
| MySQL8.0+ `caching_sha2_password` 认证报错 | 新版本默认认证方式变更 | pymysql配置加`ssl_disabled=True`，或建用户时指定`mysql_native_password` |
| 容器间服务名访问失败 | 默认bridge网络不支持服务名解析 | 用Compose自动创建的自定义网络 |
| MySQL 1045权限拒绝 | 用户未创建/变量名不匹配/普通用户权限冲突 | 优先用root用户连接，`docker compose down -v`清空旧数据重新初始化 |
| 健康检查失败、容器异常重启 | 检查命令错误/启动预热期不足 | 修正检查命令，给足`start_period`预热时间 |

### 2. 代码&工程化类

| 坑点 | 核心原因 | 解决方案 |
| --- | --- | --- |
| BeautifulSoup找class语法报错 | `class`是Python保留关键字 | 用`class_="xxx"`替代 |
| 定时任务导致CPU爆满 | 主循环无sleep、高频空转 | while循环内加`time.sleep(1)` |
| 镜像运行报`ModuleNotFoundError` | 依赖未写入`requirements.txt` | 所有第三方库全量写入依赖文件 |
| .env推仓库泄露敏感信息 | 未配置`.gitignore` | `.gitignore`添加`.env`，仅上传`.env.example`模板 |

### 3. Nginx配置类

| 坑点 | 核心原因 | 解决方案 |
| --- | --- | --- |
| 配置内`$`变量被Shell替换 | Here Document未加单引号 | 用`<< 'EOF'`生成配置，禁止Shell解析变量 |

---

## 三、落地建议

核心架构：Docker Compose一键编排「MySQL+爬虫容器+Nginx展示页」
核心功能：`schedule`定时抓取招投标公告→MySQL结构化存储→Nginx简易前端展示，配合健康检查保障服务依赖顺序
工程规范：严格遵循依赖管理、敏感信息隔离规则

---

## 四、项目启动核心Checklist

- [ ]  所有第三方依赖全量写入`requirements.txt`
- [ ]  `.env`变量名与compose一致，已加入`.gitignore`
- [ ]  环境变量读取加兜底值，数据库操作加事务提交/回滚
- [ ]  定时任务循环加sleep，MySQL健康检查配置正确
- [ ]  Nginx配置生成用带单引号的`<< 'EOF'`语法
