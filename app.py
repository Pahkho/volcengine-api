from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 初始化核心应用
app = FastAPI(
    title="Volcengine FASTAPI代理",
    description="Volcengine FASTAPI代理服务",
    version="1.0.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由模块
from routers import health, agent, task

app.include_router(agent.router, prefix="/api")
app.include_router(task.router, prefix="/api")
app.include_router(health.router)

# 启动服务
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5002, reload=True)